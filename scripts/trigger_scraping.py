#!/usr/bin/env python3
"""
Trigger scraping for websites.

This script triggers scraping for Blueprint.ng and Daily Trust using the API.
"""

import sys
import asyncio
import logging
import requests
import json
from typing import Dict, Any, List, Optional

# Add the project root to the Python path
sys.path.append(".")

from config.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def get_websites() -> List[Dict[str, Any]]:
    """Get all websites from the API."""
    config = get_config()
    api_url = f"http://{config.api.host}:{config.api.port}/api/websites"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting websites: {str(e)}")
        return []

def trigger_scraping(website_id: int, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Trigger scraping for a website."""
    config = get_config()
    api_url = f"http://{config.api.host}:{config.api.port}/api/scraping/website/{website_id}"
    
    try:
        response = requests.post(api_url, json={"config": config or {}})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error triggering scraping for website {website_id}: {str(e)}")
        return {"status": "error", "message": str(e)}

def trigger_all_scraping(config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Trigger scraping for all websites."""
    config_obj = get_config()
    api_url = f"http://{config_obj.api.host}:{config_obj.api.port}/api/scraping/all"
    
    try:
        response = requests.post(api_url, json={"config": config or {}})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error triggering scraping for all websites: {str(e)}")
        return [{"status": "error", "message": str(e)}]

def main():
    """Main function."""
    # Get all websites
    websites = get_websites()
    
    if not websites:
        logger.error("No websites found")
        return
    
    # Print websites
    logger.info(f"Found {len(websites)} websites:")
    for website in websites:
        logger.info(f"Website: {website['name']} ({website['base_url']}), ID: {website['id']}")
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Scrape a specific website")
    print("2. Scrape all websites")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        # Ask which website to scrape
        website_id = input("Enter website ID to scrape: ")
        try:
            website_id = int(website_id)
        except ValueError:
            logger.error("Invalid website ID")
            return
        
        # Ask how many articles to scrape
        limit = input("Enter maximum number of articles to scrape (default: 10): ")
        try:
            limit = int(limit) if limit else 10
        except ValueError:
            logger.error("Invalid limit")
            return
        
        # Trigger scraping
        config = {
            "max_articles": limit,
            "max_concurrent": 5,
            "rate_limit": 2,
            "proxy_rotation": True
        }
        
        result = trigger_scraping(website_id, config)
        logger.info(f"Scraping triggered for website {website_id}: {result}")
    
    elif choice == "2":
        # Ask how many articles to scrape
        limit = input("Enter maximum number of articles to scrape per website (default: 10): ")
        try:
            limit = int(limit) if limit else 10
        except ValueError:
            logger.error("Invalid limit")
            return
        
        # Trigger scraping
        config = {
            "max_articles": limit,
            "max_concurrent": 5,
            "rate_limit": 2,
            "proxy_rotation": True
        }
        
        results = trigger_all_scraping(config)
        logger.info(f"Scraping triggered for all websites: {results}")
    
    elif choice == "3":
        logger.info("Exiting")
        return
    
    else:
        logger.error("Invalid choice")
        return

if __name__ == "__main__":
    main()
