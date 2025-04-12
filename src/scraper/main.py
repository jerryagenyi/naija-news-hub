"""
Main scraper module for Naija News Hub.

This module provides the main entry point for the scraper.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.database.connection import get_db
from src.database.models import Website, ScrapingJob, Article
from src.scraper.url_discovery import discover_urls
from src.scraper.article_extractor import extract_article

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
    db = next(get_db())
    
    try:
        # Get website from database
        website = db.query(Website).filter(Website.id == website_id).first()
        if not website:
            raise ValueError(f"Website with ID {website_id} not found")
        
        # Create scraping job
        job = ScrapingJob(
            website_id=website_id,
            status="running",
            start_time=datetime.utcnow(),
            config=config,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        logger.info(f"Starting scraping job {job.id} for website {website.name} ({website.base_url})")
        
        try:
            # Discover URLs
            urls = await discover_urls(website.base_url, config)
            job.articles_found = len(urls)
            db.commit()
            
            logger.info(f"Found {len(urls)} URLs for website {website.name}")
            
            # Extract articles
            articles_scraped = 0
            for url in urls:
                try:
                    article_data = await extract_article(url, website_id, config)
                    
                    # Check if article already exists
                    existing_article = db.query(Article).filter(Article.url == url).first()
                    if existing_article:
                        # Update existing article
                        for key, value in article_data.items():
                            setattr(existing_article, key, value)
                    else:
                        # Create new article
                        article = Article(**article_data)
                        db.add(article)
                    
                    db.commit()
                    articles_scraped += 1
                    
                    # Update job status
                    job.articles_scraped = articles_scraped
                    db.commit()
                    
                except Exception as e:
                    logger.error(f"Error extracting article from {url}: {str(e)}")
                    # Log error but continue with next URL
            
            # Update job status
            job.status = "completed"
            job.end_time = datetime.utcnow()
            db.commit()
            
            logger.info(f"Completed scraping job {job.id} for website {website.name}")
            
            return {
                "job_id": job.id,
                "website_id": website_id,
                "articles_found": job.articles_found,
                "articles_scraped": job.articles_scraped,
                "status": job.status,
            }
            
        except Exception as e:
            # Update job status on error
            job.status = "failed"
            job.end_time = datetime.utcnow()
            job.error_message = str(e)
            db.commit()
            
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
    db = next(get_db())
    
    try:
        # Get all active websites
        websites = db.query(Website).filter(Website.active == True).all()
        
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
