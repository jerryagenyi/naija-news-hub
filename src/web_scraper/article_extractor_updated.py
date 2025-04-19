"""
Article extraction module for Naija News Hub.

This module provides functions to extract article content from news websites.
"""

import logging
import re
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode
)
from config.config import get_config
from playwright.async_api import Error as PlaywrightError
from src.utility_modules.error_handling import ScrapingErrorHandler
from src.utility_modules.content_validation import validate_article_content
from src.web_scraper.category_extractor import extract_categories_from_html, extract_tags_from_html, categorize_article
from src.web_scraper.extraction_strategies_updated import get_extraction_strategy_for_website, get_fallback_extraction_strategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ArticleExtractor:
    """Article extractor class."""

    def __init__(self):
        """Initialize the article extractor."""
        self.error_handler = ScrapingErrorHandler()

    async def extract_article(self, url: str, website_id: int, config: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Extract article content from a URL.

        Args:
            url: URL of the article
            website_id: ID of the website
            config: Optional configuration for article extraction

        Returns:
            Optional[Dict[str, Any]]: Extracted article data if successful, None otherwise
        """
        logger.info(f"Extracting article from {url}")

        # Get configuration
        app_config = get_config()
        crawl_config = app_config.crawl4ai

        # Create browser config
        browser_config = BrowserConfig(
            headless=True,
            user_agent=config.get("user_agent", crawl_config.user_agent) if config else crawl_config.user_agent,
            memory_limit="adaptive",  # Adaptive memory management
            viewport={"width": 1280, "height": 800},
            timeout=30000  # 30 seconds timeout
        )

        # Get extraction strategy for the website
        extraction_strategy = get_extraction_strategy_for_website(website_id)
        if not extraction_strategy:
            logger.warning(f"No extraction strategy found for website ID {website_id}, using fallback strategy")
            extraction_strategy = get_fallback_extraction_strategy()

        # Create crawler run config
        crawler_run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            css_selector="article, .article, .post, .content, main",  # Common article selectors
            excluded_selector="nav, footer, header, .sidebar, .menu, .navigation, .comments, .related, .social, .share",
            excluded_tags=["script", "style", "noscript", "iframe"],
            scan_full_page=True,
            wait_until="networkidle",
            extraction_strategy=extraction_strategy,
            fit_markdown=True,  # Enable fit markdown for better content extraction
            word_count_threshold=50,  # Minimum word count for content blocks
            screenshot=False,  # Set to True if you want screenshots
            exclude_external_images=False  # Include external images
        )

        try:
            # Create AsyncWebCrawler
            async with AsyncWebCrawler(config=browser_config) as crawler:
                # Extract article
                result = await crawler.arun(url, config=crawler_run_config)

                if not result.success:
                    logger.error(f"Failed to extract article from {url}: {result.error_message}")
                    return None

                # Extract content from the result
                content_html = result.cleaned_html or ""
                
                # Use fit_markdown for better content extraction if available
                content_markdown = result.markdown.fit_markdown if result.markdown and hasattr(result.markdown, 'fit_markdown') else \
                                  result.markdown.raw_markdown if result.markdown else ""

                # Calculate word count and reading time
                word_count = len(re.findall(r'\\w+', content_html)) if content_html else 0
                reading_time = max(1, word_count // 200)  # Assuming 200 words per minute reading speed

                # Get extracted data from the extraction strategy
                extracted_data = result.extracted_data or {}

                # Get title from extraction strategy or fallback to HTML title
                title = extracted_data.get("title")
                if not title:
                    title_match = re.search(r'<title>(.*?)</title>', result.html, re.IGNORECASE | re.DOTALL)
                    title = title_match.group(1) if title_match else f"Article from {url}"

                # Get author from extraction strategy or fallback to meta tag
                author = extracted_data.get("author")
                if not author or author == "Unknown Author":
                    author_match = re.search(r'<meta\\s+name=["\']author["\'](\\s+content=|>)["\'](.*?)["\'](/?>|\\s)', result.html, re.IGNORECASE | re.DOTALL)
                    author = author_match.group(2) if author_match else "Unknown Author"

                # Get published date from extraction strategy or fallback to meta tag
                published_at = extracted_data.get("published_date")
                if not published_at:
                    date_match = re.search(r'<meta\\s+property=["\']article:published_time["\'](\\s+content=|>)["\'](.*?)["\'](/?>|\\s)', result.html, re.IGNORECASE | re.DOTALL)
                    published_at = date_match.group(2) if date_match else datetime.now(timezone.utc).isoformat()

                # Get image URL from extraction strategy or fallback to first image
                image_url = extracted_data.get("image_url")
                # Try to find image URLs in the media if not found in extraction strategy
                if not image_url and result.media and 'images' in result.media and result.media['images']:
                    # Use the first image with the highest score
                    images = sorted(result.media['images'], key=lambda x: x.get('score', 0), reverse=True)
                    if images:
                        image_url = images[0].get('src')

                # Get categories and tags from extraction strategy
                categories = extracted_data.get("categories", [])
                tags = extracted_data.get("tags", [])

                # Create article data
                article_data = {
                    "title": title,
                    "url": url,
                    "content": content_markdown,  # Use markdown for content
                    "content_markdown": content_markdown,
                    "content_html": content_html,
                    "author": author,
                    "published_at": published_at,
                    "image_url": image_url,
                    "website_id": website_id,
                    "article_metadata": {
                        "word_count": word_count,
                        "reading_time": reading_time,
                        "categories": categories,
                        "tags": tags,
                        "schema": {},
                        "extraction_method": "strategy" if extracted_data else "fallback"
                    },
                    "active": True,
                }

                # Get website base URL for category URL generation
                website_base_url = url
                # Extract domain from URL
                parsed_url = urlparse(url)
                website_base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

                # Categorize the article if no categories were extracted
                if not categories:
                    article_data = categorize_article(article_data, website_base_url)

                # Validate article content
                validation_result = validate_article_content(article_data)
                logger.info(f"Content validation result for {url}: {validation_result}")

                # Add validation results to metadata
                article_data["article_metadata"]["validation"] = validation_result.to_dict()

                # If content is not valid, log warning
                if not validation_result.is_valid:
                    logger.warning(f"Article content validation failed for {url}: {validation_result.issues}")

                    # If validation score is too low, return None
                    if validation_result.score < 30:  # Very low quality content
                        logger.error(f"Article content quality too low for {url}: score={validation_result.score}")
                        return None

                logger.info(f"Successfully extracted article from {url}: {article_data['title']}")
                return article_data

        except PlaywrightError as pe:
            logger.error(f"Playwright error extracting article from {url}: {str(pe)}")
            # Try a fallback approach without Playwright
            try:
                # Use a simpler approach with requests and BeautifulSoup
                import requests
                from bs4 import BeautifulSoup

                # Get the page content
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract title
                title = soup.title.text if soup.title else f"Article from {url}"

                # Extract content
                content_element = soup.find('article') or soup.find(class_='post-content') or soup.find(class_='entry-content') or soup.find('main')
                content = content_element.text if content_element else "Content could not be extracted"
                content_html = str(content_element) if content_element else ""

                # Extract author
                author_element = soup.find(class_='author') or soup.find(class_='byline') or soup.find(rel='author')
                author = author_element.text if author_element else "Unknown Author"

                # Extract image
                image_element = soup.find('meta', property='og:image') or soup.find('img', class_='wp-post-image')
                image_url = image_element['content'] if image_element and 'content' in image_element.attrs else \
                           image_element['src'] if image_element and 'src' in image_element.attrs else None

                # Calculate word count and reading time
                word_count = len(content.split())
                reading_time = max(1, word_count // 200)

                logger.info(f"Successfully extracted article from {url} using fallback method")

                return {
                    "title": title,
                    "url": url,
                    "content": content,
                    "content_markdown": f"# {title}\n\n{content}",
                    "content_html": content_html,
                    "author": author,
                    "published_at": datetime.now(timezone.utc).isoformat(),
                    "image_url": image_url,
                    "website_id": website_id,
                    "article_metadata": {
                        "word_count": word_count,
                        "reading_time": reading_time,
                        "extraction_method": "fallback_requests"
                    },
                    "active": True,
                }
            except Exception as fallback_error:
                logger.error(f"Fallback extraction also failed for {url}: {str(fallback_error)}")
                # Return None instead of dummy data
                logger.error(f"Failed to extract article from {url} using both primary and fallback methods")
                return None
        except Exception as e:
            logger.error(f"Error extracting article from {url}: {str(e)}")
            # Return None instead of dummy data
            logger.error(f"Failed to extract article from {url}")
            return None

    async def extract_article_metadata(self, url: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract article metadata from a URL.

        Args:
            url: URL of the article
            config: Optional configuration for metadata extraction

        Returns:
            Dict[str, Any]: Extracted metadata
        """
        logger.info(f"Extracting metadata from {url}")

        # Get configuration
        app_config = get_config()
        crawl_config = app_config.crawl4ai

        # Create browser config
        browser_config = BrowserConfig(
            headless=True,
            user_agent=config.get("user_agent", crawl_config.user_agent) if config else crawl_config.user_agent,
            memory_limit="adaptive",
            viewport={"width": 1280, "height": 800},
            wait_until="networkidle",
            timeout=30000
        )

        # Create crawler run config optimized for metadata extraction
        crawler_run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            css_selector="head, meta, title",  # Focus on metadata in the head
            excluded_tags=["script", "style", "noscript", "iframe"],
            wait_until="networkidle",
            scan_full_page=False  # No need to scan the full page for metadata
        )

        try:
            # Create AsyncWebCrawler
            async with AsyncWebCrawler(config=browser_config) as crawler:
                # Extract article metadata
                result = await crawler.arun(url, config=crawler_run_config)

                if not result.success:
                    logger.error(f"Failed to extract metadata from {url}: {result.error_message}")
                    return {}

                # Try to extract metadata from result.metadata first (Crawl4AI's built-in metadata extraction)
                if result.metadata:
                    metadata = {
                        "title": result.metadata.get("title", ""),
                        "author": result.metadata.get("author", "Unknown"),
                        "published_at": result.metadata.get("published_date", datetime.now(timezone.utc).isoformat()),
                        "categories": result.metadata.get("categories", []),
                        "tags": result.metadata.get("tags", []),
                        "image_url": result.metadata.get("image_url", ""),
                        "description": result.metadata.get("description", ""),
                        "schema": result.metadata.get("schema", {})
                    }
                    
                    logger.info(f"Successfully extracted metadata from {url} using Crawl4AI metadata")
                    return metadata

                # Fallback to manual extraction if Crawl4AI metadata is not available
                # Try to extract title from HTML
                title_match = re.search(r'<title>(.*?)</title>', result.html, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1) if title_match else f"Article from {url}"

                # Try to extract author
                author_match = re.search(r'<meta\\s+name=["\']author["\'](\\s+content=|>)["\'](.*?)["\'](/?>|\\s)', result.html, re.IGNORECASE | re.DOTALL)
                author = author_match.group(2) if author_match else "Unknown"

                # Try to extract publication date
                date_match = re.search(r'<meta\\s+property=["\']article:published_time["\'](\\s+content=|>)["\'](.*?)["\'](/?>|\\s)', result.html, re.IGNORECASE | re.DOTALL)
                published_at = date_match.group(2) if date_match else datetime.now(timezone.utc).isoformat()

                # Extract categories and tags using the category extractor
                categories = extract_categories_from_html(result.html)
                tags = extract_tags_from_html(result.html)

                # Try to extract image URL
                image_match = re.search(r'<meta\\s+property=["\']og:image["\'](\\s+content=|>)["\'](.*?)["\'](/?>|\\s)', result.html, re.IGNORECASE | re.DOTALL)
                image_url = image_match.group(2) if image_match else None

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

                logger.info(f"Successfully extracted metadata from {url} using fallback method")
                return metadata

        except Exception as e:
            logger.error(f"Error extracting metadata from {url}: {str(e)}")
            # Return empty metadata instead of dummy data
            logger.error(f"Failed to extract metadata from {url}")
            return {}

# Create a singleton instance
article_extractor = ArticleExtractor()

async def extract_article(url: str, website_id: int, config: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Extract article content from a URL.

    Args:
        url: URL of the article
        website_id: ID of the website
        config: Optional configuration for article extraction

    Returns:
        Optional[Dict[str, Any]]: Extracted article data if successful, None otherwise
    """
    return await article_extractor.extract_article(url, website_id, config)

async def extract_article_metadata(url: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Extract article metadata from a URL.

    Args:
        url: URL of the article
        config: Optional configuration for metadata extraction

    Returns:
        Dict[str, Any]: Extracted metadata
    """
    return await article_extractor.extract_article_metadata(url, config)

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
