#!/usr/bin/env python3
"""
Clean dummy data from the database.

This script removes all articles with dummy/placeholder content from the database.
"""

import sys
import logging
from sqlalchemy import text

# Add the project root to the Python path
sys.path.append(".")

from src.database_management.connection import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def clean_dummy_data():
    """Clean dummy data from the database."""
    db = next(get_db())
    
    try:
        # Find dummy articles
        dummy_query = text("""
            SELECT id, title, url 
            FROM articles 
            WHERE title LIKE 'Sample Article from%' 
            OR content = 'This is a sample article content.'
            OR url LIKE '%/article/%'
        """)
        
        result = db.execute(dummy_query)
        dummy_articles = result.fetchall()
        
        if not dummy_articles:
            logger.info("No dummy articles found")
            return
        
        logger.info(f"Found {len(dummy_articles)} dummy articles")
        
        # Print the first 10 dummy articles
        for i, article in enumerate(dummy_articles[:10]):
            logger.info(f"Dummy article {i+1}: {article.title} ({article.url})")
        
        # Ask for confirmation
        confirm = input(f"Are you sure you want to delete {len(dummy_articles)} dummy articles? (y/n): ")
        
        if confirm.lower() != 'y':
            logger.info("Operation cancelled")
            return
        
        # Delete article categories
        for article in dummy_articles:
            # Delete from article_categories
            db.execute(text(f"DELETE FROM article_categories WHERE article_id = {article.id}"))
        
        # Delete dummy articles
        article_ids = [article.id for article in dummy_articles]
        chunks = [article_ids[i:i + 100] for i in range(0, len(article_ids), 100)]
        
        for chunk in chunks:
            ids_str = ','.join(str(id) for id in chunk)
            db.execute(text(f"DELETE FROM articles WHERE id IN ({ids_str})"))
        
        db.commit()
        
        logger.info(f"Successfully deleted {len(dummy_articles)} dummy articles")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error cleaning dummy data: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    clean_dummy_data()
