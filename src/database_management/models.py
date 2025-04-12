"""
Database models for Naija News Hub.

This module defines the SQLAlchemy ORM models for the database.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from src.utils.enums import ErrorType, ErrorSeverity

class Base(DeclarativeBase):
    pass

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
    """Model for tracking scraping jobs."""
    __tablename__ = 'scraping_jobs'

    id = Column(Integer, primary_key=True)
    status = Column(String(50), nullable=False, default='pending')
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    error_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    errors = relationship("ErrorLog", back_populates="job", cascade="all, delete-orphan")
    articles = relationship("Article", back_populates="job", cascade="all, delete-orphan")

class ErrorLog(Base):
    """Model for tracking errors during scraping."""
    __tablename__ = 'error_logs'

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('scraping_jobs.id', ondelete='CASCADE'), nullable=False)
    error_type = Column(Enum(ErrorType), nullable=False)
    severity = Column(Enum(ErrorSeverity), nullable=False)
    error_message = Column(Text, nullable=False)
    url = Column(String(500))
    context = Column(Text)
    stack_trace = Column(Text)
    recovery_actions = Column(Text)
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job = relationship("ScrapingJob", back_populates="errors")
