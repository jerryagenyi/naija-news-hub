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

from src.api.main import app
from src.scraper.main import scrape_website, scrape_all_websites
from src.database.connection import init_db
from src.scraper.url_discovery import discover_urls
from src.scraper.article_extractor import extract_article

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

def main():
    """Main entry point."""
    args = parse_args()

    if args.command == "api":
        logger.info(f"Starting API server on {args.host}:{args.port}")
        uvicorn.run(
            "src.api.main:app",
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
    elif args.command == "test":
        logger.info(f"Testing scraper with URL: {args.url}")
        asyncio.run(test_scraper(args.url, args.discover, args.extract))
    else:
        logger.error("No command specified")

if __name__ == "__main__":
    main()
