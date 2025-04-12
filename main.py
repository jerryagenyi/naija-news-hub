#!/usr/bin/env python3
"""
Main entry point for Naija News Hub.

This module provides the main entry point for the application.
"""

import argparse
import asyncio
import logging
import uvicorn
from typing import Optional, Dict, Any, List

from src.api_endpoints.main import app
from src.web_scraper.main import scrape_website, scrape_all_websites
from src.database_management.connection import init_db, get_db, SessionLocal
from src.web_scraper.url_discovery import discover_urls
from src.web_scraper.article_extractor import extract_article
from src.service_layer import ArticleService
from src.database_management.repositories import WebsiteRepository, ArticleRepository, ScrapingRepository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Naija News Hub")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # API command
    api_parser = subparsers.add_parser("api", help="Run the API server")
    api_parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    api_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    api_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Run the scraper")
    scrape_parser.add_argument("--website-id", type=int, help="ID of the website to scrape")
    scrape_parser.add_argument("--all", action="store_true", help="Scrape all active websites")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize the database")

    # DB command
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_subparsers = db_parser.add_subparsers(dest="db_command", help="Database command to run")

    # Add website command
    add_website_parser = db_subparsers.add_parser("add-website", help="Add a website to the database")
    add_website_parser.add_argument("--name", type=str, required=True, help="Website name")
    add_website_parser.add_argument("--url", type=str, required=True, help="Website base URL")
    add_website_parser.add_argument("--description", type=str, help="Website description")
    add_website_parser.add_argument("--logo-url", type=str, help="Website logo URL")
    add_website_parser.add_argument("--sitemap-url", type=str, help="Website sitemap URL")

    # List websites command
    list_websites_parser = db_subparsers.add_parser("list-websites", help="List websites in the database")

    # Extract and store command
    extract_store_parser = db_subparsers.add_parser("extract-store", help="Extract and store an article")
    extract_store_parser.add_argument("--url", type=str, required=True, help="Article URL")
    extract_store_parser.add_argument("--website-id", type=int, required=True, help="Website ID")

    # Discover and store command
    discover_store_parser = db_subparsers.add_parser("discover-store", help="Discover and store articles")
    discover_store_parser.add_argument("--website-id", type=int, required=True, help="Website ID")

    # Get article stats command
    article_stats_parser = db_subparsers.add_parser("article-stats", help="Get article statistics")
    article_stats_parser.add_argument("--website-id", type=int, help="Website ID")

    # Get recent articles command
    recent_articles_parser = db_subparsers.add_parser("recent-articles", help="Get recent articles")
    recent_articles_parser.add_argument("--website-id", type=int, help="Website ID")
    recent_articles_parser.add_argument("--limit", type=int, default=10, help="Maximum number of articles to return")

    # Test command
    test_parser = subparsers.add_parser("test", help="Test the scraper")
    test_parser.add_argument("--url", type=str, required=True, help="URL to test")
    test_parser.add_argument("--discover", action="store_true", help="Test URL discovery")
    test_parser.add_argument("--extract", action="store_true", help="Test article extraction")

    return parser.parse_args()

async def run_scraper(website_id: Optional[int] = None):
    """Run the scraper."""
    if website_id:
        logger.info(f"Scraping website with ID {website_id}")
        result = await scrape_website(website_id)
        logger.info(f"Scraping result: {result}")
    else:
        logger.info("Scraping all active websites")
        results = await scrape_all_websites()
        logger.info(f"Scraping results: {results}")

async def test_scraper(url: str, discover: bool = False, extract: bool = False):
    """Test the scraper."""
    if not discover and not extract:
        # If no specific test is specified, run both
        discover = True
        extract = True

    if discover:
        logger.info(f"Testing URL discovery for {url}")
        try:
            urls = await discover_urls(url)
            logger.info(f"Discovered {len(urls)} URLs:")
            for i, discovered_url in enumerate(urls[:10], 1):
                logger.info(f"{i}. {discovered_url}")
            if len(urls) > 10:
                logger.info(f"... and {len(urls) - 10} more")
        except Exception as e:
            logger.error(f"Error discovering URLs: {str(e)}")

    if extract:
        logger.info(f"Testing article extraction for {url}")
        try:
            # Use a dummy website_id for testing
            article_data = await extract_article(url, website_id=1)
            logger.info(f"Extracted article: {article_data['title']}")
            logger.info(f"Author: {article_data['author']}")
            logger.info(f"Published: {article_data['published_at']}")
            logger.info(f"Content length: {len(article_data['content'])} characters")
            logger.info(f"Word count: {article_data['article_metadata']['word_count']} words")
            logger.info(f"Reading time: {article_data['article_metadata']['reading_time']} minutes")
        except Exception as e:
            logger.error(f"Error extracting article: {str(e)}")

def handle_db_command(args):
    """Handle database commands."""
    if not args.db_command:
        logger.error("No database command specified")
        return

    # Create a database session
    db = SessionLocal()
    try:
        if args.db_command == "add-website":
            # Add a website to the database
            website_repo = WebsiteRepository(db)
            website_data = {
                "name": args.name,
                "base_url": args.url,
                "description": args.description,
                "logo_url": args.logo_url,
                "sitemap_url": args.sitemap_url,
                "active": True
            }
            website = website_repo.create_website(website_data)
            logger.info(f"Added website: {website.name} (ID: {website.id})")

        elif args.db_command == "list-websites":
            # List websites in the database
            website_repo = WebsiteRepository(db)
            websites = website_repo.get_all_websites(active_only=False)
            logger.info(f"Found {len(websites)} websites:")
            for website in websites:
                logger.info(f"ID: {website.id}, Name: {website.name}, URL: {website.base_url}, Active: {website.active}")

        elif args.db_command == "extract-store":
            # Extract and store an article
            article_service = ArticleService(db)
            result = asyncio.run(article_service.extract_and_store_article(args.url, args.website_id))
            if result:
                logger.info(f"Article extracted and stored: {result['title']} (ID: {result['id']})")
                logger.info(f"Status: {result['status']}")
            else:
                logger.error(f"Failed to extract and store article: {args.url}")

        elif args.db_command == "discover-store":
            # Discover and store articles
            article_service = ArticleService(db)
            result = asyncio.run(article_service.discover_and_store_articles(args.website_id))
            logger.info(f"Discovery and storage result: {result}")

        elif args.db_command == "article-stats":
            # Get article statistics
            article_service = ArticleService(db)
            stats = article_service.get_article_stats(args.website_id)
            logger.info(f"Article statistics: {stats}")

        elif args.db_command == "recent-articles":
            # Get recent articles
            article_service = ArticleService(db)
            articles = article_service.get_recent_articles(args.website_id, args.limit)
            logger.info(f"Found {len(articles)} recent articles:")
            for article in articles:
                logger.info(f"ID: {article['id']}, Title: {article['title']}, URL: {article['url']}")
                logger.info(f"  Author: {article['author']}, Published: {article['published_at']}")
                logger.info(f"  Website: {article['website_name']} (ID: {article['website_id']})")
                logger.info(f"  Categories: {', '.join(article['categories'])}")
                logger.info("---")
        else:
            logger.error(f"Unknown database command: {args.db_command}")
    finally:
        db.close()

def main():
    """Main entry point."""
    args = parse_args()

    if args.command == "api":
        logger.info(f"Starting API server on {args.host}:{args.port}")
        uvicorn.run(
            "src.api-endpoints.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
        )
    elif args.command == "scrape":
        if args.all:
            asyncio.run(run_scraper())
        elif args.website_id:
            asyncio.run(run_scraper(args.website_id))
        else:
            logger.error("Either --website-id or --all must be specified")
    elif args.command == "init":
        logger.info("Initializing database")
        init_db()
        logger.info("Database initialized")
    elif args.command == "db":
        handle_db_command(args)
    elif args.command == "test":
        logger.info(f"Testing scraper with URL: {args.url}")
        asyncio.run(test_scraper(args.url, args.discover, args.extract))
    else:
        logger.error("No command specified")

if __name__ == "__main__":
    main()
