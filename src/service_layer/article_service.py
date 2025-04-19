"""
Article service module for Naija News Hub.

This module provides services to extract and store articles.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from src.utility_modules.datetime_utils import convert_to_db_datetime

from src.database_management.models import Article
from src.database_management.connection import get_db
from src.database_management.repositories import ArticleRepository, WebsiteRepository, ScrapingRepository
from src.web_scraper.article_extractor import extract_article
from src.web_scraper.url_discovery import discover_urls
from src.utility_modules.content_validation import validate_article_content
from src.utility_modules.article_comparison import should_update_article, merge_article_data, get_article_changes_summary
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

    async def extract_and_store_article(self, url: str, website_id: int, force_update: bool = False) -> Optional[Dict[str, Any]]:
        """
        Extract an article from a URL and store it in the database.
        If the article already exists, check if it needs to be updated.

        Args:
            url (str): Article URL
            website_id (int): Website ID
            force_update (bool, optional): Force update even if article exists. Defaults to False.

        Returns:
            Optional[Dict[str, Any]]: Extracted article data if successful, None otherwise
        """
        try:
            # Check if article already exists
            existing_article = self.article_repo.get_article_by_url(url)
            if existing_article and not force_update:
                # Update the last_checked_at timestamp
                self.article_repo.update_article(existing_article.id, {
                    "last_checked_at": convert_to_db_datetime(None)
                })

                logger.info(f"Article already exists: {url}")
                return {
                    "id": existing_article.id,
                    "title": existing_article.title,
                    "url": existing_article.url,
                    "status": "existing",
                    "last_checked_at": convert_to_db_datetime(None)
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
                "published_at": convert_to_db_datetime(article_data.get("published_at")),
                "image_url": article_data.get("image_url", ""),
                "website_id": website_id,
                "article_metadata": article_data.get("article_metadata", {}),
                "last_checked_at": convert_to_db_datetime(None)
            }

            # Check if article metadata contains validation results
            validation_data = article_data.get("article_metadata", {}).get("validation", {})

            # If validation data is not present, validate the article
            if not validation_data:
                validation_result = validate_article_content(db_article_data)
                if not db_article_data["article_metadata"]:
                    db_article_data["article_metadata"] = {}
                db_article_data["article_metadata"]["validation"] = validation_result.to_dict()

                # Log validation results
                logger.info(f"Content validation result for {url}: {validation_result}")

                # If content is not valid, log warning
                if not validation_result.is_valid:
                    logger.warning(f"Article content validation failed for {url}: {validation_result.issues}")

                    # If validation score is too low, return None
                    if validation_result.score < 30:  # Very low quality content
                        logger.error(f"Article content quality too low for {url}: score={validation_result.score}")
                        return None

            # If article exists, check if it needs to be updated
            if existing_article and force_update:
                # Force update the article
                logger.info(f"Force updating article: {url}")

                # Merge existing data with new data
                merged_data = merge_article_data(existing_article, db_article_data)

                # Update the article
                article = self.article_repo.update_article(existing_article.id, merged_data)

                # Get a summary of changes
                changes_summary = get_article_changes_summary(existing_article, db_article_data)
                logger.info(f"Article update summary for {url}:\n{changes_summary}")

                status = "updated"
            elif existing_article:
                # Check if article needs to be updated
                should_update, reasons = should_update_article(existing_article, db_article_data)

                if should_update:
                    logger.info(f"Updating article: {url}, reasons: {reasons}")

                    # Merge existing data with new data
                    merged_data = merge_article_data(existing_article, db_article_data)

                    # Update the article
                    article = self.article_repo.update_article(existing_article.id, merged_data)

                    # Get a summary of changes
                    changes_summary = get_article_changes_summary(existing_article, db_article_data)
                    logger.info(f"Article update summary for {url}:\n{changes_summary}")

                    status = "updated"
                else:
                    logger.info(f"No update needed for article: {url}, reasons: {reasons}")
                    article = existing_article
                    status = "unchanged"
            else:
                # Store new article in database
                article = self.article_repo.create_article(db_article_data)
                status = "new"

            # Add categories if available
            categories = article_data.get("categories", [])
            category_urls = article_data.get("category_urls", [])

            # Ensure we have the same number of category URLs as categories
            if len(category_urls) < len(categories):
                # Get website base URL
                website = self.website_repo.get_website_by_id(website_id)
                base_url = website.base_url

                # Generate missing category URLs
                for i in range(len(category_urls), len(categories)):
                    category_name = categories[i]
                    category_urls.append(f"{base_url}/category/{category_name.lower().replace(' ', '-')}")

            # Process each category
            for i, category_name in enumerate(categories):
                category_url = category_urls[i] if i < len(category_urls) else None

                # Try to find existing category by name
                category = self.website_repo.get_category_by_name(website_id, category_name)

                if not category and category_url:
                    # Try to find by URL
                    category = self.website_repo.get_category_by_url(website_id, category_url)

                if not category:
                    # Create new category
                    if not category_url:
                        # Generate URL if not provided
                        website = self.website_repo.get_website_by_id(website_id)
                        category_url = f"{website.base_url}/category/{category_name.lower().replace(' ', '-')}"

                    category = self.website_repo.create_category(website_id, {
                        "name": category_name,
                        "url": category_url
                    })
                    logger.info(f"Created new category: {category_name} ({category_url})")

                # Add category to article
                self.article_repo.add_article_category(article.id, category.id)

            logger.info(f"Successfully processed article: {url} (status: {status})")
            return {
                "id": article.id,
                "title": article.title,
                "url": article.url,
                "status": status,
                "last_checked_at": article.last_checked_at
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
                },
                "articles_found": 0,
                "articles_scraped": 0
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
            from src.database_management.models import Article
            articles = self.db.query(Article).order_by(
                Article.published_at.desc()
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
