#!/usr/bin/env python3
"""
Test script to extract 5 articles from blueprint.ng using specific URLs.
"""

import sys
import asyncio
import logging
from pprint import pprint
from typing import List, Dict, Any, Optional

# Add the project root to the Python path
sys.path.append(".")

from src.web_scraper.article_extractor import extract_article
from src.database_management.models import Website
from src.database_management.connection import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def test_blueprint_extraction():
    """Test article extraction from blueprint.ng using specific URLs."""
    # Get the website ID for blueprint.ng
    db = next(get_db())
    website = db.query(Website).filter(Website.base_url.like("%blueprint.ng%")).first()
    
    if not website:
        logger.error("Blueprint.ng website not found in the database")
        return
    
    website_id = website.id
    base_url = website.base_url
    
    logger.info(f"Testing article extraction from {base_url} (ID: {website_id})")
    
    # Use specific article URLs from blueprint.ng
    urls = [
        "https://blueprint.ng/csos-laud-tinubu-matawalle-for-progress-in-fight-against-insecurity/",
        "https://blueprint.ng/maikalangus-defection-to-apc-game-changer-for-amac-residents-bravo-oluohu/",
        "https://blueprint.ng/nerc-electricity-value-chain-and-power-sector-overview/",
        "https://blueprint.ng/easter-imbibe-spirit-of-love-togetherness-nnpp-chieftain-urges-nigerians/",
        "https://blueprint.ng/we-have-expanded-access-to-tertiary-education-in-kaduna-state-gov-sani/"
    ]
    
    logger.info(f"Selected {len(urls)} URLs for extraction")
    
    # Extract articles
    articles = []
    for url in urls:
        logger.info(f"Extracting article from {url}")
        article_data = await extract_article(url, website_id)
        
        if article_data:
            logger.info(f"Successfully extracted article: {article_data['title']}")
            articles.append(article_data)
        else:
            logger.error(f"Failed to extract article from {url}")
    
    # Print the extracted articles
    logger.info(f"Extracted {len(articles)} articles")
    for i, article in enumerate(articles):
        logger.info(f"Article {i+1}:")
        logger.info(f"Title: {article['title']}")
        logger.info(f"URL: {article['url']}")
        logger.info(f"Author: {article['author']}")
        logger.info(f"Published at: {article['published_at']}")
        logger.info(f"Word count: {article['article_metadata']['word_count']}")
        logger.info(f"Extraction method: {article['article_metadata'].get('extraction_method', 'unknown')}")
        logger.info(f"Content preview: {article['content'][:200]}...")
        logger.info("-" * 80)
    
    return articles

if __name__ == "__main__":
    asyncio.run(test_blueprint_extraction())
