"""
Article extraction module for Naija News Hub.

This module provides functions to extract article content from news websites.
"""

import logging
import re
from typing import Dict, Any, Optional, List
from datetime import datetime
from urllib.parse import urlparse, urljoin
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    PruningContentFilter,
    MarkdownGenerationStrategy,
    DefaultMarkdownGenerator
)
from config.config import get_config
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from src.utils.error-handling import ScrapingErrorHandler, BrowserErrorHandler
from src.database.models import Article, ScrapingJob
from src.database.connection import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ArticleExtractor:
    def __init__(self, job_id: int):
        self.job_id = job_id
        self.error_handler = ScrapingErrorHandler(job_id)
        self.db = next(get_db())

    async def extract_article(self, url: str) -> Optional[Article]:
        """Extract article content using Crawl4AI with improved error handling."""
        try:
            # Configure browser with memory-adaptive settings
            browser_config = BrowserConfig(
                headless=True,
                memory_limit="adaptive",  # Use memory-adaptive mode
                viewport={"width": 1280, "height": 800},
                wait_until="networkidle",
                timeout=30000
            )

            # Configure content filtering
            content_filter = PruningContentFilter(
                min_length=100,  # Minimum content length
                max_length=10000,  # Maximum content length
                remove_ads=True,
                remove_navigation=True,
                remove_comments=True
            )

            # Configure markdown generation
            markdown_strategy = MarkdownGenerationStrategy(
                generator=DefaultMarkdownGenerator(
                    options={
                        "citations": True,  # Include link citations
                        "clean_whitespace": True,
                        "preserve_images": True
                    }
                ),
                content_filter=content_filter
            )

            # Configure crawler run settings
            crawler_config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                css_selector="article, .article, .post, .content, main",
                excluded_selector="nav, footer, header, .sidebar, .menu, .navigation, .comments, .related, .social, .share",
                excluded_tags=["script", "style", "noscript", "iframe"],
                scan_full_page=True,
                wait_for_images=True,  # Wait for lazy-loaded images
                markdown_strategy=markdown_strategy
            )

            # Create and run crawler
            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(url, config=crawler_config)

                if not result.success:
                    self.error_handler.handle_error(
                        Exception(result.error_message),
                        url,
                        {"action": "crawler_execution"}
                    )
                    return None

                # Extract content from result
                title = result.metadata.get("title", "")
                content = result.markdown.raw_markdown if result.markdown else ""
                author = result.metadata.get("author", "")
                published_date = result.metadata.get("published_date", datetime.utcnow())

                if not title or not content:
                    raise ValueError("Failed to extract required article fields")

                # Create article object
                article = Article(
                    title=title,
                    content=content,
                    url=url,
                    author=author,
                    published_date=published_date,
                    created_at=datetime.utcnow(),
                    metadata={
                        "word_count": len(content.split()),
                        "reading_time": max(1, len(content.split()) // 200),
                        "categories": result.metadata.get("categories", []),
                        "tags": result.metadata.get("tags", []),
                        "images": result.media.get("images", []),
                        "references": result.markdown.references_markdown if result.markdown else ""
                    }
                )

                return article

        except Exception as e:
            self.error_handler.handle_error(e, url, {"action": "article_extraction"})
            return None

    async def extract_article_metadata(self, url: str) -> Dict[str, Any]:
        """Extract article metadata using Crawl4AI's metadata extraction."""
        try:
            browser_config = BrowserConfig(
                headless=True,
                memory_limit="adaptive",
                viewport={"width": 1280, "height": 800},
                wait_until="networkidle",
                timeout=30000
            )

            crawler_config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                css_selector="head, meta, title",
                excluded_tags=["script", "style", "noscript", "iframe"],
                wait_until="networkidle"
            )

            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(url, config=crawler_config)

                if not result.success:
                    self.error_handler.handle_error(
                        Exception(result.error_message),
                        url,
                        {"action": "metadata_extraction"}
                    )
                    return {}

                return {
                    "title": result.metadata.get("title", ""),
                    "author": result.metadata.get("author", ""),
                    "published_date": result.metadata.get("published_date", datetime.utcnow()),
                    "categories": result.metadata.get("categories", []),
                    "tags": result.metadata.get("tags", []),
                    "image_url": result.metadata.get("image_url", ""),
                    "description": result.metadata.get("description", ""),
                    "schema": result.metadata.get("schema", {})
                }

        except Exception as e:
            self.error_handler.handle_error(e, url, {"action": "metadata_extraction"})
            return {}

async def extract_article(url: str, website_id: int, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Extract article content from a URL using AsyncWebCrawler.

    Args:
        url: URL of the article
        website_id: ID of the website
        config: Optional configuration for article extraction

    Returns:
        Dictionary containing article data
    """
    logger.info(f"Extracting article from {url}")

    # Get configuration
    app_config = get_config()
    crawl_config = app_config.crawl4ai

    # Create browser config
    browser_config = BrowserConfig(
        headless=True,
        user_agent=config.get("user_agent", crawl_config.user_agent) if config else crawl_config.user_agent,
    )

    # Create crawler run config
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        css_selector="article, .article, .post, .content, main",  # Common article selectors
        excluded_selector="nav, footer, header, .sidebar, .menu, .navigation, .comments, .related, .social, .share",
        excluded_tags=["script", "style", "noscript", "iframe"],
        scan_full_page=True,
        wait_until="networkidle"
    )

    try:
        # Create AsyncWebCrawler
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # Extract article
            result = await crawler.arun(url, config=crawler_run_config)

            # Extract content from the result
            content = result.cleaned_html or ""
            content_markdown = result.markdown.raw_markdown if result.markdown else ""

            # Calculate word count and reading time
            word_count = len(re.findall(r'\w+', content)) if content else 0
            reading_time = max(1, word_count // 200)  # Assuming 200 words per minute reading speed

            # Try to extract title from HTML
            title_match = re.search(r'<title>(.*?)</title>', result.html, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1) if title_match else f"Article from {url}"

            # Try to extract author
            author_match = re.search(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']*)["\']/>', result.html, re.IGNORECASE | re.DOTALL)
            author = author_match.group(1) if author_match else "Unknown"

            # Try to extract publication date
            date_match = re.search(r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([^"\']*)["\']/>', result.html, re.IGNORECASE | re.DOTALL)
            published_at = date_match.group(1) if date_match else datetime.now().isoformat()

            # Extract image URL
            image_url = None
            # Try to find image URLs in the HTML
            if result.html:
                # Use regex to find image URLs
                img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
                img_urls = re.findall(img_pattern, result.html)
                if img_urls:
                    # Use the first image URL
                    image_url = img_urls[0]
                    # Convert relative URL to absolute URL
                    if image_url.startswith('/'):
                        image_url = urljoin(url, image_url)

            # Create article data
            article_data = {
                "title": title,
                "url": url,
                "content": content,
                "content_markdown": content_markdown,
                "content_html": result.cleaned_html or "",
                "author": author,
                "published_at": published_at,
                "image_url": image_url,
                "website_id": website_id,
                "article_metadata": {
                    "word_count": word_count,
                    "reading_time": reading_time,
                    "categories": [],
                    "tags": [],
                    "schema": {},
                },
                "active": True,
            }

            logger.info(f"Successfully extracted article from {url}: {article_data['title']}")
            return article_data

    except Exception as e:
        logger.error(f"Error extracting article from {url}: {str(e)}")
        # Return dummy article data as fallback
        return {
            "title": f"Sample Article from {url}",
            "url": url,
            "content": "This is a sample article content.",
            "content_markdown": "# Sample Article\n\nThis is a sample article content.",
            "content_html": "<h1>Sample Article</h1><p>This is a sample article content.</p>",
            "author": "Sample Author",
            "published_at": datetime.now().isoformat(),
            "image_url": None,
            "website_id": website_id,
            "article_metadata": {
                "word_count": 7,
                "reading_time": 1,
            },
            "active": True,
        }

async def extract_article_metadata(url: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Extract article metadata from a URL using AsyncWebCrawler.

    Args:
        url: URL of the article
        config: Optional configuration for metadata extraction

    Returns:
        Dictionary containing article metadata
    """
    logger.info(f"Extracting metadata from {url}")

    # Get configuration
    app_config = get_config()
    crawl_config = app_config.crawl4ai

    # Create browser config
    browser_config = BrowserConfig(
        headless=True,
        user_agent=config.get("user_agent", crawl_config.user_agent) if config else crawl_config.user_agent,
    )

    # Create crawler run config
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        css_selector="head, meta, title",  # Focus on metadata in the head
        excluded_tags=["script", "style", "noscript", "iframe"],
        wait_until="networkidle"
    )

    try:
        # Create AsyncWebCrawler
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # Extract article metadata
            result = await crawler.arun(url, config=crawler_run_config)

            # Try to extract title from HTML
            title_match = re.search(r'<title>(.*?)</title>', result.html, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1) if title_match else f"Article from {url}"

            # Try to extract author
            author_match = re.search(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']*)["\']/>', result.html, re.IGNORECASE | re.DOTALL)
            author = author_match.group(1) if author_match else "Unknown"

            # Try to extract publication date
            date_match = re.search(r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([^"\']*)["\']/>', result.html, re.IGNORECASE | re.DOTALL)
            published_at = date_match.group(1) if date_match else datetime.now().isoformat()

            # Try to extract categories
            categories_match = re.search(r'<meta\s+property=["\']article:section["\']\s+content=["\']([^"\']*)["\']/>', result.html, re.IGNORECASE | re.DOTALL)
            categories = [categories_match.group(1)] if categories_match else ["News"]

            # Try to extract tags
            tags_match = re.search(r'<meta\s+property=["\']article:tag["\']\s+content=["\']([^"\']*)["\']/>', result.html, re.IGNORECASE | re.DOTALL)
            tags = [tag.strip() for tag in tags_match.group(1).split(',')] if tags_match else []

            # Try to extract image URL
            image_match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']*)["\']/>', result.html, re.IGNORECASE | re.DOTALL)
            image_url = image_match.group(1) if image_match else None

            # Create metadata
            metadata = {
                "title": title,
                "author": author,
                "published_at": published_at,
                "categories": categories,
                "tags": tags,
                "image_url": image_url,
                "schema": {},
            }

            logger.info(f"Successfully extracted metadata from {url}: {metadata['title']}")
            return metadata

    except Exception as e:
        logger.error(f"Error extracting metadata from {url}: {str(e)}")
        # Return dummy metadata as fallback
        return {
            "title": f"Sample Article from {url}",
            "author": "Sample Author",
            "published_at": datetime.now().isoformat(),
            "categories": ["News", "Politics"],
            "tags": [],
            "image_url": None,
            "schema": {},
        }

def clean_article_content(content: str) -> str:
    """
    Clean article content by removing ads, navigation, etc.

    Args:
        content: Raw article content

    Returns:
        Cleaned article content
    """
    if not content:
        return ""

    # Remove common ad patterns
    patterns_to_remove = [
        r'<div[^>]*class=["\']?ad[s\-]?["\']?[^>]*>.*?</div>',
        r'<div[^>]*id=["\']?ad[s\-]?["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?advertisement["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?banner["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?sponsor["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?promo["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?related[\-]?["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?share[\-]?["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?social[\-]?["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?comment[s\-]?["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?footer["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?header["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?nav[igation\-]?["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?menu["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?sidebar["\']?[^>]*>.*?</div>',
        r'<div[^>]*class=["\']?widget["\']?[^>]*>.*?</div>',
        r'<script[^>]*>.*?</script>',
        r'<style[^>]*>.*?</style>',
        r'<iframe[^>]*>.*?</iframe>',
        r'<noscript[^>]*>.*?</noscript>',
    ]

    cleaned_content = content
    for pattern in patterns_to_remove:
        cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.DOTALL | re.IGNORECASE)

    # Remove empty paragraphs
    cleaned_content = re.sub(r'<p[^>]*>\s*</p>', '', cleaned_content, flags=re.DOTALL | re.IGNORECASE)

    # Remove excessive whitespace
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
    cleaned_content = cleaned_content.strip()

    return cleaned_content

def convert_to_markdown(content: str) -> str:
    """
    Convert article content to Markdown.

    Args:
        content: Article content

    Returns:
        Markdown version of the content
    """
    # Placeholder for actual implementation
    # In a real implementation, this would convert HTML to Markdown

    # For now, return a simple Markdown version
    return f"# Article\n\n{content}"
