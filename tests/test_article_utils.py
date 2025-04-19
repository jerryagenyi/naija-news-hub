#!/usr/bin/env python
"""
Tests for article utility functions.
"""
import json
import datetime
import unittest
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.article_utils import (
    create_article_metadata,
    format_tags,
    extract_content_from_metadata,
    extract_metadata_field,
    update_article_content
)

class TestArticleUtils(unittest.TestCase):
    """Test article utility functions."""

    def test_create_article_metadata(self):
        """Test creating article metadata."""
        # Test with minimal parameters
        metadata = create_article_metadata(
            content="# Test Article\n\nThis is a test.",
            title="Test Article"
        )

        self.assertEqual(metadata["metadata"]["title"], "Test Article")
        self.assertEqual(metadata["content"]["markdown"], "# Test Article\n\nThis is a test.")
        self.assertEqual(metadata["content"]["word_count"], 7)
        self.assertEqual(metadata["content"]["reading_time"], 1)

        # Test with all parameters
        published_date = datetime.datetime(2025, 5, 16, 12, 0, 0)
        metadata = create_article_metadata(
            content="# Test Article\n\nThis is a comprehensive test article with more words to test word count and reading time calculation.",
            title="Comprehensive Test",
            author="Test Author",
            published_date=published_date,
            source_website="Test Website",
            source_url="https://test.com/article",
            image_url="https://test.com/image.jpg",
            categories=[
                {"name": "Test", "url": "https://test.com/category/test"},
                {"name": "Example", "url": "https://test.com/category/example"}
            ],
            word_count=100,
            reading_time=2
        )

        self.assertEqual(metadata["metadata"]["title"], "Comprehensive Test")
        self.assertEqual(metadata["metadata"]["author"], "Test Author")
        self.assertEqual(metadata["metadata"]["published_date"], published_date.isoformat())
        self.assertEqual(metadata["metadata"]["source_website"], "Test Website")
        self.assertEqual(metadata["content"]["word_count"], 100)
        self.assertEqual(metadata["content"]["reading_time"], 2)
        self.assertEqual(len(metadata["metadata"]["categories"]), 2)

    def test_format_tags(self):
        """Test formatting tags."""
        # Test without base URL
        tags = ["Test", "Example", "Multiple Words"]
        formatted_tags = format_tags(tags)

        self.assertEqual(len(formatted_tags), 3)
        self.assertEqual(formatted_tags[0]["name"], "Test")
        self.assertNotIn("url", formatted_tags[0])

        # Test with base URL
        formatted_tags = format_tags(tags, base_url="https://test.com")

        self.assertEqual(len(formatted_tags), 3)
        self.assertEqual(formatted_tags[0]["name"], "Test")
        self.assertEqual(formatted_tags[0]["url"], "https://test.com/tag/test")
        self.assertEqual(formatted_tags[2]["url"], "https://test.com/tag/multiple-words")

    def test_extract_content_from_metadata(self):
        """Test extracting content from metadata."""
        # Create test metadata
        metadata = create_article_metadata(
            content="# Test Content",
            title="Test Title"
        )

        # Test with dict
        content = extract_content_from_metadata(metadata)
        self.assertEqual(content, "# Test Content")

        # Test with JSON string
        json_metadata = json.dumps(metadata)
        content = extract_content_from_metadata(json_metadata)
        self.assertEqual(content, "# Test Content")

        # Test with empty metadata
        content = extract_content_from_metadata({})
        self.assertEqual(content, "")

    def test_extract_metadata_field(self):
        """Test extracting metadata field."""
        # Create test metadata
        metadata = create_article_metadata(
            content="# Test Content",
            title="Test Title",
            author="Test Author"
        )

        # Test with dict
        title = extract_metadata_field(metadata, "title")
        self.assertEqual(title, "Test Title")

        author = extract_metadata_field(metadata, "author")
        self.assertEqual(author, "Test Author")

        # Test with JSON string
        json_metadata = json.dumps(metadata)
        title = extract_metadata_field(json_metadata, "title")
        self.assertEqual(title, "Test Title")

        # Test with non-existent field
        field = extract_metadata_field(metadata, "non_existent")
        self.assertIsNone(field)

    def test_update_article_content(self):
        """Test updating article content."""
        # Create test metadata
        metadata = create_article_metadata(
            content="# Original Content",
            title="Test Title",
            word_count=2,
            reading_time=1
        )

        # Update content
        updated_metadata = update_article_content(
            metadata,
            "# Updated Content\n\nThis is updated content with more words to test word count and reading time recalculation."
        )

        # Check that content was updated
        self.assertEqual(updated_metadata["content"]["markdown"], "# Updated Content\n\nThis is updated content with more words to test word count and reading time recalculation.")
        self.assertEqual(updated_metadata["content"]["word_count"], 18)
        self.assertEqual(updated_metadata["content"]["reading_time"], 1)

        # Check that other metadata was preserved
        self.assertEqual(updated_metadata["metadata"]["title"], "Test Title")

        # Test with JSON string
        json_metadata = json.dumps(metadata)
        updated_metadata = update_article_content(
            json_metadata,
            "# Updated JSON Content"
        )

        self.assertEqual(updated_metadata["content"]["markdown"], "# Updated JSON Content")
        self.assertEqual(updated_metadata["content"]["word_count"], 4)

if __name__ == "__main__":
    unittest.main()
