#!/usr/bin/env python3
"""
Add websites to the database.

This script adds Blueprint.ng and Daily Trust to the database.
"""

import sys
import asyncio
import logging
from sqlalchemy.exc import IntegrityError

# Add the project root to the Python path
sys.path.append(".")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database_management.models import Website
from src.database_management.repositories import WebsiteRepository
from config.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def add_websites():
    """Add websites to the database."""
    # Get database configuration
    config = get_config()
    db_config = config.database

    # Create database engine
    connection_string = f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
    engine = create_engine(connection_string)

    # Create session
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        # Create repository
        website_repo = WebsiteRepository(db)

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
            try:
                # Check if website already exists
                existing_website = db.query(Website).filter(Website.base_url == website_data["base_url"]).first()

                if existing_website:
                    logger.info(f"Website already exists: {website_data['name']} ({website_data['base_url']})")

                    # Update website
                    for key, value in website_data.items():
                        setattr(existing_website, key, value)

                    db.commit()
                    logger.info(f"Updated website: {website_data['name']} ({website_data['base_url']})")
                else:
                    # Create website
                    website = Website(**website_data)
                    db.add(website)
                    db.commit()
                    logger.info(f"Added website: {website_data['name']} ({website_data['base_url']})")
            except IntegrityError:
                db.rollback()
                logger.error(f"Error adding website: {website_data['name']} ({website_data['base_url']})")
                continue

        # Get all websites
        websites = website_repo.get_all_websites()

        # Print websites
        logger.info(f"Total websites: {len(websites)}")
        for website in websites:
            logger.info(f"Website: {website.name} ({website.base_url}), ID: {website.id}")

        return websites
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(add_websites())
