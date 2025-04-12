"""
Repositories package for Naija News Hub.

This package provides repository classes for database operations.
"""

from src.database.repositories.article_repository import ArticleRepository
from src.database.repositories.website_repository import WebsiteRepository
from src.database.repositories.scraping_repository import ScrapingRepository

__all__ = [
    'ArticleRepository',
    'WebsiteRepository',
    'ScrapingRepository'
]
