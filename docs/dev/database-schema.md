# Naija News Hub - Database Schema Documentation

This document provides a comprehensive overview of the database schema for the Naija News Hub project, including table definitions, relationships, and SQL creation scripts.

## Entity-Relationship Diagram

```
+----------------+       +----------------+       +----------------+
|    websites    |       | scraping_jobs  |       |   categories   |
+----------------+       +----------------+       +----------------+
| id             |<----->| website_id     |       | id             |
| name           |       | status         |       | name           |
| base_url       |       | start_time     |       | url            |
| description    |       | end_time       |       | website_id     |<----+
| logo_url       |       | articles_found |       | active         |     |
| sitemap_url    |       | articles_scraped|      | created_at     |     |
| active         |       | error_message  |       | updated_at     |     |
| created_at     |       | config         |       +----------------+     |
| updated_at     |       | created_at     |                              |
+----------------+       | updated_at     |                              |
        ^                +----------------+                              |
        |                        |                                       |
        |                        v                                       |
        |                +----------------+                              |
        |                | scraping_errors|                              |
        |                +----------------+                              |
        |                | id             |                              |
        |                | job_id         |                              |
        |                | url            |                              |
        |                | error_type     |                              |
        |                | error_message  |                              |
        |                | stack_trace    |                              |
        |                | created_at     |                              |
        |                +----------------+                              |
        |                                                                |
        |                                                                |
        |                +----------------+       +----------------+      |
        |                |    articles    |       |article_categories|    |
        +--------------->| id             |<----->| article_id     |     |
                         | title          |       | category_id    |-----+
                         | url            |       +----------------+
                         | content        |
                         | content_markdown|
                         | content_html   |
                         | author         |
                         | published_at   |
                         | image_url      |
                         | website_id     |
                         | metadata       |
                         | active         |
                         | created_at     |
                         | updated_at     |
                         +----------------+
```

## Table Definitions

### 1. websites

Stores information about news websites being scraped.

| Column Name       | Data Type      | Constraints       | Description                                |
|-------------------|----------------|-------------------|--------------------------------------------|
| id                | SERIAL         | PRIMARY KEY       | Unique identifier for the website          |
| name              | VARCHAR(255)   | NOT NULL          | Name of the website                        |
| base_url          | VARCHAR(255)   | NOT NULL, UNIQUE  | Base URL of the website                    |
| description       | TEXT           |                   | Description of the website                 |
| logo_url          | VARCHAR(255)   |                   | URL of the website logo                    |
| sitemap_url       | VARCHAR(255)   |                   | URL of the sitemap                         |
| active            | BOOLEAN        | DEFAULT TRUE      | Whether the website is active              |
| created_at        | TIMESTAMP      | DEFAULT NOW()     | When the record was created                |
| updated_at        | TIMESTAMP      | DEFAULT NOW()     | When the record was last updated           |

### 2. scraping_jobs

Stores information about scraping jobs.

| Column Name    | Data Type      | Constraints                | Description                                |
|----------------|----------------|----------------------------|--------------------------------------------|
| id             | SERIAL         | PRIMARY KEY                | Unique identifier for the scraping job     |
| website_id     | INTEGER        | FOREIGN KEY (websites.id)  | Reference to the website                   |
| status         | VARCHAR(50)    | NOT NULL, DEFAULT 'pending'| Status of the job (pending/running/completed/failed) |
| start_time     | TIMESTAMP      |                            | When the job started                       |
| end_time       | TIMESTAMP      |                            | When the job ended                         |
| articles_found | INTEGER        | DEFAULT 0                  | Number of articles found                   |
| articles_scraped| INTEGER       | DEFAULT 0                  | Number of articles scraped                 |
| error_message  | TEXT           |                            | Error message if job failed                |
| config         | JSON           |                            | Configuration for the job                  |
| created_at     | TIMESTAMP      | DEFAULT NOW()              | When the record was created                |
| updated_at     | TIMESTAMP      | DEFAULT NOW()              | When the record was last updated           |

### 3. categories

Stores category information for news websites.

| Column Name    | Data Type      | Constraints                | Description                                |
|----------------|----------------|----------------------------|--------------------------------------------|
| id             | SERIAL         | PRIMARY KEY                | Unique identifier for the category         |
| name           | VARCHAR(255)   | NOT NULL                   | Name of the category                       |
| url            | VARCHAR(255)   | NOT NULL                   | URL of the category page                   |
| website_id     | INTEGER        | FOREIGN KEY (websites.id)  | Reference to the website                   |
| active         | BOOLEAN        | DEFAULT TRUE               | Whether the category is active             |
| created_at     | TIMESTAMP      | DEFAULT NOW()              | When the record was created                |
| updated_at     | TIMESTAMP      | DEFAULT NOW()              | When the record was last updated           |

### 4. articles

Stores scraped article content and metadata.

| Column Name      | Data Type      | Constraints                | Description                                |
|------------------|----------------|----------------------------|--------------------------------------------|
| id               | SERIAL         | PRIMARY KEY                | Unique identifier for the article          |
| title            | VARCHAR(512)   | NOT NULL                   | Title of the article                       |
| url              | VARCHAR(512)   | NOT NULL, UNIQUE           | URL of the article                         |
| content          | TEXT           |                            | Content of the article                     |
| content_markdown | TEXT           |                            | Markdown content of the article            |
| content_html     | TEXT           |                            | HTML content of the article                |
| author           | VARCHAR(255)   |                            | Author of the article                      |
| published_at     | TIMESTAMP      |                            | Publication date of the article            |
| image_url        | VARCHAR(512)   |                            | URL of the article image                   |
| website_id       | INTEGER        | FOREIGN KEY (websites.id)  | Reference to the website                   |
| metadata         | JSON           |                            | Metadata of the article                    |
| active           | BOOLEAN        | DEFAULT TRUE               | Whether the article is active              |
| created_at       | TIMESTAMP      | DEFAULT NOW()              | When the record was created                |
| updated_at       | TIMESTAMP      | DEFAULT NOW()              | When the record was last updated           |

### 5. scraping_errors

Stores error information for debugging and monitoring.

| Column Name      | Data Type      | Constraints                | Description                                |
|------------------|----------------|----------------------------|--------------------------------------------|
| id               | SERIAL         | PRIMARY KEY                | Unique identifier for the error log        |
| job_id           | INTEGER        | FOREIGN KEY (scraping_jobs.id) | Reference to the scraping job           |
| url              | VARCHAR(512)   |                            | URL that caused the error                  |
| error_type       | VARCHAR(255)   | NOT NULL                   | Type of error                              |
| error_message    | TEXT           | NOT NULL                   | Error message                              |
| stack_trace      | TEXT           |                            | Stack trace of the error                   |
| created_at       | TIMESTAMP      | DEFAULT NOW()              | When the error occurred                    |

### 6. article_categories

Stores relationships between articles and categories.

| Column Name      | Data Type      | Constraints                | Description                                |
|------------------|----------------|----------------------------|--------------------------------------------|
| article_id      | INTEGER        | PRIMARY KEY, FOREIGN KEY (articles.id) | Reference to the article                   |
| category_id     | INTEGER        | PRIMARY KEY, FOREIGN KEY (categories.id) | Reference to the category               |

## SQL Creation Scripts

```sql
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

-- Create articles table
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    url VARCHAR(512) NOT NULL UNIQUE,
    content TEXT,
    content_markdown TEXT,
    content_html TEXT,
    author VARCHAR(255),
    published_at TIMESTAMP,
    image_url VARCHAR(512),
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    metadata JSONB,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
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
CREATE INDEX idx_scraping_jobs_website_id ON scraping_jobs(website_id);
CREATE INDEX idx_scraping_jobs_status ON scraping_jobs(status);
CREATE INDEX idx_scraping_errors_job_id ON scraping_errors(job_id);
CREATE INDEX idx_scraping_errors_error_type ON scraping_errors(error_type);
```

## Database Migration Strategy

### Initial Setup

1. Create the database:
   ```sql
   CREATE DATABASE naija_news;
   ```

2. Run the SQL creation scripts to set up the initial schema.

### Schema Updates

When updating the schema:

1. Create a migration script that:
   - Adds new tables/columns
   - Modifies existing tables/columns
   - Preserves existing data

2. Test the migration script in a development environment.

3. Apply the migration script to the production database.

4. Update the schema documentation to reflect the changes.

### Example Migration Script

```sql
-- Example migration to add a new column to articles
ALTER TABLE articles ADD COLUMN content_hash VARCHAR(64);

-- Example migration to create a new index
CREATE INDEX idx_articles_content_hash ON articles(content_hash);

-- Example migration to add a new table
CREATE TABLE article_views (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id) ON DELETE CASCADE,
    view_count INTEGER DEFAULT 0,
    last_viewed TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Data Backup and Recovery

### Backup Strategy

1. **Regular Backups**: Schedule daily backups of the database.
   ```bash
   pg_dump -U username -d naija_news > naija_news_$(date +%Y%m%d).sql
   ```

2. **Incremental Backups**: Consider using WAL archiving for point-in-time recovery.

3. **Backup Rotation**: Keep daily backups for a week, weekly backups for a month, and monthly backups for a year.

### Recovery Procedure

1. Create a new database if needed:
   ```sql
   CREATE DATABASE naija_news_recovery;
   ```

2. Restore from backup:
   ```bash
   psql -U username -d naija_news_recovery < naija_news_backup.sql
   ```

## Performance Considerations

### Indexing Strategy

The schema includes indexes on:
- Foreign keys for efficient joins
- Frequently queried columns
- Columns used in WHERE clauses

### Query Optimization

1. Use prepared statements for frequently executed queries.
2. Use EXPLAIN ANALYZE to identify slow queries.
3. Consider partitioning large tables (e.g., articles_data) by website_id or date.

### Connection Pooling

Configure connection pooling to efficiently manage database connections:
- Set appropriate pool size based on workload
- Configure connection timeout and max lifetime
- Monitor connection usage

## Security Considerations

### Access Control

1. Create a dedicated database user for the application with limited privileges:
   ```sql
   CREATE USER naija_news_app WITH PASSWORD 'secure_password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO naija_news_app;
   ```

2. Use different users for different environments (development, testing, production).

### Data Protection

1. Store sensitive configuration (database credentials) in environment variables.
2. Consider encrypting sensitive data columns if needed.
3. Implement proper input validation to prevent SQL injection.

## Monitoring and Maintenance

### Regular Maintenance Tasks

1. **Vacuum and Analyze**: Schedule regular VACUUM and ANALYZE operations to maintain performance.
   ```sql
   VACUUM ANALYZE;
   ```

2. **Index Maintenance**: Rebuild indexes periodically to reduce fragmentation.
   ```sql
   REINDEX TABLE articles_data;
   ```

3. **Statistics Update**: Update statistics for the query planner.
   ```sql
   ANALYZE;
   ```

### Monitoring Queries

1. **Table Size**:
   ```sql
   SELECT pg_size_pretty(pg_total_relation_size('articles')) AS articles_size;
   ```

2. **Index Usage**:
   ```sql
   SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
   FROM pg_stat_user_indexes
   WHERE schemaname = 'public'
   ORDER BY idx_scan DESC;
   ```

3. **Slow Queries**:
   ```sql
   SELECT query, calls, total_time, mean_time
   FROM pg_stat_statements
   ORDER BY mean_time DESC
   LIMIT 10;
   ```
