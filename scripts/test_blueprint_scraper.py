"""
Test script for scraping Blueprint.ng.

This script adds Blueprint.ng to the database and runs a test scrape.
"""

import asyncio
import logging
import sys
from datetime import datetime
from sqlalchemy.orm import Session

# Add the project root to the Python path
sys.path.append(".")

from src.database_management.connection import get_db, init_db
from src.database_management.repositories.website_repository import WebsiteRepository
from src.database_management.repositories.scraping_repository import ScrapingRepository
from src.service_layer.article_service import ArticleService
from config.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def test_blueprint_scraper():
    """Test scraping Blueprint.ng."""
    # Get database session
    db = next(get_db())
    
    # Create repositories
    website_repo = WebsiteRepository(db)
    scraping_repo = ScrapingRepository(db)
    
    # Check if Blueprint.ng already exists
    blueprint = website_repo.get_website_by_url("https://blueprint.ng")
    
    if not blueprint:
        logger.info("Adding Blueprint.ng to the database")
        
        # Add Blueprint.ng to the database
        blueprint = website_repo.create_website({
            "name": "Blueprint News",
            "base_url": "https://blueprint.ng",
            "description": "Blueprint gives you the latest Nigerian news in one place. Read the news behind the news on burning National issues in Nigeria and the world.",
            "logo_url": "https://blueprint.ng/wp-content/uploads/2025/01/blueprint.ng_logo.jpg",
            "sitemap_url": "https://blueprint.ng/sitemap.xml",
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        logger.info(f"Added Blueprint.ng to the database with ID {blueprint.id}")
        
        # Add categories
        categories = [
            {"name": "Top Stories", "url": "https://blueprint.ng/category/top-newspaper/"},
            {"name": "Breaking News", "url": "https://blueprint.ng/category/breaking-news/"},
            {"name": "Nigerian News", "url": "https://blueprint.ng/category/news/"},
            {"name": "Politics", "url": "https://blueprint.ng/category/news-politics/"},
            {"name": "Business", "url": "https://blueprint.ng/category/business-news/"},
            {"name": "Security & Crime", "url": "https://blueprint.ng/category/security/"},
            {"name": "Health", "url": "https://blueprint.ng/category/health-news/"},
            {"name": "Sports", "url": "https://blueprint.ng/category/sports-npfl-news/"},
            {"name": "Entertainment", "url": "https://blueprint.ng/category/entertainment/"},
            {"name": "Opinion", "url": "https://blueprint.ng/category/opinion/"}
        ]
        
        for category_data in categories:
            website_repo.create_category(blueprint.id, category_data)
            logger.info(f"Added category {category_data['name']} to Blueprint.ng")
    else:
        logger.info(f"Blueprint.ng already exists in the database with ID {blueprint.id}")
    
    # Create article service
    article_service = ArticleService(db)
    
    # Run test scrape
    logger.info(f"Starting test scrape for Blueprint.ng (ID: {blueprint.id})")
    result = await article_service.discover_and_store_articles(blueprint.id)
    
    # Log results
    logger.info(f"Scraping results: {result}")
    
    # Print summary
    print("\n=== Blueprint.ng Scraping Test Results ===")
    print(f"Status: {result.get('status', 'unknown')}")
    print(f"Articles found: {result.get('articles_found', 0)}")
    print(f"Articles stored: {result.get('articles_stored', 0)}")
    print(f"Articles existing: {result.get('articles_existing', 0)}")
    print(f"Articles failed: {result.get('articles_failed', 0)}")
    print(f"Message: {result.get('message', '')}")
    print("=========================================\n")
    
    # Get the latest articles
    articles = article_service.get_latest_articles(limit=5)
    
    # Print the latest articles
    print("\n=== Latest Articles ===")
    for article in articles:
        print(f"Title: {article.get('title')}")
        print(f"URL: {article.get('url')}")
        print(f"Author: {article.get('author')}")
        print(f"Published: {article.get('published_at')}")
        print(f"Website: {article.get('website_name')}")
        print(f"Categories: {', '.join(article.get('categories', []))}")
        print("------------------------")
    print("=======================\n")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_blueprint_scraper())
