#!/usr/bin/env python3
"""
Script to scrape articles from Blueprint.ng and store them in the database.
This script includes a workaround for the datetime issue.
"""

import sys
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

# Add the project root to the Python path
sys.path.append(".")

from src.database_management.connection import get_db
from src.database_management.repositories import WebsiteRepository, ArticleRepository
from src.web_scraper.article_extractor import extract_article
from src.utility_modules.datetime_utils import parse_datetime, convert_to_db_datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def scrape_blueprint():
    """Scrape articles from Blueprint.ng and store them in the database."""
    # Get database session
    db = next(get_db())
    
    # Create repositories
    website_repo = WebsiteRepository(db)
    article_repo = ArticleRepository(db)
    
    # Get website ID for Blueprint.ng
    website = website_repo.get_website_by_base_url("https://blueprint.ng")
    if not website:
        logger.error("Blueprint.ng website not found in the database")
        return
    
    website_id = website.id
    base_url = website.base_url
    
    logger.info(f"Scraping articles from {base_url} (ID: {website_id})")
    
    # Use specific article URLs from Blueprint.ng
    urls = [
        "https://blueprint.ng/csos-laud-tinubu-matawalle-for-progress-in-fight-against-insecurity/",
        "https://blueprint.ng/maikalangus-defection-to-apc-game-changer-for-amac-residents-bravo-oluohu/",
        "https://blueprint.ng/nerc-electricity-value-chain-and-power-sector-overview/",
        "https://blueprint.ng/easter-imbibe-spirit-of-love-togetherness-nnpp-chieftain-urges-nigerians/",
        "https://blueprint.ng/we-have-expanded-access-to-tertiary-education-in-kaduna-state-gov-sani/"
    ]
    logger.info(f"Using {len(urls)} specific URLs from {base_url}")
    
    # Extract articles
    articles_found = 0
    articles_stored = 0
    articles_failed = 0
    
    for url in urls:
        try:
            # Extract article
            article_data = await extract_article(url, website_id)
            articles_found += 1
            
            if not article_data:
                logger.error(f"Failed to extract article: {url}")
                articles_failed += 1
                continue
            
            # Fix the published_at field
            if isinstance(article_data["published_at"], str):
                article_data["published_at"] = parse_datetime(article_data["published_at"])
            
            # Prepare article data for database
            db_article_data = {
                "title": article_data.get("title", "Untitled"),
                "url": url,
                "content": article_data.get("content", ""),
                "content_markdown": article_data.get("content_markdown", ""),
                "content_html": article_data.get("content_html", ""),
                "author": article_data.get("author", "Unknown"),
                "published_at": convert_to_db_datetime(article_data.get("published_at")),
                "image_url": article_data.get("image_url", ""),
                "website_id": website_id,
                "article_metadata": article_data.get("article_metadata", {}),
                "last_checked_at": datetime.now(timezone.utc)
            }
            
            # Check if article already exists
            existing_article = article_repo.get_article_by_url(url)
            if existing_article:
                logger.info(f"Article already exists: {url}")
                continue
            
            # Store article in database
            article = article_repo.create_article(db_article_data)
            articles_stored += 1
            
            logger.info(f"Successfully stored article: {url}")
            
        except Exception as e:
            logger.error(f"Error extracting and storing article {url}: {str(e)}")
            articles_failed += 1
    
    # Log results
    logger.info(f"Scraping results:")
    logger.info(f"  Articles found: {articles_found}")
    logger.info(f"  Articles stored: {articles_stored}")
    logger.info(f"  Articles failed: {articles_failed}")
    
    return {
        "articles_found": articles_found,
        "articles_stored": articles_stored,
        "articles_failed": articles_failed
    }

if __name__ == "__main__":
    asyncio.run(scrape_blueprint())
