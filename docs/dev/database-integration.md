# Database Integration Documentation

**Last Updated:** April 13, 2025

## Overview

This document describes the database integration implementation for the Naija News Hub project. The integration allows for storing and retrieving articles, websites, categories, and scraping job information from the PostgreSQL database.

## Architecture

The database integration follows a repository pattern with a service layer:

1. **Repository Layer**: Provides data access methods for each entity
2. **Service Layer**: Implements business logic and coordinates between repositories
3. **Models**: Defines SQLAlchemy ORM models for database tables

```
+----------------+       +----------------+       +----------------+
|    Services    |------>|  Repositories  |------>|     Models     |
+----------------+       +----------------+       +----------------+
        |                        |                        |
        v                        v                        v
+----------------+       +----------------+       +----------------+
|  Business Logic|       |  Data Access   |       |  Database Schema|
+----------------+       +----------------+       +----------------+
```

## Repository Classes

### ArticleRepository

Handles operations related to articles:

- Creating and updating articles
- Retrieving articles by ID, URL, website, or category
- Managing article categories
- Searching articles
- Batch operations for article creation

```python
# Key methods
def create_article(self, article_data: Dict[str, Any]) -> Article
def get_article_by_id(self, article_id: int) -> Optional[Article]
def get_article_by_url(self, url: str) -> Optional[Article]
def get_articles_by_website(self, website_id: int, limit: int = 100, offset: int = 0) -> List[Article]
def update_article(self, article_id: int, article_data: Dict[str, Any]) -> Optional[Article]
def add_article_category(self, article_id: int, category_id: int) -> bool
def search_articles(self, query: str, limit: int = 100, offset: int = 0) -> List[Article]
def batch_create_articles(self, articles_data: List[Dict[str, Any]]) -> List[Article]
```

### WebsiteRepository

Handles operations related to websites and categories:

- Creating and updating websites
- Retrieving websites by ID or URL
- Managing website categories
- Listing active websites

```python
# Key methods
def create_website(self, website_data: Dict[str, Any]) -> Website
def get_website_by_id(self, website_id: int) -> Optional[Website]
def get_website_by_url(self, base_url: str) -> Optional[Website]
def get_all_websites(self, active_only: bool = True) -> List[Website]
def create_category(self, website_id: int, category_data: Dict[str, Any]) -> Category
def get_website_categories(self, website_id: int, active_only: bool = True) -> List[Category]
```

### ScrapingRepository

Handles operations related to scraping jobs and errors:

- Creating and updating scraping jobs
- Tracking job status (pending, running, completed, failed)
- Recording scraping errors
- Generating job statistics

```python
# Key methods
def create_job(self, job_data: Dict[str, Any]) -> ScrapingJob
def start_job(self, job_id: int) -> Optional[ScrapingJob]
def complete_job(self, job_id: int, articles_found: int, articles_scraped: int) -> Optional[ScrapingJob]
def fail_job(self, job_id: int, error_message: str) -> Optional[ScrapingJob]
def create_error(self, error_data: Dict[str, Any]) -> ScrapingError
def get_job_stats(self, website_id: Optional[int] = None) -> Dict[str, Any]
```

## Service Layer

### ArticleService

Provides business logic for article operations:

- Extracting and storing articles
- Discovering and storing articles from websites
- Retrieving article statistics
- Managing article metadata

```python
# Key methods
async def extract_and_store_article(self, url: str, website_id: int) -> Optional[Dict[str, Any]]
async def discover_and_store_articles(self, website_id: int) -> Dict[str, Any]
async def extract_and_store_article_batch(self, urls: List[str], website_id: int) -> Dict[str, Any]
def get_article_stats(self, website_id: Optional[int] = None) -> Dict[str, Any]
def get_recent_articles(self, website_id: Optional[int] = None, limit: int = 10) -> List[Dict[str, Any]]
```

## Command-Line Interface

The database integration includes CLI commands for database operations:

```
python main.py db add-website --name "Website Name" --url "https://example.com" [options]
python main.py db list-websites
python main.py db extract-store --url "https://example.com/article" --website-id 1
python main.py db discover-store --website-id 1
python main.py db article-stats [--website-id 1]
python main.py db recent-articles [--website-id 1] [--limit 10]
```

## Configuration

The database integration uses the following configuration options:

```python
# Database configuration
database_config = DatabaseConfig(
    host=os.getenv("NAIJA_NEWS_DB_HOST", "localhost"),
    port=int(os.getenv("NAIJA_NEWS_DB_PORT", "5432")),
    database=db_name,
    user=os.getenv("NAIJA_NEWS_DB_USER", "postgres"),
    password=os.getenv("NAIJA_NEWS_DB_PASSWORD", ""),
)

# Scraper configuration
scraper_config = ScraperConfig(
    max_articles_per_run=int(os.getenv("NAIJA_NEWS_SCRAPER_MAX_ARTICLES", "10")),
    max_concurrent_requests=int(os.getenv("NAIJA_NEWS_SCRAPER_MAX_CONCURRENT", "5")),
    default_timeout=int(os.getenv("NAIJA_NEWS_SCRAPER_TIMEOUT", "30")),
    # Additional options...
)
```

## Error Handling

The database integration includes robust error handling:

1. **Transaction Management**: Uses SQLAlchemy's transaction management to ensure data consistency
2. **Exception Handling**: Catches and logs database exceptions
3. **Retry Mechanism**: Implements retry logic for transient errors
4. **Validation**: Validates data before insertion to prevent constraint violations

## Performance Considerations

1. **Batch Operations**: Uses batch inserts for efficient article storage
2. **Connection Pooling**: Configures connection pooling for efficient database connections
3. **Indexing**: Uses appropriate indexes for efficient queries
4. **Pagination**: Implements pagination for large result sets

## Usage Examples

### Adding a Website

```python
website_repo = WebsiteRepository(db)
website_data = {
    "name": "BBC News",
    "base_url": "https://www.bbc.com/news",
    "description": "BBC News website",
    "logo_url": "https://www.bbc.com/news/logo.png",
    "active": True
}
website = website_repo.create_website(website_data)
```

### Extracting and Storing an Article

```python
article_service = ArticleService(db)
result = await article_service.extract_and_store_article(
    "https://www.bbc.com/news/world-middle-east-67037548", 
    website_id=1
)
```

### Discovering and Storing Articles

```python
article_service = ArticleService(db)
result = await article_service.discover_and_store_articles(website_id=1)
```

## Future Improvements

1. **Caching**: Implement caching for frequently accessed data
2. **Full-Text Search**: Add full-text search capabilities for article content
3. **Content Versioning**: Implement versioning for article content
4. **Incremental Updates**: Add support for incremental updates to articles
5. **Data Compression**: Implement compression for large text fields
6. **Sharding**: Consider sharding for very large datasets

## Related Files

- `src/database/repositories/article_repository.py`: Article repository implementation
- `src/database/repositories/website_repository.py`: Website repository implementation
- `src/database/repositories/scraping_repository.py`: Scraping repository implementation
- `src/services/article_service.py`: Article service implementation
- `src/database/models.py`: SQLAlchemy ORM models
- `src/database/connection.py`: Database connection management
- `config/config.py`: Configuration management
- `main.py`: CLI commands for database operations

## References

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html)
