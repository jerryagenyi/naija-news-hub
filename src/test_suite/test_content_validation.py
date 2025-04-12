"""
Unit tests for content validation module.
"""

import unittest
from datetime import datetime, timedelta
from src.utility_modules.content_validation import ContentValidator, ValidationResult, validate_article_content


class TestContentValidation(unittest.TestCase):
    """Test cases for content validation."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test configuration
        self.test_config = {
            "enabled": True,
            "min_quality_score": 50,
            "reject_low_quality": True,
            "min_title_length": 10,
            "max_title_length": 200,
            "min_content_length": 100,
            "max_content_length": 10000,
            "min_word_count": 50,
            "min_paragraph_count": 2,
            "max_duplicate_paragraph_ratio": 0.3,
            "max_ad_content_ratio": 0.2,
            "min_image_count": 0,
            "max_recent_date_days": 365 * 5,  # 5 years
            "detect_clickbait": True,
            "detect_spam": True,
            "detect_placeholder": True
        }
        
        # Create a validator with test configuration
        self.validator = ContentValidator(self.test_config)
        
        # Create a good article
        self.good_article = {
            "title": "This is a good article title with proper length",
            "content": "This is a good article content with proper length. " * 30,
            "content_markdown": "# This is a good article\n\nThis is a paragraph.\n\nThis is another paragraph.\n\n" + ("This is more content. " * 30),
            "content_html": "<h1>This is a good article</h1><p>This is a paragraph.</p><p>This is another paragraph.</p><p>" + ("This is more content. " * 30) + "</p>",
            "author": "John Doe",
            "published_at": datetime.now().isoformat(),
            "image_url": "https://example.com/image.jpg",
            "article_metadata": {
                "word_count": 150,
                "reading_time": 1,
                "categories": ["News", "Technology"],
                "tags": ["AI", "Machine Learning"]
            }
        }
        
        # Create a bad article
        self.bad_article = {
            "title": "Short",
            "content": "Too short content.",
            "content_markdown": "# Short\n\nToo short content.",
            "content_html": "<h1>Short</h1><p>Too short content.</p>",
            "author": "",
            "published_at": (datetime.now() + timedelta(days=10)).isoformat(),  # Future date
            "image_url": "",
            "article_metadata": {}
        }
        
        # Create a spam article
        self.spam_article = {
            "title": "You won't believe this amazing offer! Buy now!",
            "content": "Buy now! Limited time offer! Discount! " * 20,
            "content_markdown": "# Amazing offer\n\nBuy now! Limited time offer! Discount! " * 20,
            "content_html": "<h1>Amazing offer</h1><p>Buy now! Limited time offer! Discount! " * 20 + "</p>",
            "author": "Sales Team",
            "published_at": datetime.now().isoformat(),
            "image_url": "",
            "article_metadata": {
                "word_count": 100,
                "reading_time": 1
            }
        }
        
        # Create a placeholder article
        self.placeholder_article = {
            "title": "Article Title To Be Updated",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20,
            "content_markdown": "# Article Title\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20,
            "content_html": "<h1>Article Title</h1><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20 + "</p>",
            "author": "Content Team",
            "published_at": datetime.now().isoformat(),
            "image_url": "",
            "article_metadata": {
                "word_count": 120,
                "reading_time": 1
            }
        }

    def test_validation_result_creation(self):
        """Test ValidationResult creation."""
        result = ValidationResult(True, 90.5, ["Issue 1", "Issue 2"], {"key": "value"})
        self.assertTrue(result.is_valid)
        self.assertEqual(result.score, 90.5)
        self.assertEqual(result.issues, ["Issue 1", "Issue 2"])
        self.assertEqual(result.metadata, {"key": "value"})
        
        # Test to_dict method
        result_dict = result.to_dict()
        self.assertEqual(result_dict["is_valid"], True)
        self.assertEqual(result_dict["score"], 90.5)
        self.assertEqual(result_dict["issues"], ["Issue 1", "Issue 2"])
        self.assertEqual(result_dict["metadata"], {"key": "value"})
        
        # Test string representation
        self.assertIn("ValidationResult", str(result))
        self.assertIn("90.50", str(result))
        self.assertIn("2", str(result))

    def test_good_article_validation(self):
        """Test validation of a good article."""
        result = self.validator.validate_article(self.good_article)
        self.assertTrue(result.is_valid)
        self.assertGreaterEqual(result.score, 80)  # Good articles should have high scores
        self.assertLessEqual(len(result.issues), 2)  # Good articles should have few issues

    def test_bad_article_validation(self):
        """Test validation of a bad article."""
        result = self.validator.validate_article(self.bad_article)
        self.assertFalse(result.is_valid)
        self.assertLessEqual(result.score, 60)  # Bad articles should have low scores
        self.assertGreaterEqual(len(result.issues), 3)  # Bad articles should have multiple issues
        
        # Check for specific issues
        title_issue = any("title" in issue.lower() for issue in result.issues)
        content_issue = any("content" in issue.lower() for issue in result.issues)
        date_issue = any("future" in issue.lower() for issue in result.issues)
        
        self.assertTrue(title_issue, "Should have title issue")
        self.assertTrue(content_issue, "Should have content issue")
        self.assertTrue(date_issue, "Should have date issue")

    def test_spam_article_validation(self):
        """Test validation of a spam article."""
        result = self.validator.validate_article(self.spam_article)
        
        # Check for spam detection
        spam_issue = any("spam" in issue.lower() for issue in result.issues)
        clickbait_issue = any("clickbait" in issue.lower() for issue in result.issues)
        
        self.assertTrue(spam_issue or clickbait_issue, "Should detect spam or clickbait")
        self.assertLessEqual(result.score, 70)  # Spam articles should have lower scores

    def test_placeholder_article_validation(self):
        """Test validation of a placeholder article."""
        result = self.validator.validate_article(self.placeholder_article)
        
        # Check for placeholder detection
        placeholder_issue = any("placeholder" in issue.lower() or "lorem ipsum" in issue.lower() for issue in result.issues)
        
        self.assertTrue(placeholder_issue, "Should detect placeholder content")
        self.assertLessEqual(result.score, 70)  # Placeholder articles should have lower scores

    def test_validation_with_disabled_validation(self):
        """Test validation when validation is disabled."""
        # Create a validator with validation disabled
        disabled_config = self.test_config.copy()
        disabled_config["enabled"] = False
        disabled_validator = ContentValidator(disabled_config)
        
        # Validate a bad article with validation disabled
        result = disabled_validator.validate_article(self.bad_article)
        
        # Should always be valid when validation is disabled
        self.assertTrue(result.is_valid)
        self.assertEqual(result.score, 100.0)
        self.assertEqual(len(result.issues), 0)
        self.assertEqual(result.metadata["validation_enabled"], False)

    def test_validate_article_content_function(self):
        """Test the validate_article_content function."""
        result = validate_article_content(self.good_article)
        self.assertTrue(result.is_valid)
        self.assertGreaterEqual(result.score, 80)
        
        result = validate_article_content(self.bad_article)
        self.assertFalse(result.is_valid)
        self.assertLessEqual(result.score, 60)


if __name__ == "__main__":
    unittest.main()
