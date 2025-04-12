"""
Unit tests for article update functionality.
"""

import unittest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.database_management.models import Article, Website
from src.service_layer.article_service import ArticleService
from src.utility_modules.article_comparison import (
    should_update_article,
    has_significant_content_changes,
    has_metadata_changes,
    merge_article_data,
    get_article_changes_summary
)


class TestArticleComparison(unittest.TestCase):
    """Test cases for article comparison functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock article
        self.existing_article = MagicMock(spec=Article)
        self.existing_article.id = 1
        self.existing_article.title = "Test Article"
        self.existing_article.url = "https://example.com/test-article"
        self.existing_article.content = "This is a test article content."
        self.existing_article.content_markdown = "# Test Article\n\nThis is a test article content."
        self.existing_article.content_html = "<h1>Test Article</h1><p>This is a test article content.</p>"
        self.existing_article.author = "Test Author"
        self.existing_article.published_at = datetime.utcnow() - timedelta(days=1)
        self.existing_article.image_url = "https://example.com/image.jpg"
        self.existing_article.website_id = 1
        self.existing_article.article_metadata = {"word_count": 7, "reading_time": 1}
        self.existing_article.active = True
        self.existing_article.created_at = datetime.utcnow() - timedelta(days=1)
        self.existing_article.updated_at = datetime.utcnow() - timedelta(days=1)
        self.existing_article.last_checked_at = datetime.utcnow() - timedelta(days=1)
        self.existing_article.update_count = 0

        # Create new article data
        self.new_article_data = {
            "title": "Test Article Updated",
            "url": "https://example.com/test-article",
            "content": "This is a test article content with some updates.",
            "content_markdown": "# Test Article Updated\n\nThis is a test article content with some updates.",
            "content_html": "<h1>Test Article Updated</h1><p>This is a test article content with some updates.</p>",
            "author": "Test Author",
            "published_at": datetime.utcnow(),
            "image_url": "https://example.com/image.jpg",
            "website_id": 1,
            "article_metadata": {"word_count": 9, "reading_time": 1},
            "active": True,
            "last_checked_at": datetime.utcnow()
        }

        # Create unchanged article data
        self.unchanged_article_data = {
            "title": "Test Article",
            "url": "https://example.com/test-article",
            "content": "This is a test article content.",
            "content_markdown": "# Test Article\n\nThis is a test article content.",
            "content_html": "<h1>Test Article</h1><p>This is a test article content.</p>",
            "author": "Test Author",
            "published_at": self.existing_article.published_at,
            "image_url": "https://example.com/image.jpg",
            "website_id": 1,
            "article_metadata": {"word_count": 7, "reading_time": 1},
            "active": True,
            "last_checked_at": datetime.utcnow()
        }

    def test_should_update_article_with_changes(self):
        """Test should_update_article with changes."""
        should_update, reasons = should_update_article(self.existing_article, self.new_article_data)
        self.assertTrue(should_update)
        self.assertGreater(len(reasons), 0)

    def test_should_update_article_without_changes(self):
        """Test should_update_article without changes."""
        should_update, reasons = should_update_article(self.existing_article, self.unchanged_article_data)
        self.assertFalse(should_update)
        self.assertEqual(len(reasons), 1)
        self.assertEqual(reasons[0], "No significant changes detected")

    def test_should_update_article_force_update(self):
        """Test should_update_article with force update."""
        should_update, reasons = should_update_article(
            self.existing_article, self.unchanged_article_data, force_update=True
        )
        self.assertTrue(should_update)
        self.assertEqual(reasons[0], "Force update enabled")

    def test_has_significant_content_changes(self):
        """Test has_significant_content_changes."""
        # Test with significant changes
        self.assertTrue(has_significant_content_changes(self.existing_article, self.new_article_data))

        # Test without significant changes
        self.assertFalse(has_significant_content_changes(self.existing_article, self.unchanged_article_data))

    def test_has_metadata_changes(self):
        """Test has_metadata_changes."""
        # Test with metadata changes
        self.assertTrue(has_metadata_changes(self.existing_article, self.new_article_data))

        # Test without metadata changes
        self.assertFalse(has_metadata_changes(self.existing_article, self.unchanged_article_data))

    def test_merge_article_data(self):
        """Test merge_article_data."""
        merged_data = merge_article_data(self.existing_article, self.new_article_data)

        # Check that merged data contains new values
        self.assertEqual(merged_data["title"], self.new_article_data["title"])
        self.assertEqual(merged_data["content"], self.new_article_data["content"])

        # Check that update_count is incremented
        self.assertEqual(merged_data["update_count"], self.existing_article.update_count + 1)

        # Check that last_checked_at is updated
        self.assertIsNotNone(merged_data["last_checked_at"])

    def test_get_article_changes_summary(self):
        """Test get_article_changes_summary."""
        summary = get_article_changes_summary(self.existing_article, self.new_article_data)

        # Check that summary contains changes
        self.assertIn("Title changed", summary)
        self.assertIn("Content length changed", summary)

        # Test without changes
        summary = get_article_changes_summary(self.existing_article, self.unchanged_article_data)
        self.assertEqual(summary, "No significant changes detected")


# We'll skip the ArticleService tests for now as they require more complex mocking
# and focus on the core article comparison functionality


if __name__ == "__main__":
    unittest.main()
