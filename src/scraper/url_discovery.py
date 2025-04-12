"""
URL discovery module for Naija News Hub.

This module provides functions to discover article URLs from news websites.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def discover_urls(base_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from a website.
    
    Args:
        base_url: Base URL of the website
        config: Optional configuration for URL discovery
        
    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from {base_url}")
    
    # Placeholder for actual implementation
    # In a real implementation, this would use Crawl4AI to discover URLs
    
    # For now, return a list of dummy URLs
    return [
        urljoin(base_url, f"/article/{i}") for i in range(1, 11)
    ]

async def discover_urls_from_sitemap(sitemap_url: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from a sitemap.
    
    Args:
        sitemap_url: URL of the sitemap
        config: Optional configuration for sitemap parsing
        
    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from sitemap {sitemap_url}")
    
    # Placeholder for actual implementation
    # In a real implementation, this would parse the sitemap XML
    
    # For now, return an empty list
    return []

async def discover_urls_from_category_pages(base_url: str, category_urls: List[str], config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Discover article URLs from category pages.
    
    Args:
        base_url: Base URL of the website
        category_urls: List of category page URLs
        config: Optional configuration for category page parsing
        
    Returns:
        List of discovered article URLs
    """
    logger.info(f"Discovering URLs from {len(category_urls)} category pages")
    
    # Placeholder for actual implementation
    # In a real implementation, this would parse each category page
    
    # For now, return an empty list
    return []

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
    
    return True
