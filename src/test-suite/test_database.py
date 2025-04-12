"""
Tests for the database module.

This module provides tests for the database functionality.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.models import Base, Website, Article, Category, ArticleCategory, ScrapingJob

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Fixture for database session."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

def test_create_website(db_session):
    """Test creating a website."""
    website = Website(
        name="Test Website",
        base_url="https://example.com",
        description="A test website",
        active=True,
    )
    db_session.add(website)
    db_session.commit()
    
    # Check that the website was created
    db_website = db_session.query(Website).filter(Website.name == "Test Website").first()
    assert db_website is not None
    assert db_website.name == "Test Website"
    assert db_website.base_url == "https://example.com"
    assert db_website.description == "A test website"
    assert db_website.active is True

def test_create_category(db_session):
    """Test creating a category."""
    # First, create a website
    website = Website(
        name="Test Website",
        base_url="https://example.com",
        description="A test website",
        active=True,
    )
    db_session.add(website)
    db_session.commit()
    
    # Then, create a category
    category = Category(
        name="Test Category",
        url="https://example.com/category/test",
        website_id=website.id,
        active=True,
    )
    db_session.add(category)
    db_session.commit()
    
    # Check that the category was created
    db_category = db_session.query(Category).filter(Category.name == "Test Category").first()
    assert db_category is not None
    assert db_category.name == "Test Category"
    assert db_category.url == "https://example.com/category/test"
    assert db_category.website_id == website.id
    assert db_category.active is True

def test_create_article(db_session):
    """Test creating an article."""
    # First, create a website
    website = Website(
        name="Test Website",
        base_url="https://example.com",
        description="A test website",
        active=True,
    )
    db_session.add(website)
    db_session.commit()
    
    # Then, create an article
    article = Article(
        title="Test Article",
        url="https://example.com/article/test",
        content="This is a test article.",
        content_markdown="# Test Article\n\nThis is a test article.",
        content_html="<h1>Test Article</h1><p>This is a test article.</p>",
        author="Test Author",
        website_id=website.id,
        active=True,
    )
    db_session.add(article)
    db_session.commit()
    
    # Check that the article was created
    db_article = db_session.query(Article).filter(Article.title == "Test Article").first()
    assert db_article is not None
    assert db_article.title == "Test Article"
    assert db_article.url == "https://example.com/article/test"
    assert db_article.content == "This is a test article."
    assert db_article.author == "Test Author"
    assert db_article.website_id == website.id
    assert db_article.active is True

def test_article_category_relationship(db_session):
    """Test the relationship between articles and categories."""
    # First, create a website
    website = Website(
        name="Test Website",
        base_url="https://example.com",
        description="A test website",
        active=True,
    )
    db_session.add(website)
    db_session.commit()
    
    # Then, create a category
    category = Category(
        name="Test Category",
        url="https://example.com/category/test",
        website_id=website.id,
        active=True,
    )
    db_session.add(category)
    db_session.commit()
    
    # Then, create an article
    article = Article(
        title="Test Article",
        url="https://example.com/article/test",
        content="This is a test article.",
        website_id=website.id,
        active=True,
    )
    db_session.add(article)
    db_session.commit()
    
    # Finally, create the relationship
    article_category = ArticleCategory(
        article_id=article.id,
        category_id=category.id,
    )
    db_session.add(article_category)
    db_session.commit()
    
    # Check that the relationship was created
    db_article = db_session.query(Article).filter(Article.title == "Test Article").first()
    assert db_article is not None
    assert len(db_article.categories) == 1
    assert db_article.categories[0].category_id == category.id
    
    db_category = db_session.query(Category).filter(Category.name == "Test Category").first()
    assert db_category is not None
    assert len(db_category.articles) == 1
    assert db_category.articles[0].article_id == article.id
