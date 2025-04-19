#!/usr/bin/env python3
"""
Script to scrape articles from Blueprint.ng and store them in the database.
"""

import sys
import asyncio
import logging
from typing import List, Dict, Any, Optional

# Add the project root to the Python path
sys.path.append(".")

from src.database_management.connection import get_db
from src.database_management.repositories import WebsiteRepository
from src.service_layer.article_service import ArticleService
from src.web_scraper.url_discovery import discover_urls
from src.web_scraper.article_extractor import extract_article

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

    # Create repositories and services
    website_repo = WebsiteRepository(db)
    article_service = ArticleService(db)

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

    # Extract and store articles
    results = await article_service.extract_and_store_article_batch(urls, website_id)

    # Log results
    logger.info(f"Scraping results:")
    logger.info(f"  Articles found: {results.get('articles_found', 0)}")
    logger.info(f"  Articles stored: {results.get('articles_stored', 0)}")
    logger.info(f"  Articles existing: {results.get('articles_existing', 0)}")
    logger.info(f"  Articles failed: {results.get('articles_failed', 0)}")
    logger.info(f"  Status: {results.get('status', 'unknown')}")
    logger.info(f"  Message: {results.get('message', 'No message')}")

    return results

if __name__ == "__main__":
    asyncio.run(scrape_blueprint())
