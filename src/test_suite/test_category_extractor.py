"""
Unit tests for category extractor module.
"""

import unittest
from src.web_scraper.category_extractor import (
    extract_categories_from_html,
    extract_tags_from_html,
    normalize_category_name,
    generate_category_url,
    categorize_article
)


class TestCategoryExtractor(unittest.TestCase):
    """Test cases for category extractor."""

    def setUp(self):
        """Set up test fixtures."""
        # Sample HTML with various category indicators
        self.sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Article</title>
            <meta property="article:section" content="Politics" />
            <meta property="og:article:section" content="Government" />
            <meta name="DC.subject" content="Elections, Voting, Democracy" />
            <meta property="article:tag" content="Nigeria, Election, 2023" />
            <meta name="keywords" content="politics, government, election" />
            <link rel="canonical" href="https://example.com/politics/election-2023" />
        </head>
        <body>
            <nav>
                <ul>
                    <li class="breadcrumb-item"><a href="/">Home</a></li>
                    <li class="breadcrumb-item"><a href="/news">News</a></li>
                    <li class="breadcrumb-item current"><a href="/news/politics">Politics</a></li>
                </ul>
            </nav>
            <div itemscope itemtype="http://schema.org/Article">
                <meta itemprop="articleSection" content="Political News" />
                <h1>Test Article</h1>
                <p>This is a test article about politics and elections.</p>
            </div>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "NewsArticle",
                "headline": "Test Article",
                "articleSection": "Politics",
                "keywords": ["Nigeria", "Election", "2023"],
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home"
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "News"
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "name": "Politics"
                        }
                    ]
                }
            }
            </script>
            <div class="tags">
                <a href="/tag/nigeria" class="tag">Nigeria</a>
                <a href="/tag/election" class="tag">Election</a>
                <a href="/tag/2023" class="tag">2023</a>
            </div>
        </body>
        </html>
        """

        # Sample article data
        self.sample_article = {
            "title": "Test Article About Politics",
            "content": "This is a test article about politics and elections in Nigeria. The 2023 election is approaching.",
            "content_html": self.sample_html,
            "url": "https://example.com/politics/election-2023",
            "author": "Test Author",
            "published_at": "2023-01-01T00:00:00Z",
            "image_url": "https://example.com/image.jpg",
            "article_metadata": {
                "word_count": 20,
                "reading_time": 1
            }
        }

    def test_extract_categories_from_html(self):
        """Test extracting categories from HTML."""
        categories = extract_categories_from_html(self.sample_html)

        # Check that we extracted categories from various sources
        self.assertIn("Politics", categories)
        self.assertIn("News", categories)

        # Print categories for debugging
        print(f"Extracted categories: {categories}")

        # Check that we don't have duplicates
        self.assertEqual(len(categories), len(set(categories)))

        # Check that we have at least 3 categories
        self.assertGreaterEqual(len(categories), 3)

    def test_extract_tags_from_html(self):
        """Test extracting tags from HTML."""
        tags = extract_tags_from_html(self.sample_html)

        # Check that we extracted tags from various sources
        self.assertIn("Nigeria", tags)
        self.assertIn("Election", tags)
        self.assertIn("2023", tags)

        # Check that we don't have duplicates
        self.assertEqual(len(tags), len(set(tags)))

        # Check that we have at least 3 tags
        self.assertGreaterEqual(len(tags), 3)

    def test_normalize_category_name(self):
        """Test normalizing category names."""
        # Test title case
        self.assertEqual(normalize_category_name("politics"), "Politics")

        # Test abbreviations
        self.assertEqual(normalize_category_name("ai news"), "AI News")
        self.assertEqual(normalize_category_name("us politics"), "US Politics")

        # Test special characters
        self.assertEqual(normalize_category_name("politics & government"), "Politics Government")

        # Test extra whitespace
        self.assertEqual(normalize_category_name("  politics  "), "Politics")

    def test_generate_category_url(self):
        """Test generating category URLs."""
        # Test basic URL generation
        self.assertEqual(
            generate_category_url("https://example.com", "Politics"),
            "https://example.com/category/politics"
        )

        # Test with spaces
        self.assertEqual(
            generate_category_url("https://example.com", "Political News"),
            "https://example.com/category/political-news"
        )

        # Test with special characters
        self.assertEqual(
            generate_category_url("https://example.com", "Politics & Government"),
            "https://example.com/category/politics-government"
        )

        # Test with trailing slash
        self.assertEqual(
            generate_category_url("https://example.com/", "Politics"),
            "https://example.com/category/politics"
        )

    def test_categorize_article(self):
        """Test categorizing an article."""
        # Categorize the article
        result = categorize_article(self.sample_article, "https://example.com")

        # Check that we have categories
        self.assertIn("categories", result)
        self.assertGreater(len(result["categories"]), 0)

        # Check that we have tags
        self.assertIn("tags", result)
        self.assertGreater(len(result["tags"]), 0)

        # Check that we have category URLs
        self.assertIn("category_urls", result)
        self.assertEqual(len(result["category_urls"]), len(result["categories"]))

        # Check that category URLs are properly formatted
        for url in result["category_urls"]:
            self.assertTrue(url.startswith("https://example.com/category/"))

    def test_categorize_article_with_no_categories(self):
        """Test categorizing an article with no explicit categories."""
        # Create an article with no categories in HTML
        article = self.sample_article.copy()
        article["content_html"] = "<html><body><p>This is an article about technology and AI.</p></body></html>"

        # Categorize the article
        result = categorize_article(article, "https://example.com")

        # Check that we inferred categories from content
        self.assertIn("categories", result)
        self.assertGreater(len(result["categories"]), 0)

        # Check that we have category URLs
        self.assertIn("category_urls", result)
        self.assertEqual(len(result["category_urls"]), len(result["categories"]))


if __name__ == "__main__":
    unittest.main()
