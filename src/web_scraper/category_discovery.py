"""
Category discovery module for Naija News Hub.

This module provides functions to discover article URLs from category pages.
"""

import logging
import re
from typing import List, Dict, Any, Optional, Set
from urllib.parse import urljoin, urlparse

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from config.config import get_config
from src.utility_modules.rate_limiter import execute_with_rate_limit
from src.utility_modules.anti_ban import get_browser_config, get_crawler_config
from src.web_scraper.url_discovery import is_valid_article_url

# Configure logging
logger = logging.getLogger(__name__)

async def _discover_urls_from_category_page_internal(category_url: str, base_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Internal function to discover article URLs from a category page using AsyncWebCrawler.

    Args:
        category_url: URL of the category page
        base_url: Base URL of the website
        config: Optional configuration for category page parsing

    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from category page {category_url}")

    # Get configuration
    app_config = get_config()
    crawl_config = app_config.crawl4ai

    # Get anti-ban browser configuration
    anti_ban_browser_config = get_browser_config(category_url)
    
    # Create browser config
    browser_config = BrowserConfig(
        headless=anti_ban_browser_config.get("headless", True),
        user_agent=config.get("user_agent", anti_ban_browser_config.get("user_agent", crawl_config.user_agent)),
        viewport_width=anti_ban_browser_config.get("viewport_width", 1280),
        viewport_height=anti_ban_browser_config.get("viewport_height", 800)
    )

    # Get anti-ban crawler configuration
    anti_ban_crawler_config = get_crawler_config(category_url)
    
    # Create crawler run config optimized for category pages
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_tags=["script", "style", "noscript", "iframe", "nav", "footer", "header", ".sidebar", ".menu", ".navigation"],
        exclude_external_links=True,  # Only interested in internal links
        exclude_social_media_links=True,
        word_count_threshold=0,  # No minimum word count for URL discovery
        **anti_ban_crawler_config  # Add any domain-specific crawler configuration
    )

    # Discover URLs from the category page
    try:
        # Create AsyncWebCrawler
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # Crawl the category page
            result = await crawler.arun(category_url, config=crawler_run_config)

            # Extract links from the result using Crawl4AI's built-in link extraction
            urls = []

            # Use result.links which contains all links found on the page
            if result.links and isinstance(result.links, dict) and 'internal' in result.links:
                # Get internal links (same domain)
                internal_links = result.links['internal']
                logger.info(f"Found {len(internal_links)} internal links for category {category_url}")

                # Add all internal links to our list
                for link in internal_links:
                    if isinstance(link, str):
                        urls.append(link)
                    elif isinstance(link, dict) and 'url' in link:
                        urls.append(link['url'])
            else:
                logger.warning(f"No internal links found in result.links for category {category_url}")

                # Fallback to HTML parsing if no links found
                if result.html:
                    # Use regex to find all URLs in the HTML
                    url_pattern = r'href=["\']((?!javascript)[^"\']+)["\']'
                    found_urls = re.findall(url_pattern, result.html)
                    logger.info(f"Found {len(found_urls)} URLs in HTML using fallback method for category {category_url}")

                    # Process the URLs
                    for url in found_urls:
                        # Convert relative URLs to absolute URLs
                        if url.startswith('/'):
                            url = urljoin(category_url, url)
                        # Add the URL to the list
                        urls.append(url)

            # Filter URLs to ensure they are valid article URLs
            valid_urls = [url for url in urls if is_valid_article_url(url, base_url)]

            logger.info(f"Discovered {len(valid_urls)} valid article URLs from category page {category_url}")
            return valid_urls

    except Exception as e:
        logger.error(f"Error discovering URLs from category page {category_url}: {str(e)}")
        return []

async def discover_urls_from_category_page(category_url: str, base_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from a category page with rate limiting and retries.

    Args:
        category_url: URL of the category page
        base_url: Base URL of the website
        config: Optional configuration for category page parsing

    Returns:
        List of discovered article URLs
    """
    return await execute_with_rate_limit(_discover_urls_from_category_page_internal, category_url, base_url, config)

async def discover_urls_from_category_pages(base_url: str, category_urls: List[str], config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from multiple category pages with rate limiting and retries.

    Args:
        base_url: Base URL of the website
        category_urls: List of category page URLs
        config: Optional configuration for category page parsing

    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from {len(category_urls)} category pages")
    
    # Use a set to store unique URLs
    all_urls: Set[str] = set()
    
    # Process each category page
    for category_url in category_urls:
        urls = await discover_urls_from_category_page(category_url, base_url, config)
        all_urls.update(urls)
        
    # Convert set to list and return
    result = list(all_urls)
    logger.info(f"Discovered {len(result)} unique URLs from {len(category_urls)} category pages")
    return result
