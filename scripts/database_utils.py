#!/usr/bin/env python3
"""
Database Utility Script for Naija News Hub

This script provides utilities for:
1. Checking database tables and their contents
2. Fixing categories for articles that don't have them
3. Fixing article service code to properly handle categories

Usage:
    python scripts/database_utils.py check      # Check database tables and contents
    python scripts/database_utils.py fix-categories  # Fix categories for articles
    python scripts/database_utils.py fix-code    # Fix article service code
    python scripts/database_utils.py all         # Run all operations
"""

import sys
import logging
import re
import argparse
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

def check_database(verbose: bool = False):
    """
    Check the database tables and their contents.
    
    Args:
        verbose: Whether to show detailed information
    """
    logger.info("Checking database tables and contents...")
    
    # Get database session
    db = next(get_db())

    try:
        # Check websites table
        websites_count = db.query(Website).count()
        logger.info(f"Websites count: {websites_count}")
        
        if websites_count > 0:
            websites = db.query(Website).all()
            for website in websites:
                logger.info(f"Website: {website.id} - {website.name} - {website.base_url}")
        
        # Check articles table
        articles_count = db.query(Article).count()
        logger.info(f"Articles count: {articles_count}")
        
        if articles_count > 0:
            articles = db.query(Article).limit(5).all()
            for article in articles:
                logger.info(f"Article: {article.id} - {article.title} - {article.url}")
                
                if verbose:
                    logger.info(f"  Metadata: {article.article_metadata}")
                
                # Check if article has categories
                article_categories = db.query(ArticleCategory).filter(ArticleCategory.article_id == article.id).all()
                if article_categories:
                    logger.info(f"  Article {article.id} has {len(article_categories)} categories")
                    if verbose:
                        for ac in article_categories:
                            category = db.query(Category).filter(Category.id == ac.category_id).first()
                            if category:
                                logger.info(f"    Category: {category.id} - {category.name} - {category.url}")
                else:
                    logger.info(f"  Article {article.id} has no categories")
                    
                    # Check if article has categories in metadata
                    if article.article_metadata and 'categories' in article.article_metadata:
                        categories = article.article_metadata.get('categories', [])
                        logger.info(f"  Article {article.id} has {len(categories)} categories in metadata: {categories}")
        
        # Check categories table
        categories_count = db.query(Category).count()
        logger.info(f"Categories count: {categories_count}")
        
        if categories_count > 0 and verbose:
            categories = db.query(Category).all()
            for category in categories:
                logger.info(f"Category: {category.id} - {category.name} - {category.url}")
        
        # Check article_categories table
        article_categories_count = db.query(ArticleCategory).count()
        logger.info(f"Article-Categories count: {article_categories_count}")
        
        if article_categories_count > 0 and verbose:
            article_categories = db.query(ArticleCategory).all()
            for ac in article_categories:
                logger.info(f"Article-Category: {ac.article_id} - {ac.category_id}")
    
    finally:
        db.close()

def fix_categories(dry_run: bool = False):
    """
    Fix categories for articles.
    
    This function:
    1. Checks if articles have categories in their metadata
    2. Creates categories in the database if they don't exist
    3. Links articles to categories
    
    Args:
        dry_run: If True, don't make any changes to the database
    """
    logger.info("Fixing categories for articles...")
    
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
                if not dry_run:
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
                else:
                    logger.info(f"  [DRY RUN] Would update article metadata with categories")
            
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
                    
                    if not dry_run:
                        category = website_repo.create_category(article.website_id, {
                            "name": category_name,
                            "url": category_url
                        })
                        logger.info(f"  Created new category: {category_name} ({category_url})")
                    else:
                        logger.info(f"  [DRY RUN] Would create new category: {category_name} ({category_url})")
                        continue  # Skip adding category to article in dry run mode
                
                # Add category to article
                if not dry_run:
                    result = article_repo.add_article_category(article.id, category.id)
                    if result:
                        logger.info(f"  Added category {category_name} to article {article.id}")
                    else:
                        logger.warning(f"  Failed to add category {category_name} to article {article.id}")
                else:
                    logger.info(f"  [DRY RUN] Would add category {category_name} to article {article.id}")
    
    finally:
        db.close()

def fix_article_service():
    """
    Fix the article_service.py file to properly handle categories.
    
    This function:
    1. Updates the extract_and_store_article method to properly handle categories
    2. Ensures categories are extracted from article_metadata
    """
    logger.info("Fixing article_service.py to properly handle categories...")
    
    file_path = "src/service_layer/article_service.py"
    
    # Read the file
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"File {file_path} not found")
        return
    
    # Check if the file already has the fix
    if "categories = article_data.get(\"article_metadata\", {}).get(\"categories\", [])" in content:
        logger.info(f"File {file_path} already has the fix")
        return
    
    # Update the categories extraction
    old_pattern = r"# Add categories if available\s+categories = article_data\.get\(\"categories\", \[\]\)"
    new_pattern = """# Add categories if available
            categories = article_data.get("article_metadata", {}).get("categories", [])
            category_urls = article_data.get("article_metadata", {}).get("category_urls", [])
            
            # If no categories in article_metadata, check top-level (for backward compatibility)
            if not categories:
                categories = article_data.get("categories", [])
                category_urls = article_data.get("category_urls", [])"""
    
    content = re.sub(old_pattern, new_pattern, content)
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {file_path}")

def fix_article_extractor():
    """
    Fix the article_extractor.py file to properly handle categories.
    
    This function:
    1. Updates the article data creation to include website base URL
    2. Adds categorization for articles without categories
    """
    logger.info("Fixing article_extractor.py to properly handle categories...")
    
    file_path = "src/web_scraper/article_extractor.py"
    
    # Read the file
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"File {file_path} not found")
        return
    
    # Check if the file already has the fix
    if "# Categorize the article if no categories were extracted" in content:
        logger.info(f"File {file_path} already has the fix")
        return
    
    # Update the article data creation
    old_pattern = r"# Create article data\s+article_data = \{\s+\"title\": title,\s+\"url\": url,\s+\"content\": content_markdown,\s+\"content_markdown\": content_markdown,\s+\"content_html\": content_html,\s+\"author\": author,\s+\"published_at\": published_at,\s+\"image_url\": image_url,\s+\"website_id\": website_id,\s+\"article_metadata\": \{\s+\"word_count\": word_count,\s+\"reading_time\": reading_time,\s+\"categories\": categories,\s+\"tags\": tags,\s+\"schema\": \{\},\s+\"extraction_method\": \"strategy\" if extracted_data else \"fallback\"\s+\},\s+\"active\": True,\s+\}"
    new_pattern = """# Create article data
                article_data = {
                    "title": title,
                    "url": url,
                    "content": content_markdown,  # Use markdown for content
                    "content_markdown": content_markdown,
                    "content_html": content_html,
                    "author": author,
                    "published_at": published_at,
                    "image_url": image_url,
                    "website_id": website_id,
                    "article_metadata": {
                        "word_count": word_count,
                        "reading_time": reading_time,
                        "categories": categories,
                        "tags": tags,
                        "schema": {},
                        "extraction_method": "strategy" if extracted_data else "fallback"
                    },
                    "active": True,
                }
                
                # Get website base URL for category URL generation
                website_base_url = url
                # Extract domain from URL
                parsed_url = urlparse(url)
                website_base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                
                # Categorize the article if no categories were extracted
                if not categories:
                    article_data = categorize_article(article_data, website_base_url)"""
    
    content = re.sub(old_pattern, new_pattern, content)
    
    # Add import for categorize_article if not already present
    if "from src.web_scraper.category_extractor import categorize_article" not in content:
        import_pattern = r"from src\.web_scraper\.category_extractor import extract_categories_from_html, extract_tags_from_html"
        import_replacement = "from src.web_scraper.category_extractor import extract_categories_from_html, extract_tags_from_html, categorize_article"
        content = re.sub(import_pattern, import_replacement, content)
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {file_path}")

def main():
    """Main function to parse arguments and run the appropriate function."""
    parser = argparse.ArgumentParser(description="Database utility script for Naija News Hub")
    parser.add_argument("action", choices=["check", "fix-categories", "fix-code", "all"], 
                        help="Action to perform")
    parser.add_argument("--verbose", "-v", action="store_true", 
                        help="Show detailed information")
    parser.add_argument("--dry-run", "-d", action="store_true", 
                        help="Don't make any changes to the database")
    
    args = parser.parse_args()
    
    if args.action == "check" or args.action == "all":
        check_database(args.verbose)
    
    if args.action == "fix-categories" or args.action == "all":
        fix_categories(args.dry_run)
    
    if args.action == "fix-code" or args.action == "all":
        fix_article_service()
        fix_article_extractor()

if __name__ == "__main__":
    main()
