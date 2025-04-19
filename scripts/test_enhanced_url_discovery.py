#!/usr/bin/env python3
"""
Script to test the enhanced URL discovery functionality.
"""

import sys
import asyncio
import logging
from typing import List, Dict, Any, Optional

# Add the project root to the Python path
sys.path.append(".")

from src.web_scraper.enhanced_url_discovery import discover_urls
from src.web_scraper.enhanced_article_extractor import extract_article

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def test_url_discovery(base_url: str) -> List[str]:
    """
    Test URL discovery for a website.
    
    Args:
        base_url: Base URL of the website
        
    Returns:
        List of discovered article URLs
    """
    logger.info(f"Testing URL discovery for {base_url}")
    
    # Discover URLs
    urls = await discover_urls(base_url)
    
    logger.info(f"Discovered {len(urls)} URLs from {base_url}")
    
    # Print the first 10 URLs
    for i, url in enumerate(urls[:10]):
        logger.info(f"URL {i+1}: {url}")
    
    return urls

async def test_article_extraction(url: str, website_id: int) -> Optional[Dict[str, Any]]:
    """
    Test article extraction for a URL.
    
    Args:
        url: URL of the article
        website_id: ID of the website
        
    Returns:
        Extracted article data if successful, None otherwise
    """
    logger.info(f"Testing article extraction for {url}")
    
    # Extract article
    article_data = await extract_article(url, website_id)
    
    if article_data:
        logger.info(f"Successfully extracted article: {article_data['title']}")
        logger.info(f"Published at: {article_data['published_at']}")
        logger.info(f"Author: {article_data['author']}")
        logger.info(f"Content length: {len(article_data['content'])}")
    else:
        logger.error(f"Failed to extract article from {url}")
    
    return article_data

async def main():
    """Main function."""
    # Test URL discovery for Blueprint.ng
    base_url = "https://blueprint.ng"
    website_id = 1  # Assuming website ID 1 for Blueprint.ng
    
    # Discover URLs
    urls = await test_url_discovery(base_url)
    
    if urls:
        # Test article extraction for the first URL
        await test_article_extraction(urls[0], website_id)
    
    logger.info("Testing completed")

if __name__ == "__main__":
    asyncio.run(main())
