#!/usr/bin/env python3
"""
Script to fix categories for articles.

This script:
1. Checks if articles have categories in their metadata
2. Creates categories in the database if they don't exist
3. Links articles to categories
"""

import sys
import logging
from typing import Dict, Any, List, Optional
import json

# Add the project root to the Python path
sys.path.append(".")

from src.database_management.connection import get_db
from src.database_management.models import Website, Article, Category, ArticleCategory
from src.database_management.repositories.website_repository import WebsiteRepository
from src.database_management.repositories.article_repository import ArticleRepository
from src.web_scraper.category_extractor import categorize_article, extract_categories_from_html

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def fix_categories():
    """Fix categories for articles."""
    # Get database session
    db = next(get_db())

    try:
        # Create repositories
        website_repo = WebsiteRepository(db)
        article_repo = ArticleRepository(db)
        
        # Get all articles
        articles = db.query(Article).all()
        logger.info(f"Found {len(articles)} articles")
        
        # Process each article
        for article in articles:
            logger.info(f"Processing article {article.id}: {article.title}")
            
            # Check if article already has categories
            article_categories = db.query(ArticleCategory).filter(ArticleCategory.article_id == article.id).all()
            if article_categories:
                logger.info(f"  Article {article.id} already has {len(article_categories)} categories")
                continue
            
            # Get website
            website = website_repo.get_website_by_id(article.website_id)
            if not website:
                logger.warning(f"  Website {article.website_id} not found for article {article.id}")
                continue
            
            # Get base URL
            base_url = website.base_url
            
            # Check if article has categories in metadata
            categories = []
            category_urls = []
            
            if article.article_metadata and 'categories' in article.article_metadata:
                categories = article.article_metadata.get('categories', [])
                category_urls = article.article_metadata.get('category_urls', [])
                logger.info(f"  Found {len(categories)} categories in metadata: {categories}")
            
            # If no categories in metadata, try to extract from content
            if not categories and article.content_html:
                logger.info(f"  No categories in metadata, trying to extract from content")
                
                # Create article data for categorization
                article_data = {
                    "title": article.title,
                    "url": article.url,
                    "content": article.content,
                    "content_markdown": article.content_markdown,
                    "content_html": article.content_html,
                    "author": article.author,
                    "published_at": article.published_at,
                    "image_url": article.image_url,
                    "website_id": article.website_id,
                    "article_metadata": article.article_metadata or {},
                }
                
                # Categorize the article
                article_data = categorize_article(article_data, base_url)
                
                # Get categories and category URLs
                categories = article_data.get("categories", [])
                category_urls = article_data.get("category_urls", [])
                
                logger.info(f"  Extracted {len(categories)} categories: {categories}")
                
                # Update article metadata
                if article.article_metadata:
                    metadata = article.article_metadata
                    metadata["categories"] = categories
                    metadata["category_urls"] = category_urls
                else:
                    metadata = {
                        "categories": categories,
                        "category_urls": category_urls
                    }
                
                article.article_metadata = metadata
                db.commit()
                logger.info(f"  Updated article metadata with categories")
            
            # Ensure we have the same number of category URLs as categories
            if len(category_urls) < len(categories):
                # Generate missing category URLs
                for i in range(len(category_urls), len(categories)):
                    category_name = categories[i]
                    category_urls.append(f"{base_url}/category/{category_name.lower().replace(' ', '-')}")
            
            # Process each category
            for i, category_name in enumerate(categories):
                category_url = category_urls[i] if i < len(category_urls) else None
                
                # Try to find existing category by name
                category = website_repo.get_category_by_name(article.website_id, category_name)
                
                if not category and category_url:
                    # Try to find by URL
                    category = website_repo.get_category_by_url(article.website_id, category_url)
                
                if not category:
                    # Create new category
                    if not category_url:
                        # Generate URL if not provided
                        category_url = f"{base_url}/category/{category_name.lower().replace(' ', '-')}"
                    
                    category = website_repo.create_category(article.website_id, {
                        "name": category_name,
                        "url": category_url
                    })
                    logger.info(f"  Created new category: {category_name} ({category_url})")
                
                # Add category to article
                result = article_repo.add_article_category(article.id, category.id)
                if result:
                    logger.info(f"  Added category {category_name} to article {article.id}")
                else:
                    logger.warning(f"  Failed to add category {category_name} to article {article.id}")
    
    finally:
        db.close()

if __name__ == "__main__":
    fix_categories()
