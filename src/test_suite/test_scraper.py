"""
Tests for the scraper module.

This module provides tests for the scraper functionality.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock

from src.web_scraper.url_discovery import discover_urls, is_valid_article_url
from src.web_scraper.article_extractor import extract_article

def test_is_valid_article_url():
    """Test the is_valid_article_url function."""
    base_url = "https://example.com"
    
    # Valid URLs
    assert is_valid_article_url("https://example.com/article/1", base_url) is True
    assert is_valid_article_url("https://example.com/news/article-title", base_url) is True
    
    # Invalid URLs
    assert is_valid_article_url("https://other-domain.com/article/1", base_url) is False
    assert is_valid_article_url("https://example.com/category/news", base_url) is False
    assert is_valid_article_url("https://example.com/tag/politics", base_url) is False
    assert is_valid_article_url("https://example.com/author/john-doe", base_url) is False
    assert is_valid_article_url("https://example.com/search?q=news", base_url) is False
    assert is_valid_article_url("https://example.com/sitemap.xml", base_url) is False

@pytest.mark.asyncio
async def test_discover_urls():
    """Test the discover_urls function."""
    base_url = "https://example.com"
    urls = await discover_urls(base_url)
    
    # Check that we got some URLs
    assert len(urls) > 0
    
    # Check that all URLs are from the same domain
    for url in urls:
        assert url.startswith(base_url)

@pytest.mark.asyncio
async def test_extract_article():
    """Test the extract_article function."""
    url = "https://example.com/article/1"
    website_id = 1
    
    article_data = await extract_article(url, website_id)
    
    # Check that we got article data
    assert article_data is not None
    assert "title" in article_data
    assert "content" in article_data
    assert "url" in article_data
    assert article_data["url"] == url
    assert article_data["website_id"] == website_id
