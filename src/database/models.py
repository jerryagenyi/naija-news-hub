"""
Database models for Naija News Hub.

This module defines the SQLAlchemy ORM models for the database.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Website(Base):
    """Model for news websites."""
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    base_url = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String(255), nullable=True)
    sitemap_url = Column(String(255), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    articles = relationship("Article", back_populates="website")
    categories = relationship("Category", back_populates="website")

    def __repr__(self):
        return f"<Website(name='{self.name}', base_url='{self.base_url}')>"

class Category(Base):
    """Model for news categories."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    website = relationship("Website", back_populates="categories")
    articles = relationship("ArticleCategory", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}', url='{self.url}')>"

class Article(Base):
    """Model for news articles."""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    url = Column(String(512), nullable=False, unique=True)
    content = Column(Text, nullable=True)
    content_markdown = Column(Text, nullable=True)
    content_html = Column(Text, nullable=True)
    author = Column(String(255), nullable=True)
    published_at = Column(DateTime, nullable=True)
    image_url = Column(String(512), nullable=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    article_metadata = Column(JSON, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    website = relationship("Website", back_populates="articles")
    categories = relationship("ArticleCategory", back_populates="article")

    def __repr__(self):
        return f"<Article(title='{self.title}', url='{self.url}')>"

class ArticleCategory(Base):
    """Model for article-category relationships."""
    __tablename__ = "article_categories"

    article_id = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)

    # Relationships
    article = relationship("Article", back_populates="categories")
    category = relationship("Category", back_populates="articles")

    def __repr__(self):
        return f"<ArticleCategory(article_id={self.article_id}, category_id={self.category_id})>"

class ScrapingJob(Base):
    """Model for scraping jobs."""
    __tablename__ = "scraping_jobs"

    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    status = Column(String(50), nullable=False, default="pending")  # pending, running, completed, failed
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    articles_found = Column(Integer, default=0)
    articles_scraped = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    config = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ScrapingJob(id={self.id}, website_id={self.website_id}, status='{self.status}')>"

class ScrapingError(Base):
    """Model for scraping errors."""
    __tablename__ = "scraping_errors"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("scraping_jobs.id"), nullable=False)
    url = Column(String(512), nullable=True)
    error_type = Column(String(255), nullable=False)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ScrapingError(id={self.id}, job_id={self.job_id}, error_type='{self.error_type}')>"
