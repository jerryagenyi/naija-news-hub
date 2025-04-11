"""
Tests for the news scraper.
"""

import unittest
from unittest.mock import MagicMock, patch

from scraper.article_scraper import ArticleScraper


class TestArticleScraper(unittest.TestCase):
    """Test cases for the ArticleScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://example-news-site.com"
        self.scraper = ArticleScraper(self.base_url)
    
    @patch('scraper.article_scraper.requests.Session')
    def test_get_article_links(self, mock_session):
        """Test that article links are correctly extracted."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <body>
                <a href="/2023/04/11/test-article">Test Article</a>
                <a href="https://example-news-site.com/news/another-article">Another Article</a>
                <a href="/category/politics">Politics</a>
                <article>
                    <a href="/story/important-news">Important News</a>
                </article>
            </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        
        # Set up the mock session
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        # Call the method
        links = self.scraper.get_article_links()
        
        # Assertions
        self.assertEqual(len(links), 3)
        self.assertIn("https://example-news-site.com/2023/04/11/test-article", links)
        self.assertIn("https://example-news-site.com/news/another-article", links)
        self.assertIn("https://example-news-site.com/story/important-news", links)
        self.assertNotIn("https://example-news-site.com/category/politics", links)


if __name__ == '__main__':
    unittest.main()
