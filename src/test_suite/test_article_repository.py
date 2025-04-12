"""
Tests for the ArticleRepository class.

This module provides tests for the ArticleRepository class.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from src.database_management.models import Article, Category
from src.database_management.repositories.article_repository import ArticleRepository

class TestArticleRepository:
    """Test cases for ArticleRepository."""

    def test_create_article(self, article_repository, sample_website):
        """Test creating an article."""
        # Prepare test data
        article_data = {
            "title": "New Test Article",
            "url": "https://example.com/new-test-article",
            "content": "This is a new test article content.",
            "content_markdown": "# New Test Article\n\nThis is a new test article content.",
            "content_html": "<h1>New Test Article</h1><p>This is a new test article content.</p>",
            "author": "Test Author",
            "published_at": datetime.utcnow(),
            "image_url": "https://example.com/new-image.jpg",
            "website_id": sample_website.id,
            "article_metadata": {"word_count": 8, "reading_time": 1},
            "active": True
        }
        
        # Create article
        article = article_repository.create_article(article_data)
        
        # Verify article was created
        assert article.id is not None
        assert article.title == "New Test Article"
        assert article.url == "https://example.com/new-test-article"
        assert article.content == "This is a new test article content."
        assert article.website_id == sample_website.id
        assert article.article_metadata["word_count"] == 8
        
    def test_create_article_duplicate_url(self, article_repository, sample_article):
        """Test creating an article with a duplicate URL."""
        # Prepare test data with the same URL as sample_article
        article_data = {
            "title": "Duplicate URL Article",
            "url": sample_article.url,  # Same URL as sample_article
            "content": "This is a duplicate URL article content.",
            "website_id": sample_article.website_id,
        }
        
        # Attempt to create article with duplicate URL should raise IntegrityError
        with pytest.raises(IntegrityError):
            article_repository.create_article(article_data)
    
    def test_get_article_by_id(self, article_repository, sample_article):
        """Test getting an article by ID."""
        # Get article by ID
        article = article_repository.get_article_by_id(sample_article.id)
        
        # Verify article was retrieved
        assert article is not None
        assert article.id == sample_article.id
        assert article.title == sample_article.title
        assert article.url == sample_article.url
        
    def test_get_article_by_id_not_found(self, article_repository):
        """Test getting an article by ID that doesn't exist."""
        # Get article by non-existent ID
        article = article_repository.get_article_by_id(999)
        
        # Verify article was not found
        assert article is None
        
    def test_get_article_by_url(self, article_repository, sample_article):
        """Test getting an article by URL."""
        # Get article by URL
        article = article_repository.get_article_by_url(sample_article.url)
        
        # Verify article was retrieved
        assert article is not None
        assert article.id == sample_article.id
        assert article.title == sample_article.title
        assert article.url == sample_article.url
        
    def test_get_article_by_url_not_found(self, article_repository):
        """Test getting an article by URL that doesn't exist."""
        # Get article by non-existent URL
        article = article_repository.get_article_by_url("https://example.com/non-existent")
        
        # Verify article was not found
        assert article is None
        
    def test_get_articles_by_website(self, article_repository, sample_articles, sample_website):
        """Test getting articles by website ID."""
        # Get articles by website ID
        articles = article_repository.get_articles_by_website(sample_website.id)
        
        # Verify articles were retrieved
        assert len(articles) == len(sample_articles)
        
        # Verify articles are ordered by published_at desc
        for i in range(len(articles) - 1):
            assert articles[i].published_at >= articles[i + 1].published_at
            
    def test_get_articles_by_website_with_limit(self, article_repository, sample_articles, sample_website):
        """Test getting articles by website ID with limit."""
        # Get articles by website ID with limit
        limit = 2
        articles = article_repository.get_articles_by_website(sample_website.id, limit=limit)
        
        # Verify articles were retrieved with limit
        assert len(articles) == limit
        
    def test_get_articles_by_website_with_offset(self, article_repository, sample_articles, sample_website):
        """Test getting articles by website ID with offset."""
        # Get all articles first to compare
        all_articles = article_repository.get_articles_by_website(sample_website.id)
        
        # Get articles by website ID with offset
        offset = 2
        articles = article_repository.get_articles_by_website(sample_website.id, offset=offset)
        
        # Verify articles were retrieved with offset
        assert len(articles) == len(all_articles) - offset
        assert articles[0].id == all_articles[offset].id
        
    def test_update_article(self, article_repository, sample_article):
        """Test updating an article."""
        # Prepare update data
        update_data = {
            "title": "Updated Test Article",
            "content": "This is an updated test article content.",
            "author": "Updated Author"
        }
        
        # Update article
        updated_article = article_repository.update_article(sample_article.id, update_data)
        
        # Verify article was updated
        assert updated_article is not None
        assert updated_article.id == sample_article.id
        assert updated_article.title == "Updated Test Article"
        assert updated_article.content == "This is an updated test article content."
        assert updated_article.author == "Updated Author"
        assert updated_article.url == sample_article.url  # URL should not change
        
    def test_update_article_not_found(self, article_repository):
        """Test updating an article that doesn't exist."""
        # Prepare update data
        update_data = {
            "title": "Updated Test Article",
            "content": "This is an updated test article content."
        }
        
        # Update non-existent article
        updated_article = article_repository.update_article(999, update_data)
        
        # Verify article was not found
        assert updated_article is None
        
    def test_delete_article(self, article_repository, sample_article):
        """Test deleting an article."""
        # Delete article
        result = article_repository.delete_article(sample_article.id)
        
        # Verify article was deleted
        assert result is True
        assert article_repository.get_article_by_id(sample_article.id) is None
        
    def test_delete_article_not_found(self, article_repository):
        """Test deleting an article that doesn't exist."""
        # Delete non-existent article
        result = article_repository.delete_article(999)
        
        # Verify article was not found
        assert result is False
        
    def test_add_article_category(self, article_repository, sample_article, sample_categories):
        """Test adding a category to an article."""
        # Add category to article
        result = article_repository.add_article_category(sample_article.id, sample_categories[0].id)
        
        # Verify category was added
        assert result is True
        
        # Get categories for article
        categories = article_repository.get_article_categories(sample_article.id)
        
        # Verify category is in the list
        assert len(categories) == 1
        assert categories[0].id == sample_categories[0].id
        
    def test_add_article_category_already_exists(self, article_repository, sample_article_with_categories):
        """Test adding a category to an article that already has the category."""
        # Get categories for article
        categories = article_repository.get_article_categories(sample_article_with_categories.id)
        
        # Add the first category again
        result = article_repository.add_article_category(sample_article_with_categories.id, categories[0].id)
        
        # Verify category was not added (already exists)
        assert result is False
        
        # Get categories for article again
        categories_after = article_repository.get_article_categories(sample_article_with_categories.id)
        
        # Verify categories count didn't change
        assert len(categories_after) == len(categories)
        
    def test_remove_article_category(self, article_repository, sample_article_with_categories):
        """Test removing a category from an article."""
        # Get categories for article
        categories = article_repository.get_article_categories(sample_article_with_categories.id)
        
        # Remove the first category
        result = article_repository.remove_article_category(sample_article_with_categories.id, categories[0].id)
        
        # Verify category was removed
        assert result is True
        
        # Get categories for article again
        categories_after = article_repository.get_article_categories(sample_article_with_categories.id)
        
        # Verify categories count decreased
        assert len(categories_after) == len(categories) - 1
        
    def test_remove_article_category_not_found(self, article_repository, sample_article):
        """Test removing a category from an article that doesn't have the category."""
        # Remove non-existent category
        result = article_repository.remove_article_category(sample_article.id, 999)
        
        # Verify category was not found
        assert result is False
        
    def test_get_article_categories(self, article_repository, sample_article_with_categories):
        """Test getting categories for an article."""
        # Get categories for article
        categories = article_repository.get_article_categories(sample_article_with_categories.id)
        
        # Verify categories were retrieved
        assert len(categories) == 3
        
    def test_get_articles_by_category(self, article_repository, sample_article_with_categories, sample_categories):
        """Test getting articles by category ID."""
        # Get articles by category ID
        articles = article_repository.get_articles_by_category(sample_categories[0].id)
        
        # Verify articles were retrieved
        assert len(articles) == 1
        assert articles[0].id == sample_article_with_categories.id
        
    def test_search_articles(self, article_repository, sample_articles):
        """Test searching articles."""
        # Search for articles containing "test"
        articles = article_repository.search_articles("test")
        
        # Verify articles were retrieved
        assert len(articles) == len(sample_articles)
        
        # Search for articles containing "article 1"
        articles = article_repository.search_articles("article 1")
        
        # Verify only articles with "article 1" were retrieved
        assert len(articles) == 1
        assert "article 1" in articles[0].title.lower() or "article 1" in articles[0].content.lower()
        
    def test_get_articles_count(self, article_repository, sample_articles, sample_website):
        """Test getting the count of articles."""
        # Get count of all articles
        count = article_repository.get_articles_count()
        
        # Verify count is correct
        assert count == len(sample_articles)
        
        # Get count of articles for a specific website
        count = article_repository.get_articles_count(sample_website.id)
        
        # Verify count is correct
        assert count == len(sample_articles)
        
    def test_get_latest_article_date(self, article_repository, sample_articles, sample_website):
        """Test getting the date of the latest article."""
        # Get latest article date
        latest_date = article_repository.get_latest_article_date(sample_website.id)
        
        # Verify latest date is correct (should be the most recent published_at date)
        assert latest_date is not None
        
        # Get the most recent published_at date from sample_articles
        most_recent_date = max(article.published_at for article in sample_articles)
        
        # Verify latest date matches most recent date
        assert latest_date == most_recent_date
        
    def test_create_or_update_article_create(self, article_repository, sample_website):
        """Test creating an article with create_or_update_article."""
        # Prepare test data
        article_data = {
            "title": "New Test Article",
            "url": "https://example.com/new-test-article",
            "content": "This is a new test article content.",
            "website_id": sample_website.id,
        }
        
        # Create article
        article = article_repository.create_or_update_article(article_data)
        
        # Verify article was created
        assert article.id is not None
        assert article.title == "New Test Article"
        assert article.url == "https://example.com/new-test-article"
        
    def test_create_or_update_article_update(self, article_repository, sample_article):
        """Test updating an article with create_or_update_article."""
        # Prepare update data
        update_data = {
            "title": "Updated Test Article",
            "url": sample_article.url,  # Same URL as sample_article
            "content": "This is an updated test article content.",
            "website_id": sample_article.website_id,
        }
        
        # Update article
        article = article_repository.create_or_update_article(update_data)
        
        # Verify article was updated
        assert article.id == sample_article.id
        assert article.title == "Updated Test Article"
        assert article.content == "This is an updated test article content."
        
    def test_batch_create_articles(self, article_repository, sample_website):
        """Test creating multiple articles in a batch."""
        # Prepare test data
        articles_data = []
        for i in range(3):
            article_data = {
                "title": f"Batch Article {i+1}",
                "url": f"https://example.com/batch-article-{i+1}",
                "content": f"This is batch article {i+1} content.",
                "website_id": sample_website.id,
            }
            articles_data.append(article_data)
        
        # Create articles in batch
        articles = article_repository.batch_create_articles(articles_data)
        
        # Verify articles were created
        assert len(articles) == 3
        for i, article in enumerate(articles):
            assert article.id is not None
            assert article.title == f"Batch Article {i+1}"
            assert article.url == f"https://example.com/batch-article-{i+1}"
