#!/usr/bin/env python3
"""
Script to list articles in the database.
"""

import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.append(".")

from src.database_management.connection import get_db
from src.database_management.repositories import ArticleRepository, WebsiteRepository
from src.database_management.models import Article

def list_articles():
    """List articles in the database."""
    # Get database session
    db = next(get_db())

    # Create repositories
    article_repo = ArticleRepository(db)
    website_repo = WebsiteRepository(db)

    # Get all articles
    articles = db.query(Article).all()

    print(f"Found {len(articles)} articles in the database:")
    print("-" * 80)

    for article in articles:
        # Get website name
        website = website_repo.get_website_by_id(article.website_id)
        website_name = website.name if website else "Unknown"

        # Format published_at date
        published_at = article.published_at.strftime("%Y-%m-%d %H:%M:%S") if article.published_at else "Unknown"

        # Print article details
        print(f"ID: {article.id}")
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Author: {article.author}")
        print(f"Published: {published_at}")
        print(f"Website: {website_name} (ID: {article.website_id})")
        print(f"Created: {article.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)

if __name__ == "__main__":
    list_articles()
