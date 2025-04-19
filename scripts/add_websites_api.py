#!/usr/bin/env python3
"""
Add websites to the database using the API.

This script adds Blueprint.ng and Daily Trust to the database using the API.
"""

import sys
import logging
import requests
import json
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def add_website(website_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a website to the database using the API."""
    api_url = "http://localhost:8000/api/websites"
    
    try:
        response = requests.post(api_url, json=website_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error adding website: {str(e)}")
        return {"status": "error", "message": str(e)}

def main():
    """Main function."""
    # Define websites
    websites = [
        {
            "name": "Blueprint News",
            "base_url": "https://blueprint.ng",
            "description": "Blueprint gives you the latest Nigerian news in one place. Read the news behind the news on burning National issues in Nigeria and the world.",
            "logo_url": "https://blueprint.ng/wp-content/uploads/2025/01/blueprint.ng_logo.jpg",
            "sitemap_url": "https://blueprint.ng/sitemap.xml",
            "active": True
        },
        {
            "name": "Daily Trust",
            "base_url": "https://dailytrust.com",
            "description": "Daily Trust is a Nigerian daily newspaper published in Abuja. It is among the leading independent newspapers in Nigeria.",
            "logo_url": "https://dailytrust.com/wp-content/uploads/2023/06/Daily-Trust-Logo.png",
            "sitemap_url": "https://dailytrust.com/sitemap_index.xml",
            "active": True
        }
    ]
    
    # Add websites to database
    for website_data in websites:
        logger.info(f"Adding website: {website_data['name']} ({website_data['base_url']})")
        result = add_website(website_data)
        
        if "id" in result:
            logger.info(f"Successfully added website: {website_data['name']} ({website_data['base_url']}), ID: {result['id']}")
        else:
            logger.error(f"Failed to add website: {website_data['name']} ({website_data['base_url']}), Error: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    main()
