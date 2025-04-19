"""
URL discovery module for Naija News Hub.

This module provides functions to discover article URLs from news websites.
"""

import logging
import re
from typing import List, Dict, Any, Optional, Set
from urllib.parse import urljoin, urlparse
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from config.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def discover_urls(base_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from a website using AsyncWebCrawler.

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
    )

    # Create crawler run config
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_selector="nav, footer, header, .sidebar, .menu, .navigation",
        excluded_tags=["script", "style", "noscript", "iframe"],
        exclude_external_links=False,
        exclude_social_media_links=True,
        scan_full_page=True,
        wait_until="networkidle"
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
                urls.extend(internal_links)
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

async def discover_urls_from_sitemap(sitemap_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from a sitemap using AsyncWebCrawler.

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
    )

    # Create crawler run config with XML handling
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_selector="nav, footer, header, .sidebar, .menu, .navigation",
        excluded_tags=["script", "style", "noscript", "iframe"],
        exclude_external_links=False,
        exclude_social_media_links=True,
        wait_until="networkidle",
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

async def discover_urls_from_category_pages(base_url: str, category_urls: List[str], config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from category pages using AsyncWebCrawler.

    Args:
        base_url: Base URL of the website
        category_urls: List of category page URLs
        config: Optional configuration for category page parsing

    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from {len(category_urls)} category pages")

    # Get configuration
    app_config = get_config()
    crawl_config = app_config.crawl4ai

    # Create browser config
    browser_config = BrowserConfig(
        headless=True,
        user_agent=config.get("user_agent", crawl_config.user_agent) if config else crawl_config.user_agent,
    )

    # Create crawler run config optimized for category pages
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_selector="nav, footer, header, .sidebar, .menu, .navigation",
        excluded_tags=["script", "style", "noscript", "iframe"],
        exclude_external_links=True,  # Only interested in internal links
        exclude_social_media_links=True,
        scan_full_page=False,  # Don't scan the full page for category pages
        wait_until="networkidle"
    )

    # Discover URLs from each category page
    all_urls: Set[str] = set()
    for category_url in category_urls:
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
                    urls.extend(internal_links)
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
        "/category/", "/tag/", "/author/", "/search/", "/page/",
        "/about/", "/contact/", "/privacy/", "/terms/", "/sitemap/",
        ".xml", ".pdf", ".jpg", ".png", ".gif", ".css", ".js"
    ]

    for pattern in excluded_patterns:
        if pattern in parsed_url.path.lower():
            return False

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
    path_segments = [s for s in parsed_url.path.split('/') if s]
    if len(path_segments) >= 2 and len(path_segments[-1]) > 5 and '-' in path_segments[-1]:
        return True

    # If we have a path with a single segment that's long enough, it might be an article
    if len(path_segments) == 1 and len(path_segments[0]) > 10:
        return True

    return False
