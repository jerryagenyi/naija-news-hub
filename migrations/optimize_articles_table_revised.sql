-- Revised migration script to optimize the articles table structure
-- Date: April 19, 2025

-- 1. Add a tags column to store article tags
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                  WHERE table_name='articles' AND column_name='tags') THEN
        ALTER TABLE articles ADD COLUMN tags JSONB;
    END IF;
END $$;

-- 2. Create a temporary table with the new structure
CREATE TABLE articles_new (
    id SERIAL PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    url VARCHAR(512) NOT NULL UNIQUE,
    author VARCHAR(255),
    published_at TIMESTAMP,
    image_url VARCHAR(512),
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    article_metadata JSONB,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    tags JSONB,
    last_checked_at TIMESTAMP
);

-- 3. Copy data from the old table to the new table
INSERT INTO articles_new (
    id, title, url, author, published_at, image_url, website_id,
    active, created_at, updated_at, tags, last_checked_at
)
SELECT
    id, title, url, author, published_at, image_url, website_id,
    active, created_at, updated_at, tags, NULL
FROM articles;

-- 4. For each record, create a structured JSON object with the content
UPDATE articles_new
SET article_metadata = COALESCE(
    (SELECT metadata FROM articles WHERE articles.id = articles_new.id),
    '{}'::jsonb
) || jsonb_build_object(
    'content', jsonb_build_object(
        'markdown', (SELECT COALESCE(content_markdown, content_markdc, content) FROM articles WHERE articles.id = articles_new.id),
        'word_count', (CASE WHEN (SELECT metadata->>'word_count' FROM articles WHERE articles.id = articles_new.id) IS NOT NULL
                       THEN (SELECT metadata->>'word_count' FROM articles WHERE articles.id = articles_new.id)::integer
                       ELSE NULL END),
        'reading_time', (CASE WHEN (SELECT metadata->>'reading_time' FROM articles WHERE articles.id = articles_new.id) IS NOT NULL
                         THEN (SELECT metadata->>'reading_time' FROM articles WHERE articles.id = articles_new.id)::integer
                         ELSE NULL END)
    ),
    'metadata', jsonb_build_object(
        'title', articles_new.title,
        'author', articles_new.author,
        'published_date', articles_new.published_at,
        'source_website', (SELECT name FROM websites WHERE websites.id = articles_new.website_id),
        'source_url', articles_new.url,
        'image_url', articles_new.image_url,
        'categories', (SELECT jsonb_agg(jsonb_build_object(
            'name', c.name,
            'url', c.url
        )) FROM categories c
        JOIN article_categories ac ON c.id = ac.category_id
        WHERE ac.article_id = articles_new.id)
    )
);

-- 5. Move tags from metadata to tags column if they exist
UPDATE articles_new
SET tags = (SELECT metadata->'tags' FROM articles WHERE articles.id = articles_new.id)
WHERE (SELECT metadata->'tags' FROM articles WHERE articles.id = articles_new.id) IS NOT NULL;

-- 6. Create indexes on the new table
CREATE INDEX idx_articles_new_website_id ON articles_new(website_id);
CREATE INDEX idx_articles_new_published_at ON articles_new(published_at);
CREATE INDEX idx_articles_new_last_checked_at ON articles_new(last_checked_at);
CREATE INDEX idx_articles_new_metadata_gin ON articles_new USING gin (article_metadata);

-- 7. Rename tables to swap them
ALTER TABLE articles RENAME TO articles_old;
ALTER TABLE articles_new RENAME TO articles;

-- 8. Update foreign key constraints in article_categories
ALTER TABLE article_categories DROP CONSTRAINT article_categories_article_id_fkey;
ALTER TABLE article_categories ADD CONSTRAINT article_categories_article_id_fkey
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE;

-- 9. Drop the old table
DROP TABLE articles_old;

-- 10. Add a comment to the table
COMMENT ON TABLE articles IS 'Stores scraped article content and metadata. Content is stored as structured JSON in article_metadata with a complete structure including title, author, date, categories, and content.';
