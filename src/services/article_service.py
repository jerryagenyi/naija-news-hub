"""
Article service module for Naija News Hub.

This module provides services to extract and store articles.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session

from src.database.repositories import ArticleRepository, WebsiteRepository, ScrapingRepository
from src.scraper.article_extractor import extract_article
from src.scraper.url_discovery import discover_urls
from config.config import get_config

# Configure logging
logger = logging.getLogger(__name__)

class ArticleService:
    """Service for article operations."""

    def __init__(self, db: Session):
        """
        Initialize the service with a database session.
        
        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db
        self.article_repo = ArticleRepository(db)
        self.website_repo = WebsiteRepository(db)
        self.scraping_repo = ScrapingRepository(db)
        self.config = get_config()

    async def extract_and_store_article(self, url: str, website_id: int) -> Optional[Dict[str, Any]]:
        """
        Extract an article from a URL and store it in the database.
        
        Args:
            url (str): Article URL
            website_id (int): Website ID
            
        Returns:
            Optional[Dict[str, Any]]: Extracted article data if successful, None otherwise
        """
        try:
            # Check if article already exists
            existing_article = self.article_repo.get_article_by_url(url)
            if existing_article:
                logger.info(f"Article already exists: {url}")
                return {
                    "id": existing_article.id,
                    "title": existing_article.title,
                    "url": existing_article.url,
                    "status": "existing"
                }
                
            # Extract article
            article_data = await extract_article(url, website_id)
            if not article_data:
                logger.error(f"Failed to extract article: {url}")
                return None
                
            # Prepare article data for database
            db_article_data = {
                "title": article_data.get("title", "Untitled"),
                "url": url,
                "content": article_data.get("content", ""),
                "content_markdown": article_data.get("content_markdown", ""),
                "content_html": article_data.get("content_html", ""),
                "author": article_data.get("author", "Unknown"),
                "published_at": article_data.get("published_at", datetime.utcnow()),
                "image_url": article_data.get("image_url", ""),
                "website_id": website_id,
                "article_metadata": article_data.get("metadata", {})
            }
            
            # Store article in database
            article = self.article_repo.create_article(db_article_data)
            
            # Add categories if available
            categories = article_data.get("categories", [])
            for category_name in categories:
                # Try to find existing category
                category = self.website_repo.get_category_by_name(website_id, category_name)
                if not category:
                    # Create new category
                    category_url = f"{self.website_repo.get_website_by_id(website_id).base_url}/category/{category_name.lower().replace(' ', '-')}"
                    category = self.website_repo.create_category(website_id, {
                        "name": category_name,
                        "url": category_url
                    })
                
                # Add category to article
                self.article_repo.add_article_category(article.id, category.id)
            
            logger.info(f"Successfully extracted and stored article: {url}")
            return {
                "id": article.id,
                "title": article.title,
                "url": article.url,
                "status": "new"
            }
        except Exception as e:
            logger.error(f"Error extracting and storing article {url}: {str(e)}")
            return None

    async def discover_and_store_articles(self, website_id: int) -> Dict[str, Any]:
        """
        Discover articles from a website and store them in the database.
        
        Args:
            website_id (int): Website ID
            
        Returns:
            Dict[str, Any]: Results of the discovery and storage process
        """
        try:
            # Get website
            website = self.website_repo.get_website_by_id(website_id)
            if not website:
                logger.error(f"Website not found: {website_id}")
                return {
                    "status": "error",
                    "message": f"Website not found: {website_id}",
                    "articles_found": 0,
                    "articles_stored": 0
                }
                
            # Create scraping job
            job = self.scraping_repo.create_job({
                "website_id": website_id,
                "status": "pending",
                "config": {
                    "max_articles": self.config.scraper.max_articles_per_run,
                    "max_concurrent": self.config.scraper.max_concurrent_requests
                }
            })
            
            # Start job
            self.scraping_repo.start_job(job.id)
            
            # Discover URLs
            logger.info(f"Discovering URLs from {website.base_url}")
            urls = await discover_urls(website.base_url)
            
            if not urls:
                logger.error(f"No URLs discovered from {website.base_url}")
                self.scraping_repo.fail_job(job.id, f"No URLs discovered from {website.base_url}")
                return {
                    "status": "error",
                    "message": f"No URLs discovered from {website.base_url}",
                    "articles_found": 0,
                    "articles_stored": 0,
                    "job_id": job.id
                }
                
            logger.info(f"Discovered {len(urls)} URLs from {website.base_url}")
            
            # Limit the number of URLs to process
            max_articles = self.config.scraper.max_articles_per_run
            if max_articles > 0 and len(urls) > max_articles:
                urls = urls[:max_articles]
                logger.info(f"Limited to {max_articles} URLs")
                
            # Extract and store articles concurrently
            max_concurrent = self.config.scraper.max_concurrent_requests
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def extract_with_semaphore(url):
                async with semaphore:
                    return await self.extract_and_store_article(url, website_id)
                    
            tasks = [extract_with_semaphore(url) for url in urls]
            results = await asyncio.gather(*tasks)
            
            # Count results
            articles_found = len(urls)
            articles_stored = sum(1 for result in results if result and result.get("status") == "new")
            articles_existing = sum(1 for result in results if result and result.get("status") == "existing")
            articles_failed = sum(1 for result in results if not result)
            
            # Complete job
            self.scraping_repo.complete_job(job.id, articles_found, articles_stored)
            
            logger.info(f"Completed scraping job for {website.base_url}: {articles_stored} new articles stored")
            
            return {
                "status": "success",
                "message": f"Completed scraping job for {website.base_url}",
                "articles_found": articles_found,
                "articles_stored": articles_stored,
                "articles_existing": articles_existing,
                "articles_failed": articles_failed,
                "job_id": job.id
            }
        except Exception as e:
            logger.error(f"Error discovering and storing articles for website {website_id}: {str(e)}")
            if 'job' in locals():
                self.scraping_repo.fail_job(job.id, str(e))
                
            return {
                "status": "error",
                "message": str(e),
                "articles_found": 0,
                "articles_stored": 0,
                "job_id": job.id if 'job' in locals() else None
            }

    async def extract_and_store_article_batch(self, urls: List[str], website_id: int) -> Dict[str, Any]:
        """
        Extract and store multiple articles in a batch.
        
        Args:
            urls (List[str]): List of article URLs
            website_id (int): Website ID
            
        Returns:
            Dict[str, Any]: Results of the batch extraction and storage process
        """
        try:
            # Get website
            website = self.website_repo.get_website_by_id(website_id)
            if not website:
                logger.error(f"Website not found: {website_id}")
                return {
                    "status": "error",
                    "message": f"Website not found: {website_id}",
                    "articles_found": 0,
                    "articles_stored": 0
                }
                
            # Create scraping job
            job = self.scraping_repo.create_job({
                "website_id": website_id,
                "status": "pending",
                "config": {
                    "max_articles": len(urls),
                    "max_concurrent": self.config.scraper.max_concurrent_requests
                }
            })
            
            # Start job
            self.scraping_repo.start_job(job.id)
            
            # Extract and store articles concurrently
            max_concurrent = self.config.scraper.max_concurrent_requests
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def extract_with_semaphore(url):
                async with semaphore:
                    return await self.extract_and_store_article(url, website_id)
                    
            tasks = [extract_with_semaphore(url) for url in urls]
            results = await asyncio.gather(*tasks)
            
            # Count results
            articles_found = len(urls)
            articles_stored = sum(1 for result in results if result and result.get("status") == "new")
            articles_existing = sum(1 for result in results if result and result.get("status") == "existing")
            articles_failed = sum(1 for result in results if not result)
            
            # Complete job
            self.scraping_repo.complete_job(job.id, articles_found, articles_stored)
            
            logger.info(f"Completed batch extraction for {website.base_url}: {articles_stored} new articles stored")
            
            return {
                "status": "success",
                "message": f"Completed batch extraction for {website.base_url}",
                "articles_found": articles_found,
                "articles_stored": articles_stored,
                "articles_existing": articles_existing,
                "articles_failed": articles_failed,
                "job_id": job.id
            }
        except Exception as e:
            logger.error(f"Error in batch extraction for website {website_id}: {str(e)}")
            if 'job' in locals():
                self.scraping_repo.fail_job(job.id, str(e))
                
            return {
                "status": "error",
                "message": str(e),
                "articles_found": 0,
                "articles_stored": 0,
                "job_id": job.id if 'job' in locals() else None
            }

    def get_article_stats(self, website_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get statistics for articles.
        
        Args:
            website_id (Optional[int], optional): Website ID. Defaults to None.
            
        Returns:
            Dict[str, Any]: Article statistics
        """
        total_articles = self.article_repo.get_articles_count(website_id)
        
        # Get website stats if website_id is provided
        website_stats = {}
        if website_id:
            website = self.website_repo.get_website_by_id(website_id)
            if website:
                latest_article_date = self.article_repo.get_latest_article_date(website_id)
                categories = self.website_repo.get_website_categories(website_id)
                
                website_stats = {
                    "name": website.name,
                    "base_url": website.base_url,
                    "latest_article_date": latest_article_date,
                    "categories_count": len(categories)
                }
                
        # Get job stats
        job_stats = self.scraping_repo.get_job_stats(website_id)
        
        return {
            "total_articles": total_articles,
            "website": website_stats,
            "jobs": job_stats
        }

    def get_recent_articles(self, website_id: Optional[int] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent articles.
        
        Args:
            website_id (Optional[int], optional): Website ID. Defaults to None.
            limit (int, optional): Maximum number of articles to return. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of recent articles
        """
        if website_id:
            articles = self.article_repo.get_articles_by_website(website_id, limit)
        else:
            # Get articles from all websites
            articles = self.db.query(self.article_repo.Article).order_by(
                self.article_repo.Article.published_at.desc()
            ).limit(limit).all()
            
        result = []
        for article in articles:
            # Get website name
            website = self.website_repo.get_website_by_id(article.website_id)
            website_name = website.name if website else "Unknown"
            
            # Get categories
            categories = self.article_repo.get_article_categories(article.id)
            category_names = [category.name for category in categories]
            
            article_dict = {
                "id": article.id,
                "title": article.title,
                "url": article.url,
                "author": article.author,
                "published_at": article.published_at,
                "website_id": article.website_id,
                "website_name": website_name,
                "categories": category_names,
                "image_url": article.image_url
            }
            result.append(article_dict)
            
        return result
