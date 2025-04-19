-- Revised migration script to optimize the articles table structure
-- Date: May 16, 2025

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
    )
);

-- 5. Create indexes on the new table
CREATE INDEX idx_articles_new_website_id ON articles_new(website_id);
CREATE INDEX idx_articles_new_published_at ON articles_new(published_at);
CREATE INDEX idx_articles_new_last_checked_at ON articles_new(last_checked_at);

-- 6. Rename tables to swap them
ALTER TABLE articles RENAME TO articles_old;
ALTER TABLE articles_new RENAME TO articles;

-- 7. Update foreign key constraints in article_categories
ALTER TABLE article_categories DROP CONSTRAINT article_categories_article_id_fkey;
ALTER TABLE article_categories ADD CONSTRAINT article_categories_article_id_fkey 
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE;

-- 8. Drop the old table
DROP TABLE articles_old;

-- 9. Add a comment to the table
COMMENT ON TABLE articles IS 'Stores scraped article content and metadata. Content is stored as structured JSON in article_metadata.';
