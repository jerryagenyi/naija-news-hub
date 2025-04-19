-- Reset database script
-- Date: April 19, 2025

-- Drop existing tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS scraping_errors CASCADE;
DROP TABLE IF EXISTS scraping_jobs CASCADE;
DROP TABLE IF EXISTS article_categories CASCADE;
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS websites CASCADE;

-- Create websites table
CREATE TABLE websites (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    base_url VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    logo_url VARCHAR(255),
    sitemap_url VARCHAR(255),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create articles table with optimized structure
CREATE TABLE articles (
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

-- Create article_categories table
CREATE TABLE article_categories (
    article_id INTEGER REFERENCES articles(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, category_id)
);

-- Create scraping_jobs table
CREATE TABLE scraping_jobs (
    id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    articles_found INTEGER DEFAULT 0,
    articles_scraped INTEGER DEFAULT 0,
    error_message TEXT,
    config JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create scraping_errors table
CREATE TABLE scraping_errors (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES scraping_jobs(id) ON DELETE CASCADE,
    url VARCHAR(512),
    error_type VARCHAR(255) NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_categories_website_id ON categories(website_id);
CREATE INDEX idx_articles_website_id ON articles(website_id);
CREATE INDEX idx_articles_published_at ON articles(published_at);
CREATE INDEX idx_articles_last_checked_at ON articles(last_checked_at);
CREATE INDEX idx_articles_metadata_gin ON articles USING gin (article_metadata);
CREATE INDEX idx_scraping_jobs_website_id ON scraping_jobs(website_id);
CREATE INDEX idx_scraping_jobs_status ON scraping_jobs(status);
CREATE INDEX idx_scraping_errors_job_id ON scraping_errors(job_id);
CREATE INDEX idx_scraping_errors_error_type ON scraping_errors(error_type);

-- Add comments to tables
COMMENT ON TABLE articles IS 'Stores scraped article content and metadata. Content is stored as structured JSON in article_metadata with a complete structure including title, author, date, categories, and content.';
COMMENT ON TABLE categories IS 'Stores category information for news websites. Categories are website-specific.';
COMMENT ON TABLE websites IS 'Stores information about news websites being scraped.';
COMMENT ON TABLE article_categories IS 'Junction table linking articles to categories.';
COMMENT ON TABLE scraping_jobs IS 'Stores information about scraping jobs.';
COMMENT ON TABLE scraping_errors IS 'Stores error information for debugging and monitoring.';

-- Insert a test website
INSERT INTO websites (name, base_url, description, active)
VALUES ('Blueprint News', 'https://blueprint.ng', 'Nigerian news website covering politics, business, and more', TRUE);

-- Insert some test categories
INSERT INTO categories (name, url, website_id, active)
VALUES
('Politics', 'https://blueprint.ng/category/politics', 1, TRUE),
('Business', 'https://blueprint.ng/category/business', 1, TRUE),
('Entertainment', 'https://blueprint.ng/category/entertainment', 1, TRUE);

-- Success message
SELECT 'Database reset complete. Created tables: websites, categories, articles, article_categories, scraping_jobs, scraping_errors' AS result;
