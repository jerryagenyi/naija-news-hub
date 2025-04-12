"""
Article repository module for Naija News Hub.

This module provides functions to interact with the articles table in the database.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_, func

from src.database_management.models import Article, Website, Category, ArticleCategory


class ArticleRepository:
    """Repository for article operations."""

    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.

        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db

    def create_article(self, article_data: Dict[str, Any]) -> Article:
        """
        Create a new article in the database.

        Args:
            article_data (Dict[str, Any]): Article data

        Returns:
            Article: Created article

        Raises:
            IntegrityError: If the article already exists
        """
        article = Article(**article_data)
        self.db.add(article)
        try:
            self.db.commit()
            self.db.refresh(article)
            return article
        except IntegrityError:
            self.db.rollback()
            raise

    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        """
        Get an article by ID.

        Args:
            article_id (int): Article ID

        Returns:
            Optional[Article]: Article if found, None otherwise
        """
        return self.db.query(Article).filter(Article.id == article_id).first()

    def get_article_by_url(self, url: str) -> Optional[Article]:
        """
        Get an article by URL.

        Args:
            url (str): Article URL

        Returns:
            Optional[Article]: Article if found, None otherwise
        """
        return self.db.query(Article).filter(Article.url == url).first()

    def get_articles_by_website(self, website_id: int, limit: int = 100, offset: int = 0) -> List[Article]:
        """
        Get articles by website ID.

        Args:
            website_id (int): Website ID
            limit (int, optional): Maximum number of articles to return. Defaults to 100.
            offset (int, optional): Offset for pagination. Defaults to 0.

        Returns:
            List[Article]: List of articles
        """
        return self.db.query(Article).filter(
            Article.website_id == website_id
        ).order_by(
            Article.published_at.desc()
        ).limit(limit).offset(offset).all()

    def get_articles_by_category(self, category_id: int, limit: int = 100, offset: int = 0) -> List[Article]:
        """
        Get articles by category ID.

        Args:
            category_id (int): Category ID
            limit (int, optional): Maximum number of articles to return. Defaults to 100.
            offset (int, optional): Offset for pagination. Defaults to 0.

        Returns:
            List[Article]: List of articles
        """
        return self.db.query(Article).join(
            ArticleCategory, Article.id == ArticleCategory.article_id
        ).filter(
            ArticleCategory.category_id == category_id
        ).order_by(
            Article.published_at.desc()
        ).limit(limit).offset(offset).all()

    def update_article(self, article_id: int, article_data: Dict[str, Any]) -> Optional[Article]:
        """
        Update an article.

        Args:
            article_id (int): Article ID
            article_data (Dict[str, Any]): Article data to update

        Returns:
            Optional[Article]: Updated article if found, None otherwise
        """
        article = self.get_article_by_id(article_id)
        if not article:
            return None

        for key, value in article_data.items():
            setattr(article, key, value)

        article.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(article)
        return article

    def delete_article(self, article_id: int) -> bool:
        """
        Delete an article.

        Args:
            article_id (int): Article ID

        Returns:
            bool: True if deleted, False if not found
        """
        article = self.get_article_by_id(article_id)
        if not article:
            return False

        self.db.delete(article)
        self.db.commit()
        return True

    def add_article_category(self, article_id: int, category_id: int) -> bool:
        """
        Add a category to an article.

        Args:
            article_id (int): Article ID
            category_id (int): Category ID

        Returns:
            bool: True if added, False if already exists or not found
        """
        # Check if article and category exist
        article = self.get_article_by_id(article_id)
        category = self.db.query(Category).filter(Category.id == category_id).first()

        if not article or not category:
            return False

        # Check if relationship already exists
        existing = self.db.query(ArticleCategory).filter(
            ArticleCategory.article_id == article_id,
            ArticleCategory.category_id == category_id
        ).first()

        if existing:
            return False

        # Create relationship
        article_category = ArticleCategory(article_id=article_id, category_id=category_id)
        self.db.add(article_category)
        self.db.commit()
        return True

    def remove_article_category(self, article_id: int, category_id: int) -> bool:
        """
        Remove a category from an article.

        Args:
            article_id (int): Article ID
            category_id (int): Category ID

        Returns:
            bool: True if removed, False if not found
        """
        article_category = self.db.query(ArticleCategory).filter(
            ArticleCategory.article_id == article_id,
            ArticleCategory.category_id == category_id
        ).first()

        if not article_category:
            return False

        self.db.delete(article_category)
        self.db.commit()
        return True

    def get_article_categories(self, article_id: int) -> List[Category]:
        """
        Get categories for an article.

        Args:
            article_id (int): Article ID

        Returns:
            List[Category]: List of categories
        """
        return self.db.query(Category).join(
            ArticleCategory, Category.id == ArticleCategory.category_id
        ).filter(
            ArticleCategory.article_id == article_id
        ).all()

    def get_articles_by_category(self, category_id: int, limit: int = 10, offset: int = 0) -> List[Article]:
        """
        Get articles for a category.

        Args:
            category_id (int): Category ID
            limit (int, optional): Maximum number of articles to return. Defaults to 10.
            offset (int, optional): Offset for pagination. Defaults to 0.

        Returns:
            List[Article]: List of articles
        """
        return self.db.query(Article).join(
            ArticleCategory, Article.id == ArticleCategory.article_id
        ).filter(
            ArticleCategory.category_id == category_id,
            Article.active == True
        ).order_by(
            Article.published_at.desc()
        ).limit(limit).offset(offset).all() if limit > 0 else self.db.query(Article).join(
            ArticleCategory, Article.id == ArticleCategory.article_id
        ).filter(
            ArticleCategory.category_id == category_id,
            Article.active == True
        ).order_by(
            Article.published_at.desc()
        ).all()

    def search_articles(self, query: str, limit: int = 100, offset: int = 0) -> List[Article]:
        """
        Search articles by title or content.

        Args:
            query (str): Search query
            limit (int, optional): Maximum number of articles to return. Defaults to 100.
            offset (int, optional): Offset for pagination. Defaults to 0.

        Returns:
            List[Article]: List of articles matching the query
        """
        search_term = f"%{query}%"
        return self.db.query(Article).filter(
            or_(
                Article.title.ilike(search_term),
                Article.content.ilike(search_term)
            )
        ).order_by(
            Article.published_at.desc()
        ).limit(limit).offset(offset).all()

    def get_articles_count(self, website_id: Optional[int] = None) -> int:
        """
        Get the count of articles, optionally filtered by website ID.

        Args:
            website_id (Optional[int], optional): Website ID. Defaults to None.

        Returns:
            int: Count of articles
        """
        query = self.db.query(func.count(Article.id))
        if website_id:
            query = query.filter(Article.website_id == website_id)
        return query.scalar() or 0

    def get_latest_article_date(self, website_id: int) -> Optional[datetime]:
        """
        Get the date of the latest article for a website.

        Args:
            website_id (int): Website ID

        Returns:
            Optional[datetime]: Date of the latest article, or None if no articles
        """
        latest_article = self.db.query(Article).filter(
            Article.website_id == website_id
        ).order_by(
            Article.published_at.desc()
        ).first()

        return latest_article.published_at if latest_article else None

    def create_or_update_article(self, article_data: Dict[str, Any]) -> Article:
        """
        Create a new article or update an existing one.

        Args:
            article_data (Dict[str, Any]): Article data

        Returns:
            Article: Created or updated article
        """
        url = article_data.get('url')
        if not url:
            raise ValueError("Article URL is required")

        existing_article = self.get_article_by_url(url)

        if existing_article:
            # Update existing article
            for key, value in article_data.items():
                setattr(existing_article, key, value)

            existing_article.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing_article)
            return existing_article
        else:
            # Create new article
            return self.create_article(article_data)

    def batch_create_articles(self, articles_data: List[Dict[str, Any]]) -> List[Article]:
        """
        Create multiple articles in a batch.

        Args:
            articles_data (List[Dict[str, Any]]): List of article data

        Returns:
            List[Article]: List of created articles
        """
        articles = []
        for article_data in articles_data:
            try:
                article = Article(**article_data)
                self.db.add(article)
                articles.append(article)
            except Exception as e:
                # Log the error but continue with other articles
                print(f"Error creating article: {e}")

        self.db.commit()

        # Refresh all articles to get their IDs
        for article in articles:
            self.db.refresh(article)

        return articles
