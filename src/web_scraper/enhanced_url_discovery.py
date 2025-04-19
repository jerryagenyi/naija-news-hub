"""
Enhanced URL discovery module for Naija News Hub.

This module provides functions to discover article URLs from news websites
with improved reliability, rate limiting, and anti-ban measures.
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
from src.web_scraper.url_discovery import is_valid_article_url
from src.web_scraper.category_discovery import discover_urls_from_category_pages

# Configure logging
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

    # Get anti-ban browser configuration
    anti_ban_browser_config = get_browser_config(base_url)
    
    # Create browser config
    browser_config = BrowserConfig(
        headless=anti_ban_browser_config.get("headless", True),
        user_agent=config.get("user_agent", anti_ban_browser_config.get("user_agent", crawl_config.user_agent)),
        viewport_width=anti_ban_browser_config.get("viewport_width", 1280),
        viewport_height=anti_ban_browser_config.get("viewport_height", 800)
    )

    # Get anti-ban crawler configuration
    anti_ban_crawler_config = get_crawler_config(base_url)
    
    # Create crawler run config
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_tags=["script", "style", "noscript", "iframe", "nav", "footer", "header", ".sidebar", ".menu", ".navigation"],
        exclude_external_links=False,
        exclude_social_media_links=True,
        word_count_threshold=0,  # No minimum word count for URL discovery
        **anti_ban_crawler_config  # Add any domain-specific crawler configuration
    )

    try:
        # Create AsyncWebCrawler
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
                logger.warning(f"No internal links found in result.links")

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
        return []

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

    # Get anti-ban browser configuration
    anti_ban_browser_config = get_browser_config(sitemap_url)
    
    # Create browser config
    browser_config = BrowserConfig(
        headless=anti_ban_browser_config.get("headless", True),
        user_agent=config.get("user_agent", anti_ban_browser_config.get("user_agent", crawl_config.user_agent)),
        viewport_width=anti_ban_browser_config.get("viewport_width", 1280),
        viewport_height=anti_ban_browser_config.get("viewport_height", 800)
    )

    # Get anti-ban crawler configuration
    anti_ban_crawler_config = get_crawler_config(sitemap_url)
    
    # Create crawler run config with XML handling
    crawler_run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_tags=["script", "style", "noscript", "iframe"],
        exclude_external_links=False,
        exclude_social_media_links=True,
        word_count_threshold=0,  # No minimum word count for sitemap
        content_type="xml",  # Specify XML content type for sitemaps
        **anti_ban_crawler_config  # Add any domain-specific crawler configuration
    )

    try:
        # Try to fetch the sitemap using aiohttp first (more reliable for XML)
        async with aiohttp.ClientSession() as session:
            # Get anti-ban headers
            headers = get_headers(sitemap_url)
            
            async with session.get(sitemap_url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Try to parse as XML
                    try:
                        root = ET.fromstring(content)
                        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                        
                        # Check if it's a sitemap index
                        sitemap_tags = root.findall('.//ns:sitemap', namespace)
                        if sitemap_tags:
                            # It's a sitemap index, extract sitemap URLs
                            sitemap_urls = []
                            for sitemap in sitemap_tags:
                                loc = sitemap.find('./ns:loc', namespace)
                                if loc is not None and loc.text:
                                    sitemap_urls.append(loc.text)
                            
                            # Recursively process each sitemap
                            all_urls = []
                            for sub_sitemap_url in sitemap_urls:
                                sub_urls = await discover_urls_from_sitemap(sub_sitemap_url, config)
                                all_urls.extend(sub_urls)
                            
                            return all_urls
                        
                        # It's a regular sitemap, extract URLs
                        urls = []
                        url_tags = root.findall('.//ns:url', namespace)
                        for url_tag in url_tags:
                            loc = url_tag.find('./ns:loc', namespace)
                            if loc is not None and loc.text:
                                urls.append(loc.text)
                        
                        # Get the base URL from the sitemap URL
                        parsed_url = urlparse(sitemap_url)
                        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                        
                        # Filter URLs to ensure they are valid article URLs
                        valid_urls = [url for url in urls if is_valid_article_url(url, base_url)]
                        
                        logger.info(f"Discovered {len(valid_urls)} valid article URLs from sitemap {sitemap_url}")
                        return valid_urls
                    except ET.ParseError:
                        # Not valid XML, fall back to Crawl4AI
                        logger.warning(f"Failed to parse sitemap {sitemap_url} as XML, falling back to Crawl4AI")
                        pass
        
        # Fall back to Crawl4AI if aiohttp fails or XML parsing fails
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

async def discover_urls_from_rss(rss_url: str) -> List[str]:
    """
    Discover article URLs from an RSS feed.

    Args:
        rss_url: URL of the RSS feed

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
        sitemap_urls = await discover_urls_from_sitemap(sitemap_url, config)
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
        rss_urls = await execute_with_rate_limit(discover_urls_from_rss, rss_url)
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
