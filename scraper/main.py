"""
Command-line interface for the news scraper.
"""

import logging
import os
import sys
from typing import Optional

import click

from scraper.article_scraper import ArticleScraper
from scraper.utils.exporters import save_to_csv, save_to_json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--url', required=True, help='Base URL of the news website to scrape')
@click.option('--limit', default=10, help='Maximum number of articles to scrape')
@click.option('--output', default='./output', help='Directory to save scraped articles')
@click.option('--format', 'output_format', type=click.Choice(['json', 'csv', 'both']), default='json',
              help='Output format for scraped articles')
@click.option('--user-agent', help='Custom user agent string')
def main(url: str, limit: int, output: str, output_format: str, user_agent: Optional[str]) -> None:
    """
    Scrape news articles from a website.
    
    This tool automatically extracts news articles from a website when provided with a base URL.
    """
    try:
        logger.info(f"Starting scraper for {url}")
        
        # Initialize the scraper
        scraper = ArticleScraper(url, user_agent=user_agent)
        
        # Get article links
        article_links = scraper.get_article_links(limit=limit)
        
        if not article_links:
            logger.error("No article links found. Please check the URL and try again.")
            sys.exit(1)
        
        logger.info(f"Found {len(article_links)} article links. Scraping...")
        
        # Scrape articles
        articles = scraper.scrape_multiple_articles(article_links)
        
        if not articles:
            logger.error("Failed to scrape any articles. Please check the URL and try again.")
            sys.exit(1)
        
        logger.info(f"Successfully scraped {len(articles)} articles")
        
        # Save articles
        if output_format in ('json', 'both'):
            json_path = save_to_json(articles, output)
            logger.info(f"Saved articles to JSON: {json_path}")
        
        if output_format in ('csv', 'both'):
            csv_path = save_to_csv(articles, output)
            logger.info(f"Saved articles to CSV: {csv_path}")
        
        logger.info("Scraping completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
