# Naija News Hub - Database Schema Documentation

This document provides a comprehensive overview of the database schema for the Naija News Hub project, including table definitions, relationships, and SQL creation scripts.

## Entity-Relationship Diagram

```
+----------------+       +----------------+       +----------------+
|    websites    |       |    sitemaps    |       |   categories   |
+----------------+       +----------------+       +----------------+
| id             |<----->| website_id     |       | id             |
| website_name   |       | article_url    |       | website_id     |<----+
| website_url    |       | last_mod       |       | category_name  |     |
| sitemap_index  |       | created_at     |       | category_url   |     |
| first_archive  |       | is_valid       |       | created_at     |     |
| last_archive   |       | last_checked   |       | is_valid       |     |
| created_at     |       | status_code    |       | last_checked   |     |
| updated_at     |       | retry_count    |       +----------------+     |
+----------------+       | last_error     |                              |
        ^                +----------------+                              |
        |                                                                |
        |                +----------------+                              |
        |                | progress_track |                              |
        +--------------->| website_id     |                              |
        |                | cat_scrape_st  |                              |
        |                | site_scrape_st |                              |
        |                | art_scrape_st  |                              |
        |                | current_step   |                              |
        |                | last_checked   |                              |
        |                | new_discovered |                              |
        |                | new_added      |                              |
        |                | last_added     |                              |
        |                | check_status   |                              |
        |                | checkpoint     |                              |
        |                +----------------+                              |
        |                                                                |
        |                +----------------+                              |
        |                |  error_logs    |                              |
        +--------------->| website_id     |                              |
        |                | error_message  |                              |
        |                | error_type     |                              |
        |                | created_at     |                              |
        |                | resolved_at    |                              |
        |                | resolution     |                              |
        |                | retry_count    |                              |
        |                +----------------+                              |
        |                                                                |
        |                +----------------+                              |
        |                | articles_data  |                              |
        +--------------->| website_id     |                              |
                         | article_id     |                              |
                         | article_title  |                              |
                         | article_cat    |<----------------------------+
                         | author         |
                         | article_url    |
                         | pub_date       |
                         | created_at     |
                         | article_content|
                         | scraping_status|
                         | retry_count    |
                         | last_error     |
                         +----------------+
```

## Table Definitions

### 1. websites

Stores information about news websites being scraped.

| Column Name       | Data Type      | Constraints       | Description                                |
|-------------------|----------------|-------------------|--------------------------------------------|
| id                | SERIAL         | PRIMARY KEY       | Unique identifier for the website          |
| website_name      | VARCHAR(255)   | NOT NULL          | Name of the website                        |
| website_url       | VARCHAR(255)   | NOT NULL, UNIQUE  | Base URL of the website                    |
| sitemap_index_url | VARCHAR(255)   |                   | URL of the sitemap index                   |
| first_archive_url | VARCHAR(255)   |                   | URL of the first archive page              |
| last_archive_url  | VARCHAR(255)   |                   | URL of the last archive page               |
| created_at        | TIMESTAMP      | DEFAULT NOW()     | When the record was created                |
| updated_at        | TIMESTAMP      |                   | When the record was last updated           |

### 2. sitemaps

Stores article URLs extracted from website sitemaps.

| Column Name    | Data Type      | Constraints                | Description                                |
|----------------|----------------|----------------------------|--------------------------------------------|
| id             | SERIAL         | PRIMARY KEY                | Unique identifier for the sitemap entry    |
| website_id     | INTEGER        | FOREIGN KEY (websites.id)  | Reference to the website                   |
| article_url    | VARCHAR(1024)  | NOT NULL, UNIQUE           | URL of the article                         |
| last_mod       | TIMESTAMP      |                            | Last modification date from sitemap        |
| created_at     | TIMESTAMP      | DEFAULT NOW()              | When the record was created                |
| is_valid       | BOOLEAN        |                            | Whether the URL is valid                   |
| last_checked   | TIMESTAMP      |                            | When the URL was last checked              |
| status_code    | INTEGER        |                            | HTTP status code of the URL                |
| retry_count    | INTEGER        | DEFAULT 0                  | Number of retry attempts                   |
| last_error     | TEXT           |                            | Last error message                         |

### 3. categories

Stores category information for news websites.

| Column Name    | Data Type      | Constraints                | Description                                |
|----------------|----------------|----------------------------|--------------------------------------------|
| id             | SERIAL         | PRIMARY KEY                | Unique identifier for the category         |
| website_id     | INTEGER        | FOREIGN KEY (websites.id)  | Reference to the website                   |
| category_name  | VARCHAR(255)   | NOT NULL                   | Name of the category                       |
| category_url   | VARCHAR(1024)  | NOT NULL                   | URL of the category page                   |
| created_at     | TIMESTAMP      | DEFAULT NOW()              | When the record was created                |
| is_valid       | BOOLEAN        |                            | Whether the category URL is valid          |
| last_checked   | TIMESTAMP      |                            | When the category was last checked         |

### 4. articles_data

Stores scraped article content and metadata.

| Column Name      | Data Type      | Constraints                | Description                                |
|------------------|----------------|----------------------------|--------------------------------------------|
| id               | SERIAL         | PRIMARY KEY                | Unique identifier for the article data     |
| website_id       | INTEGER        | FOREIGN KEY (websites.id)  | Reference to the website                   |
| article_id       | VARCHAR(255)   | NOT NULL, UNIQUE           | Unique identifier for the article          |
| article_title    | TEXT           | NOT NULL                   | Title of the article                       |
| article_category | INTEGER        | FOREIGN KEY (categories.id)| Reference to the category                  |
| author           | TEXT           |                            | Author of the article                      |
| article_url      | TEXT           | NOT NULL                   | URL of the article                         |
| pub_date         | TIMESTAMP      |                            | Publication date of the article            |
| created_at       | TIMESTAMP      | DEFAULT NOW()              | When the record was created                |
| article_content  | TEXT           |                            | Content of the article                     |
| scraping_status  | VARCHAR(50)    | DEFAULT 'pending'          | Status of scraping (pending/success/failed)|
| retry_count      | INTEGER        | DEFAULT 0                  | Number of retry attempts                   |
| last_error       | TEXT           |                            | Last error message                         |

### 5. error_logs

Stores error information for debugging and monitoring.

| Column Name      | Data Type      | Constraints                | Description                                |
|------------------|----------------|----------------------------|--------------------------------------------|
| id               | SERIAL         | PRIMARY KEY                | Unique identifier for the error log        |
| website_id       | INTEGER        | FOREIGN KEY (websites.id)  | Reference to the website                   |
| error_message    | TEXT           | NOT NULL                   | Error message                              |
| error_type       | VARCHAR(100)   | NOT NULL                   | Type of error                              |
| created_at       | TIMESTAMP      | DEFAULT NOW()              | When the error occurred                    |
| resolved_at      | TIMESTAMP      |                            | When the error was resolved                |
| resolution_notes | TEXT           |                            | Notes on how the error was resolved        |
| retry_count      | INTEGER        | DEFAULT 0                  | Number of retry attempts                   |

### 6. progress_tracking

Tracks the progress of scraping operations.

| Column Name                | Data Type      | Constraints                | Description                                |
|----------------------------|----------------|----------------------------|--------------------------------------------|
| id                         | SERIAL         | PRIMARY KEY                | Unique identifier for the progress record  |
| website_id                 | INTEGER        | FOREIGN KEY (websites.id)  | Reference to the website                   |
| category_scraping_status   | BOOLEAN        | DEFAULT FALSE              | Whether category scraping is complete      |
| sitemap_scraping_status    | BOOLEAN        | DEFAULT FALSE              | Whether sitemap scraping is complete       |
| articles_scraping_status   | BOOLEAN        | DEFAULT FALSE              | Whether article scraping is complete       |
| current_step               | INTEGER        | DEFAULT 0                  | Current step in the scraping process       |
| last_checked               | TIMESTAMP      |                            | When the progress was last checked         |
| new_articles_discovered    | INTEGER        | DEFAULT 0                  | Number of new articles discovered          |
| new_articles_added         | INTEGER        | DEFAULT 0                  | Number of new articles added               |
| last_article_added         | TIMESTAMP      |                            | When the last article was added            |
| last_check_status          | VARCHAR(100)   |                            | Status of the last check                   |
| checkpoint_data            | JSONB          |                            | Checkpoint data for resuming operations    |

## SQL Creation Scripts

```sql
-- Create websites table
CREATE TABLE websites (
    id SERIAL PRIMARY KEY,
    website_name VARCHAR(255) NOT NULL,
    website_url VARCHAR(255) NOT NULL UNIQUE,
    sitemap_index_url VARCHAR(255),
    first_archive_url VARCHAR(255),
    last_archive_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- Create sitemaps table
CREATE TABLE sitemaps (
    id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    article_url VARCHAR(1024) NOT NULL UNIQUE,
    last_mod TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    is_valid BOOLEAN,
    last_checked TIMESTAMP,
    status_code INTEGER,
    retry_count INTEGER DEFAULT 0,
    last_error TEXT
);

-- Create categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    category_name VARCHAR(255) NOT NULL,
    category_url VARCHAR(1024) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_valid BOOLEAN,
    last_checked TIMESTAMP,
    UNIQUE(website_id, category_name)
);

-- Create articles_data table
CREATE TABLE articles_data (
    id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    article_id VARCHAR(255) NOT NULL UNIQUE,
    article_title TEXT NOT NULL,
    article_category INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    author TEXT,
    article_url TEXT NOT NULL,
    pub_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    article_content TEXT,
    scraping_status VARCHAR(50) DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    last_error TEXT
);

-- Create error_logs table
CREATE TABLE error_logs (
    id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    error_message TEXT NOT NULL,
    error_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    retry_count INTEGER DEFAULT 0
);

-- Create progress_tracking table
CREATE TABLE progress_tracking (
    id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE UNIQUE,
    category_scraping_status BOOLEAN DEFAULT FALSE,
    sitemap_scraping_status BOOLEAN DEFAULT FALSE,
    articles_scraping_status BOOLEAN DEFAULT FALSE,
    current_step INTEGER DEFAULT 0,
    last_checked TIMESTAMP,
    new_articles_discovered INTEGER DEFAULT 0,
    new_articles_added INTEGER DEFAULT 0,
    last_article_added TIMESTAMP,
    last_check_status VARCHAR(100),
    checkpoint_data JSONB
);

-- Create indexes for performance
CREATE INDEX idx_sitemaps_website_id ON sitemaps(website_id);
CREATE INDEX idx_categories_website_id ON categories(website_id);
CREATE INDEX idx_articles_data_website_id ON articles_data(website_id);
CREATE INDEX idx_articles_data_category ON articles_data(article_category);
CREATE INDEX idx_error_logs_website_id ON error_logs(website_id);
CREATE INDEX idx_error_logs_error_type ON error_logs(error_type);
CREATE INDEX idx_articles_data_scraping_status ON articles_data(scraping_status);
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
-- Example migration to add a new column to articles_data
ALTER TABLE articles_data ADD COLUMN content_hash VARCHAR(64);

-- Example migration to create a new index
CREATE INDEX idx_articles_data_pub_date ON articles_data(pub_date);
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
   SELECT pg_size_pretty(pg_total_relation_size('articles_data')) AS articles_data_size;
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
