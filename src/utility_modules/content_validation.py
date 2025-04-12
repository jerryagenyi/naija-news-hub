"""
Content validation module for Naija News Hub.

This module provides functions to validate article content and ensure quality.
"""

import re
import logging
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
from config.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ValidationResult:
    """Class to represent the result of content validation."""

    def __init__(self, is_valid: bool, score: float, issues: List[str], metadata: Dict[str, Any]):
        """
        Initialize ValidationResult.

        Args:
            is_valid: Whether the content is valid
            score: Quality score (0-100)
            issues: List of validation issues
            metadata: Additional metadata about the validation
        """
        self.is_valid = is_valid
        self.score = score
        self.issues = issues
        self.metadata = metadata

    def __str__(self) -> str:
        """String representation of ValidationResult."""
        return f"ValidationResult(valid={self.is_valid}, score={self.score:.2f}, issues={len(self.issues)})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert ValidationResult to dictionary."""
        return {
            "is_valid": self.is_valid,
            "score": self.score,
            "issues": self.issues,
            "metadata": self.metadata
        }

class ContentValidator:
    """Class to validate article content."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ContentValidator.

        Args:
            config: Optional configuration for validation
        """
        self.config = config or {}

        # Get app configuration
        app_config = get_config()
        validation_config = app_config.content_validation

        # Use provided config or app config
        self.enabled = self.config.get("enabled", validation_config.enabled)
        self.min_quality_score = self.config.get("min_quality_score", validation_config.min_quality_score)
        self.reject_low_quality = self.config.get("reject_low_quality", validation_config.reject_low_quality)

        # Default validation thresholds
        self.min_title_length = self.config.get("min_title_length", validation_config.min_title_length)
        self.max_title_length = self.config.get("max_title_length", validation_config.max_title_length)
        self.min_content_length = self.config.get("min_content_length", validation_config.min_content_length)
        self.max_content_length = self.config.get("max_content_length", validation_config.max_content_length)
        self.min_word_count = self.config.get("min_word_count", validation_config.min_word_count)
        self.min_paragraph_count = self.config.get("min_paragraph_count", validation_config.min_paragraph_count)
        self.max_duplicate_paragraph_ratio = self.config.get("max_duplicate_paragraph_ratio", validation_config.max_duplicate_paragraph_ratio)
        self.max_ad_content_ratio = self.config.get("max_ad_content_ratio", validation_config.max_ad_content_ratio)
        self.min_image_count = self.config.get("min_image_count", validation_config.min_image_count)
        self.max_recent_date_days = self.config.get("max_recent_date_days", validation_config.max_recent_date_days)
        self.detect_clickbait = self.config.get("detect_clickbait", validation_config.detect_clickbait)
        self.detect_spam = self.config.get("detect_spam", validation_config.detect_spam)
        self.detect_placeholder = self.config.get("detect_placeholder", validation_config.detect_placeholder)

        # Spam and low-quality content patterns
        self.spam_patterns = self.config.get("spam_patterns", [
            r'buy now',
            r'click here',
            r'limited time offer',
            r'discount',
            r'sale',
            r'subscribe now',
            r'special offer',
            r'best price',
            r'free shipping',
            r'money back guarantee',
            r'act now',
            r'call now',
            r'exclusive deal',
            r'limited stock',
            r'order now',
            r'satisfaction guaranteed',
            r'while supplies last',
            r'sign up now',
            r'as seen on tv',
            r'free trial',
        ])

        # Clickbait title patterns
        self.clickbait_patterns = self.config.get("clickbait_patterns", [
            r'you won\'t believe',
            r'shocking',
            r'amazing',
            r'incredible',
            r'mind-blowing',
            r'jaw-dropping',
            r'unbelievable',
            r'secret',
            r'trick',
            r'hack',
            r'this one weird',
            r'doctors hate',
            r'\\d+ (things|ways|reasons|tips|tricks|hacks|facts)',
            r'number \\d+ will shock you',
            r'what happens next',
            r'you\'ll never guess',
            r'this will blow your mind',
            r'changed my life',
            r'will change your life',
            r'the truth about',
            r'find out',
            r'discover',
            r'revealed',
        ])

        # Placeholder content patterns
        self.placeholder_patterns = self.config.get("placeholder_patterns", [
            r'lorem ipsum',
            r'sample text',
            r'example content',
            r'placeholder',
            r'text here',
            r'content here',
            r'under construction',
            r'coming soon',
            r'to be updated',
            r'to be added',
        ])

    def validate_article(self, article_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate article content.

        Args:
            article_data: Article data to validate

        Returns:
            ValidationResult: Validation result
        """
        # If validation is disabled, return a valid result
        if not self.enabled:
            return ValidationResult(
                is_valid=True,
                score=100.0,
                issues=[],
                metadata={"validation_enabled": False}
            )

        issues = []
        score = 100.0  # Start with perfect score
        metadata = {"validation_enabled": True}

        # Extract article data
        title = article_data.get("title", "")
        content = article_data.get("content", "")
        content_markdown = article_data.get("content_markdown", "")
        content_html = article_data.get("content_html", "")
        author = article_data.get("author", "")
        published_at = article_data.get("published_at", "")
        image_url = article_data.get("image_url", "")
        article_metadata = article_data.get("article_metadata", {})

        # Use the most appropriate content field
        if content_markdown:
            main_content = content_markdown
        elif content:
            main_content = content
        elif content_html:
            main_content = self._strip_html_tags(content_html)
        else:
            main_content = ""

        # Validate title
        title_result = self._validate_title(title)
        issues.extend(title_result[1])
        score -= title_result[2]
        metadata["title_score"] = 100 - title_result[2]

        # Validate content
        content_result = self._validate_content(main_content)
        issues.extend(content_result[1])
        score -= content_result[2]
        metadata["content_score"] = 100 - content_result[2]

        # Validate author
        author_result = self._validate_author(author)
        issues.extend(author_result[1])
        score -= author_result[2]
        metadata["author_score"] = 100 - author_result[2]

        # Validate published date
        date_result = self._validate_published_date(published_at)
        issues.extend(date_result[1])
        score -= date_result[2]
        metadata["date_score"] = 100 - date_result[2]

        # Validate images
        image_result = self._validate_images(image_url, main_content)
        issues.extend(image_result[1])
        score -= image_result[2]
        metadata["image_score"] = 100 - image_result[2]

        # Validate metadata
        metadata_result = self._validate_metadata(article_metadata)
        issues.extend(metadata_result[1])
        score -= metadata_result[2]
        metadata["metadata_score"] = 100 - metadata_result[2]

        # Ensure score is within bounds
        score = max(0, min(100, score))

        # Determine if article is valid based on score and critical issues
        is_valid = score >= self.min_quality_score and not any(issue.startswith("[CRITICAL]") for issue in issues)

        # Add additional metadata
        metadata["word_count"] = len(re.findall(r'\w+', main_content))
        metadata["paragraph_count"] = len(re.split(r'\n\s*\n', main_content))
        metadata["validation_timestamp"] = datetime.utcnow().isoformat()

        return ValidationResult(is_valid, score, issues, metadata)

    def _validate_title(self, title: str) -> Tuple[bool, List[str], float]:
        """
        Validate article title.

        Args:
            title: Article title

        Returns:
            Tuple of (is_valid, issues, score_penalty)
        """
        issues = []
        score_penalty = 0

        # Check title length
        if not title:
            issues.append("[CRITICAL] Title is missing")
            score_penalty += 50
            return False, issues, score_penalty

        if len(title) < self.min_title_length:
            issues.append(f"Title is too short ({len(title)} chars, minimum {self.min_title_length})")
            score_penalty += 10

        if len(title) > self.max_title_length:
            issues.append(f"Title is too long ({len(title)} chars, maximum {self.max_title_length})")
            score_penalty += 5

        # Check for clickbait patterns
        clickbait_count = 0
        for pattern in self.clickbait_patterns:
            if re.search(pattern, title.lower()):
                clickbait_count += 1

        if clickbait_count > 0:
            issues.append(f"Title contains {clickbait_count} clickbait patterns")
            score_penalty += min(20, clickbait_count * 5)

        # Check for all caps
        if title.isupper() and len(title) > 10:
            issues.append("Title is in all caps")
            score_penalty += 10

        # Check for excessive punctuation
        if title.count('!') > 1 or title.count('?') > 2:
            issues.append("Title contains excessive punctuation")
            score_penalty += 5

        return len(issues) == 0, issues, score_penalty

    def _validate_content(self, content: str) -> Tuple[bool, List[str], float]:
        """
        Validate article content.

        Args:
            content: Article content

        Returns:
            Tuple of (is_valid, issues, score_penalty)
        """
        issues = []
        score_penalty = 0

        # Check content length
        if not content:
            issues.append("[CRITICAL] Content is missing")
            score_penalty += 50
            return False, issues, score_penalty

        if len(content) < self.min_content_length:
            issues.append(f"Content is too short ({len(content)} chars, minimum {self.min_content_length})")
            score_penalty += 20

        if len(content) > self.max_content_length:
            issues.append(f"Content is too long ({len(content)} chars, maximum {self.max_content_length})")
            score_penalty += 5

        # Check word count
        word_count = len(re.findall(r'\w+', content))
        if word_count < self.min_word_count:
            issues.append(f"Content has too few words ({word_count} words, minimum {self.min_word_count})")
            score_penalty += 15

        # Check paragraph count
        paragraphs = re.split(r'\n\s*\n', content)
        if len(paragraphs) < self.min_paragraph_count:
            issues.append(f"Content has too few paragraphs ({len(paragraphs)} paragraphs, minimum {self.min_paragraph_count})")
            score_penalty += 10

        # Check for duplicate paragraphs
        unique_paragraphs = set(paragraphs)
        duplicate_ratio = 1 - (len(unique_paragraphs) / len(paragraphs)) if paragraphs else 0
        if duplicate_ratio > self.max_duplicate_paragraph_ratio:
            issues.append(f"Content has high duplicate paragraph ratio ({duplicate_ratio:.2f}, maximum {self.max_duplicate_paragraph_ratio})")
            score_penalty += 15

        # Check for spam patterns
        spam_count = 0
        for pattern in self.spam_patterns:
            spam_count += len(re.findall(pattern, content.lower()))

        if spam_count > 0:
            issues.append(f"Content contains {spam_count} spam patterns")
            score_penalty += min(20, spam_count * 2)

        # Check for placeholder content
        for pattern in self.placeholder_patterns:
            if re.search(pattern, content.lower()):
                issues.append("Content contains placeholder text")
                score_penalty += 30
                break

        return len(issues) == 0, issues, score_penalty

    def _validate_author(self, author: str) -> Tuple[bool, List[str], float]:
        """
        Validate article author.

        Args:
            author: Article author

        Returns:
            Tuple of (is_valid, issues, score_penalty)
        """
        issues = []
        score_penalty = 0

        # Check author presence
        if not author:
            issues.append("Author is missing")
            score_penalty += 5
        elif author.lower() in ["unknown", "admin", "administrator", "staff", "editor", "guest"]:
            issues.append(f"Author has generic name: {author}")
            score_penalty += 3

        return len(issues) == 0, issues, score_penalty

    def _validate_published_date(self, published_at: Any) -> Tuple[bool, List[str], float]:
        """
        Validate article published date.

        Args:
            published_at: Article published date

        Returns:
            Tuple of (is_valid, issues, score_penalty)
        """
        issues = []
        score_penalty = 0

        # Check published date presence
        if not published_at:
            issues.append("Published date is missing")
            score_penalty += 5
            return False, issues, score_penalty

        # Convert string to datetime if needed
        if isinstance(published_at, str):
            try:
                # Try ISO format first
                published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            except ValueError:
                try:
                    # Try common formats
                    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%B %d, %Y"]:
                        try:
                            published_date = datetime.strptime(published_at, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        issues.append(f"Published date has invalid format: {published_at}")
                        score_penalty += 5
                        return False, issues, score_penalty
                except Exception:
                    issues.append(f"Published date has invalid format: {published_at}")
                    score_penalty += 5
                    return False, issues, score_penalty
        else:
            published_date = published_at

        # Check if date is in the future
        if published_date > datetime.utcnow():
            issues.append(f"Published date is in the future: {published_date}")
            score_penalty += 10

        # Check if date is too old
        max_age = datetime.utcnow() - timedelta(days=self.max_recent_date_days)
        if published_date < max_age:
            issues.append(f"Published date is too old: {published_date}")
            score_penalty += 5

        return len(issues) == 0, issues, score_penalty

    def _validate_images(self, image_url: str, content: str) -> Tuple[bool, List[str], float]:
        """
        Validate article images.

        Args:
            image_url: Main image URL
            content: Article content

        Returns:
            Tuple of (is_valid, issues, score_penalty)
        """
        issues = []
        score_penalty = 0

        # Count images in content
        image_count = 0
        if image_url:
            image_count += 1

        # Count markdown images
        image_count += len(re.findall(r'!\[.*?\]\(.*?\)', content))

        # Count HTML images
        image_count += len(re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', content))

        if image_count < self.min_image_count:
            issues.append(f"Article has too few images ({image_count} images, minimum {self.min_image_count})")
            score_penalty += 5

        return len(issues) == 0, issues, score_penalty

    def _validate_metadata(self, metadata: Dict[str, Any]) -> Tuple[bool, List[str], float]:
        """
        Validate article metadata.

        Args:
            metadata: Article metadata

        Returns:
            Tuple of (is_valid, issues, score_penalty)
        """
        issues = []
        score_penalty = 0

        # Check for required metadata
        if not metadata:
            issues.append("Metadata is missing")
            score_penalty += 5
            return False, issues, score_penalty

        # Check word count
        word_count = metadata.get("word_count", 0)
        if word_count < self.min_word_count:
            issues.append(f"Metadata word count is too low ({word_count} words, minimum {self.min_word_count})")
            score_penalty += 5

        return len(issues) == 0, issues, score_penalty

    def _strip_html_tags(self, html: str) -> str:
        """
        Strip HTML tags from content.

        Args:
            html: HTML content

        Returns:
            Plain text content
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)

        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)

        # Replace HTML entities
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&quot;', '"', text)
        text = re.sub(r'&#39;', "'", text)

        return text.strip()


def validate_article_content(article_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> ValidationResult:
    """
    Validate article content.

    Args:
        article_data: Article data to validate
        config: Optional configuration for validation

    Returns:
        ValidationResult: Validation result
    """
    validator = ContentValidator(config)
    return validator.validate_article(article_data)
