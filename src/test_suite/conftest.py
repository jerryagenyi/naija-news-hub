"""
Test fixtures for Naija News Hub.

This module provides test fixtures for the test suite.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta
from typing import Dict, Any, List

from src.database_management.models import Base, Website, Article, Category, ArticleCategory, ScrapingJob, ErrorLog
from src.database_management.repositories import ArticleRepository, WebsiteRepository, ScrapingRepository
from src.service_layer.article_service import ArticleService
from src.utility_modules.enums import ErrorType, ErrorSeverity

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fixture for database session."""
    # Create the tables
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

    # Drop the tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def article_repository(db_session):
    """Fixture for article repository."""
    return ArticleRepository(db_session)

@pytest.fixture
def website_repository(db_session):
    """Fixture for website repository."""
    return WebsiteRepository(db_session)

@pytest.fixture
def scraping_repository(db_session):
    """Fixture for scraping repository."""
    return ScrapingRepository(db_session)

@pytest.fixture
def article_service(db_session):
    """Fixture for article service."""
    return ArticleService(db_session)

@pytest.fixture
def sample_website(website_repository) -> Website:
    """Fixture for a sample website."""
    website_data = {
        "name": "Test Website",
        "base_url": "https://example.com",
        "description": "A test website",
        "logo_url": "https://example.com/logo.png",
        "sitemap_url": "https://example.com/sitemap.xml",
        "active": True
    }
    return website_repository.create_website(website_data)

@pytest.fixture
def sample_categories(website_repository, sample_website) -> List[Category]:
    """Fixture for sample categories."""
    categories = []
    for i in range(3):
        category_data = {
            "name": f"Category {i+1}",
            "url": f"https://example.com/category-{i+1}",
            "website_id": sample_website.id
        }
        categories.append(website_repository.create_category(sample_website.id, category_data))
    return categories

@pytest.fixture
def sample_article(article_repository, sample_website) -> Article:
    """Fixture for a sample article."""
    article_data = {
        "title": "Test Article",
        "url": "https://example.com/test-article",
        "content": "This is a test article content.",
        "content_markdown": "# Test Article\n\nThis is a test article content.",
        "content_html": "<h1>Test Article</h1><p>This is a test article content.</p>",
        "author": "Test Author",
        "published_at": datetime.utcnow() - timedelta(days=1),
        "image_url": "https://example.com/image.jpg",
        "website_id": sample_website.id,
        "article_metadata": {"word_count": 7, "reading_time": 1},
        "active": True
    }
    return article_repository.create_article(article_data)

@pytest.fixture
def sample_articles(article_repository, sample_website) -> List[Article]:
    """Fixture for sample articles."""
    articles = []
    for i in range(5):
        article_data = {
            "title": f"Test Article {i+1}",
            "url": f"https://example.com/test-article-{i+1}",
            "content": f"This is test article {i+1} content.",
            "content_markdown": f"# Test Article {i+1}\n\nThis is test article {i+1} content.",
            "content_html": f"<h1>Test Article {i+1}</h1><p>This is test article {i+1} content.</p>",
            "author": "Test Author",
            "published_at": datetime.utcnow() - timedelta(days=i),
            "image_url": f"https://example.com/image-{i+1}.jpg",
            "website_id": sample_website.id,
            "article_metadata": {"word_count": 7 + i, "reading_time": 1},
            "active": True
        }
        articles.append(article_repository.create_article(article_data))
    return articles

@pytest.fixture
def sample_article_with_categories(article_repository, sample_article, sample_categories) -> Article:
    """Fixture for a sample article with categories."""
    for category in sample_categories:
        article_repository.add_article_category(sample_article.id, category.id)
    return sample_article

@pytest.fixture
def sample_scraping_job(scraping_repository, sample_website) -> ScrapingJob:
    """Fixture for a sample scraping job."""
    job_data = {
        "website_id": sample_website.id,
        "status": "pending",
        "config": {
            "max_articles": 10,
            "max_concurrent": 5
        },
        "articles_found": 0,
        "articles_scraped": 0
    }
    return scraping_repository.create_job(job_data)

@pytest.fixture
def sample_error_log(scraping_repository, sample_scraping_job) -> ErrorLog:
    """Fixture for a sample error log."""
    error_data = {
        "job_id": sample_scraping_job.id,
        "error_type": ErrorType.NETWORK,  # Use enum value
        "severity": ErrorSeverity.MEDIUM,  # Use enum value
        "error_message": "Connection timeout",
        "url": "https://example.com/test-article",
        "context": "Trying to fetch article content",
        "stack_trace": "Traceback...",
    }
    return scraping_repository.create_error(error_data)
