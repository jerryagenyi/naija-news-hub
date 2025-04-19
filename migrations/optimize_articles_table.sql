-- Migration script to optimize the articles table structure
-- Date: May 16, 2025

-- 1. First, add a new column for content_markdc (if it doesn't exist already)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='articles' AND column_name='content_markdc') THEN
        ALTER TABLE articles ADD COLUMN content_markdc TEXT;
    END IF;
END $$;

-- 2. Add columns for tracking content updates
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='articles' AND column_name='last_checked_at') THEN
        ALTER TABLE articles ADD COLUMN last_checked_at TIMESTAMP;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='articles' AND column_name='update_count') THEN
        ALTER TABLE articles ADD COLUMN update_count INTEGER DEFAULT 0;
    END IF;
END $$;

-- 3. Copy content_markdown to content_markdc for existing records
UPDATE articles 
SET content_markdc = content_markdown 
WHERE content_markdc IS NULL AND content_markdown IS NOT NULL;

-- 4. Create a temporary table with the new structure
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
    content_markdc TEXT,
    last_checked_at TIMESTAMP,
    update_count INTEGER DEFAULT 0
);

-- 5. Copy data from the old table to the new table
INSERT INTO articles_new (
    id, title, url, author, published_at, image_url, website_id, 
    active, created_at, updated_at, content_markdc, last_checked_at, update_count
)
SELECT 
    id, title, url, author, published_at, image_url, website_id, 
    active, created_at, updated_at, content_markdc, last_checked_at, update_count
FROM articles;

-- 6. For each record, create a JSON object with the content and add it to article_metadata
UPDATE articles_new
SET article_metadata = COALESCE(
    (SELECT metadata FROM articles WHERE articles.id = articles_new.id),
    '{}'::jsonb
) || jsonb_build_object(
    'content', (SELECT content FROM articles WHERE articles.id = articles_new.id),
    'content_html', (SELECT content_html FROM articles WHERE articles.id = articles_new.id),
    'content_markdown', (SELECT content_markdown FROM articles WHERE articles.id = articles_new.id)
);

-- 7. Create indexes on the new table
CREATE INDEX idx_articles_new_website_id ON articles_new(website_id);
CREATE INDEX idx_articles_new_published_at ON articles_new(published_at);
CREATE INDEX idx_articles_new_last_checked_at ON articles_new(last_checked_at);

-- 8. Rename tables to swap them
ALTER TABLE articles RENAME TO articles_old;
ALTER TABLE articles_new RENAME TO articles;

-- 9. Update foreign key constraints in article_categories
ALTER TABLE article_categories DROP CONSTRAINT article_categories_article_id_fkey;
ALTER TABLE article_categories ADD CONSTRAINT article_categories_article_id_fkey 
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE;

-- 10. Drop the old table
DROP TABLE articles_old;

-- 11. Add a comment to the table
COMMENT ON TABLE articles IS 'Stores scraped article content and metadata. Content is stored in content_markdc (Markdown) and as JSON in article_metadata.';
