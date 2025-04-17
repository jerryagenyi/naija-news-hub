"""
Main scraper module for Naija News Hub.

This module provides the main entry point for the scraper.
"""

import logging
from typing import List, Dict, Any, Optional

from src.database.connection import SessionLocal
from src.services import ArticleService
from src.database.repositories import WebsiteRepository, ScrapingRepository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def scrape_website(website_id: int, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Scrape a website and extract articles.

    Args:
        website_id: ID of the website to scrape
        config: Optional configuration for the scraper

    Returns:
        Dict containing scraping results
    """
    # Create a database session
    db = SessionLocal()

    try:
        # Create repositories
        website_repo = WebsiteRepository(db)
        scraping_repo = ScrapingRepository(db)
        article_service = ArticleService(db)

        # Get website from database
        website = website_repo.get_website_by_id(website_id)
        if not website:
            raise ValueError(f"Website with ID {website_id} not found")

        # Create scraping job
        job_data = {
            "website_id": website_id,
            "status": "pending",
            "config": config or {}
        }
        job = scraping_repo.create_job(job_data)

        # Start job
        job = scraping_repo.start_job(job.id)

        logger.info(f"Starting scraping job {job.id} for website {website.name} ({website.base_url})")

        try:
            # Use the article service to discover and store articles
            result = await article_service.discover_and_store_articles(website_id)

            logger.info(f"Completed scraping job {job.id} for website {website.name}")

            return {
                "job_id": job.id,
                "website_id": website_id,
                "articles_found": result.get("articles_found", 0),
                "articles_stored": result.get("articles_stored", 0),
                "articles_existing": result.get("articles_existing", 0),
                "articles_failed": result.get("articles_failed", 0),
                "status": "completed" if result.get("status") == "success" else "failed",
                "message": result.get("message", "")
            }

        except Exception as e:
            # Update job status on error
            scraping_repo.fail_job(job.id, str(e))

            logger.error(f"Error in scraping job {job.id}: {str(e)}")
            raise

    finally:
        db.close()

async def scrape_all_websites(config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Scrape all active websites.

    Args:
        config: Optional configuration for the scraper

    Returns:
        List of dictionaries containing scraping results for each website
    """
    # Create a database session
    db = SessionLocal()

    try:
        # Create repositories
        website_repo = WebsiteRepository(db)

        # Get all active websites
        websites = website_repo.get_all_websites(active_only=True)

        results = []
        for website in websites:
            try:
                result = await scrape_website(website.id, config)
                results.append(result)
            except Exception as e:
                logger.error(f"Error scraping website {website.name}: {str(e)}")
                results.append({
                    "website_id": website.id,
                    "status": "failed",
                    "error": str(e),
                })

        return results

    finally:
        db.close()
