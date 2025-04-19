"""
URL discovery module for Naija News Hub.

This module provides functions to discover article URLs from news websites.
"""

import logging
import re
import asyncio
from typing import List, Dict, Any, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import feedparser
import aiohttp

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from config.config import get_config
from src.utility_modules.rate_limiter import execute_with_rate_limit
from src.utility_modules.anti_ban import get_browser_config, get_headers
from src.web_scraper.category_discovery import discover_urls_from_category_pages

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def _discover_urls_internal(base_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Internal function to discover article URLs from a website using AsyncWebCrawler.

    Args:
        base_url: Base URL of the website
        config: Optional configuration for URL discovery

    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from {base_url}")

    # Get configuration
    app_config = get_config()
    crawl_config = app_config.crawl4ai

    # Create browser config
    browser_config = BrowserConfig(
        headless=True,
        user_agent=config.get("user_agent", crawl_config.user_agent) if config else crawl_config.user_agent,
        viewport_width=1280,
        viewport_height=800
    )

    # Create crawler run config
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_tags=["script", "style", "noscript", "iframe", "nav", "footer", "header", ".sidebar", ".menu", ".navigation"],
        exclude_external_links=False,
        exclude_social_media_links=True,
        word_count_threshold=0  # No minimum word count for URL discovery
    )

    # Create AsyncWebCrawler
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # Crawl the website
            result = await crawler.arun(base_url, config=crawler_run_config)

            # Extract links from the result using Crawl4AI's built-in link extraction
            urls = []

            # Use result.links which contains all links found on the page
            if result.links and isinstance(result.links, dict) and 'internal' in result.links:
                # Get internal links (same domain)
                internal_links = result.links['internal']
                logger.info(f"Found {len(internal_links)} internal links")

                # Add all internal links to our list
                for link in internal_links:
                    if isinstance(link, str):
                        urls.append(link)
                    elif isinstance(link, dict) and 'url' in link:
                        urls.append(link['url'])
            else:
                logger.warning(f"No internal links found in result.links: {result.links}")

                # Fallback to HTML parsing if no links found
                if result.html:
                    # Use regex to find all URLs in the HTML
                    url_pattern = r'href=["\']((?!javascript)[^"\']+)["\']'
                    found_urls = re.findall(url_pattern, result.html)
                    logger.info(f"Found {len(found_urls)} URLs in HTML using fallback method")

                    # Process the URLs
                    for url in found_urls:
                        # Convert relative URLs to absolute URLs
                        if url.startswith('/'):
                            url = urljoin(base_url, url)
                        # Add the URL to the list
                        urls.append(url)

            # Filter URLs to ensure they are valid article URLs
            valid_urls = [url for url in urls if is_valid_article_url(url, base_url)]

            logger.info(f"Discovered {len(valid_urls)} valid article URLs from {base_url}")
            return valid_urls

    except Exception as e:
        logger.error(f"Error discovering URLs from {base_url}: {str(e)}")
        # Return an empty list instead of dummy URLs
        logger.warning(f"Failed to discover URLs from {base_url}, returning empty list")
        return []

async def discover_urls_from_rss(rss_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from an RSS feed.

    Args:
        rss_url: URL of the RSS feed
        config: Optional configuration for RSS feed parsing

    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from RSS feed {rss_url}")

    try:
        # Use aiohttp to fetch the RSS feed
        async with aiohttp.ClientSession() as session:
            # Get anti-ban headers
            headers = get_headers(rss_url)

            async with session.get(rss_url, headers=headers, timeout=30) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch RSS feed {rss_url}: HTTP {response.status}")
                    return []

                content = await response.text()

                # Parse the RSS feed
                feed = feedparser.parse(content)

                # Extract URLs from the feed
                urls = []
                for entry in feed.entries:
                    if hasattr(entry, 'link'):
                        urls.append(entry.link)

                # Get the base URL from the RSS URL
                parsed_url = urlparse(rss_url)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

                # Filter URLs to ensure they are valid article URLs
                valid_urls = [url for url in urls if is_valid_article_url(url, base_url)]

                logger.info(f"Discovered {len(valid_urls)} valid article URLs from RSS feed {rss_url}")
                return valid_urls

    except Exception as e:
        logger.error(f"Error parsing RSS feed {rss_url}: {str(e)}")
        return []

async def discover_urls(base_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from a website using multiple methods.

    Args:
        base_url: Base URL of the website
        config: Optional configuration for URL discovery

    Returns:
        List of discovered article URLs
    """
    logger.info(f"Starting comprehensive URL discovery for {base_url}")

    # Use a set to store unique URLs
    all_urls: Set[str] = set()

    # 1. Try to discover URLs from the main page
    main_page_urls = await execute_with_rate_limit(_discover_urls_internal, base_url, config)
    all_urls.update(main_page_urls)
    logger.info(f"Discovered {len(main_page_urls)} URLs from main page")

    # 2. Try to discover URLs from common sitemap locations
    sitemap_locations = [
        f"{base_url}/sitemap.xml",
        f"{base_url}/sitemap_index.xml",
        f"{base_url}/sitemap-index.xml",
        f"{base_url}/post-sitemap.xml",
        f"{base_url}/page-sitemap.xml",
        f"{base_url}/news-sitemap.xml",
    ]

    for sitemap_url in sitemap_locations:
        sitemap_urls = await execute_with_rate_limit(discover_urls_from_sitemap, sitemap_url, config)
        all_urls.update(sitemap_urls)
        logger.info(f"Discovered {len(sitemap_urls)} URLs from sitemap {sitemap_url}")

    # 3. Try to discover URLs from common RSS feed locations
    rss_locations = [
        f"{base_url}/feed",
        f"{base_url}/rss",
        f"{base_url}/feed/rss",
        f"{base_url}/rss.xml",
        f"{base_url}/atom.xml",
        f"{base_url}/feed/atom",
    ]

    for rss_url in rss_locations:
        rss_urls = await execute_with_rate_limit(discover_urls_from_rss, rss_url, config)
        all_urls.update(rss_urls)
        logger.info(f"Discovered {len(rss_urls)} URLs from RSS feed {rss_url}")

    # 4. Try to discover category pages
    category_patterns = [
        f"{base_url}/category/",
        f"{base_url}/categories/",
        f"{base_url}/topics/",
        f"{base_url}/sections/",
    ]

    category_urls = []
    for pattern in category_patterns:
        # Check if the pattern exists on the main page
        for url in main_page_urls:
            if url.startswith(pattern):
                category_urls.append(url)

    # 5. If we found category pages, discover URLs from them
    if category_urls:
        category_page_urls = await discover_urls_from_category_pages(base_url, category_urls, config)
        all_urls.update(category_page_urls)
        logger.info(f"Discovered {len(category_page_urls)} URLs from {len(category_urls)} category pages")

    # Convert set to list and return
    result = list(all_urls)
    logger.info(f"Total unique URLs discovered: {len(result)}")
    return result

async def _discover_urls_from_sitemap_internal(sitemap_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Internal function to discover article URLs from a sitemap using AsyncWebCrawler.

    Args:
        sitemap_url: URL of the sitemap
        config: Optional configuration for sitemap parsing

    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from sitemap {sitemap_url}")

    # Get configuration
    app_config = get_config()
    crawl_config = app_config.crawl4ai

    # Create browser config
    browser_config = BrowserConfig(
        headless=True,
        user_agent=config.get("user_agent", crawl_config.user_agent) if config else crawl_config.user_agent,
        viewport_width=1280,
        viewport_height=800
    )

    # Create crawler run config with XML handling
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_tags=["script", "style", "noscript", "iframe"],
        exclude_external_links=False,
        exclude_social_media_links=True,
        word_count_threshold=0,  # No minimum word count for sitemap
        content_type="xml"  # Specify XML content type for sitemaps
    )

    # Create AsyncWebCrawler
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # Crawl the sitemap
            result = await crawler.arun(sitemap_url, config=crawler_run_config)

            # Extract links from the result
            urls = []

            # For sitemaps, look for <loc> tags which contain URLs
            if result.html:
                # Use regex to find all URLs in <loc> tags
                url_pattern = r'<loc>([^<]+)</loc>'
                found_urls = re.findall(url_pattern, result.html)
                logger.info(f"Found {len(found_urls)} URLs in sitemap")
                urls.extend(found_urls)

            # Get the base URL from the sitemap URL
            parsed_url = urlparse(sitemap_url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

            # Filter URLs to ensure they are valid article URLs
            valid_urls = [url for url in urls if is_valid_article_url(url, base_url)]

            logger.info(f"Discovered {len(valid_urls)} valid article URLs from sitemap {sitemap_url}")
            return valid_urls

    except Exception as e:
        logger.error(f"Error parsing sitemap {sitemap_url}: {str(e)}")
        return []

async def discover_urls_from_sitemap(sitemap_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from a sitemap with rate limiting and retries.

    Args:
        sitemap_url: URL of the sitemap
        config: Optional configuration for sitemap parsing

    Returns:
        List of discovered article URLs
    """
    return await execute_with_rate_limit(_discover_urls_from_sitemap_internal, sitemap_url, config)

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

                # Add to the set of all URLs
                all_urls.update(valid_urls)

                logger.info(f"Discovered {len(valid_urls)} valid article URLs from category page {category_url}")

        except Exception as e:
            logger.error(f"Error discovering URLs from category page {category_url}: {str(e)}")

    # Convert set to list and return
    return list(all_urls)

def is_valid_article_url(url: str, base_url: str) -> bool:
    """
    Check if a URL is a valid article URL.

    Args:
        url: URL to check
        base_url: Base URL of the website

    Returns:
        True if the URL is a valid article URL, False otherwise
    """
    # Parse the URL
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)

    # Check if the URL is from the same domain
    if parsed_url.netloc != parsed_base.netloc:
        return False

    # Check if the URL has a path
    if not parsed_url.path or parsed_url.path == "/":
        return False

    # Check if the URL is not a category page, tag page, etc.
    excluded_patterns = [
        "/wp-content/", "/wp-includes/", "/wp-admin/", "/feed/", "/comments/",
        "/login/", "/register/", "/logout/", "/admin/", "/wp-json/",
        ".xml", ".pdf", ".jpg", ".png", ".gif", ".css", ".js"
    ]

    for pattern in excluded_patterns:
        if pattern in parsed_url.path.lower():
            return False

    # For Blueprint.ng, most articles are directly under the root
    # with a slug format like /some-article-title-123
    path_segments = [s for s in parsed_url.path.split('/') if s]

    # If the path has a single segment with dashes (slug-like), it's likely an article
    if len(path_segments) == 1 and '-' in path_segments[0] and len(path_segments[0]) > 5:
        return True

    # Check if the URL has a date pattern (common in news articles)
    date_patterns = [
        r'/\d{4}/\d{2}/\d{2}/',  # /YYYY/MM/DD/
        r'/\d{4}-\d{2}-\d{2}/',  # /YYYY-MM-DD/
        r'/\d{2}-\d{2}-\d{4}/',  # /DD-MM-YYYY/
        r'/\d{2}/\d{2}/\d{4}/',  # /DD/MM/YYYY/
    ]

    # If the URL has a date pattern, it's likely an article
    for pattern in date_patterns:
        if re.search(pattern, parsed_url.path):
            return True

    # Check for common article indicators in the path
    article_indicators = [
        '/article/', '/news/', '/story/', '/post/', '/read/',
        '/opinion/', '/editorial/', '/feature/', '/analysis/',
        '/politics/', '/business/', '/sports/', '/entertainment/',
        '/lifestyle/', '/health/', '/technology/', '/science/',
        '/education/', '/crime/', '/metro/', '/national/', '/world/'
    ]

    for indicator in article_indicators:
        if indicator in parsed_url.path.lower():
            return True

    # If the path has at least 2 segments and the last segment looks like a slug
    # (e.g., /news/my-article-title-123), it's likely an article
    if len(path_segments) >= 2 and len(path_segments[-1]) > 5 and '-' in path_segments[-1]:
        return True

    # For Blueprint.ng, we'll be more lenient and accept most URLs that aren't in excluded patterns
    if "blueprint.ng" in base_url:
        # Exclude common non-article pages
        non_article_pages = [
            "/about", "/contact", "/privacy", "/terms", "/sitemap", "/advertise",
            "/category", "/tag", "/author", "/search", "/page", "/wp-login", "/wp-admin",
            "/feed", "/comments", "/trackback", "/wp-content", "/wp-includes", "/wp-json"
        ]

        # Check if the path starts with any of the non-article pages
        for page in non_article_pages:
            if parsed_url.path.lower().startswith(page):
                return False

        # Check for pagination patterns which are not articles
        pagination_patterns = [
            r'/page/\d+',
            r'\?page=\d+',
            r'&page=\d+'
        ]

        for pattern in pagination_patterns:
            if re.search(pattern, parsed_url.path.lower()) or re.search(pattern, parsed_url.query.lower()):
                return False

        # Check for query parameters that indicate non-article pages
        if parsed_url.query:
            non_article_params = ['s=', 'search=', 'filter=', 'sort=', 'order=']
            for param in non_article_params:
                if param in parsed_url.query.lower():
                    return False

        # Accept URLs with a slug-like pattern (words separated by hyphens)
        slug_pattern = r'/[a-z0-9\-]+/$'
        if re.search(slug_pattern, parsed_url.path.lower() + '/'):
            return True

        # Accept most other URLs as potential articles if they have a reasonable path length
        if len(parsed_url.path) > 10 and parsed_url.path.count('/') <= 2:
            return True

    return False
