#!/usr/bin/env python3
"""
Script to check the database tables and their contents.
"""

import sys
import logging
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.append(".")

from src.database_management.connection import get_db
from src.database_management.models import Website, Article, Category, ArticleCategory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def check_database():
    """Check the database tables and their contents."""
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
                logger.info(f"  Metadata: {article.article_metadata}")

                # Check if article has categories
                article_categories = db.query(ArticleCategory).filter(ArticleCategory.article_id == article.id).all()
                if article_categories:
                    logger.info(f"  Article {article.id} has {len(article_categories)} categories")
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

        if categories_count > 0:
            categories = db.query(Category).all()
            for category in categories:
                logger.info(f"Category: {category.id} - {category.name} - {category.url}")

        # Check article_categories table
        article_categories_count = db.query(ArticleCategory).count()
        logger.info(f"Article-Categories count: {article_categories_count}")

        if article_categories_count > 0:
            article_categories = db.query(ArticleCategory).all()
            for ac in article_categories:
                logger.info(f"Article-Category: {ac.article_id} - {ac.category_id}")

    finally:
        db.close()

if __name__ == "__main__":
    check_database()
