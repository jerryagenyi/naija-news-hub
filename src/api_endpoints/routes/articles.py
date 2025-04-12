"""
Articles API routes for Naija News Hub.

This module provides API routes for managing articles.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database_management.models import Article
from src.database_management.connection import get_db
from src.service_layer.article_service import ArticleService
from src.api.schemas.article import ArticleResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/", response_model=List[ArticleResponse])
async def get_articles(
    skip: int = 0,
    limit: int = 100,
    website_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get all articles.
    
    Args:
        skip: Number of articles to skip
        limit: Maximum number of articles to return
        website_id: Filter by website ID
        search: Search term for article title or content
        db: Database session
        
    Returns:
        List of articles
    """
    query = db.query(Article)
    
    # Apply filters
    if website_id:
        query = query.filter(Article.website_id == website_id)
    
    if search:
        query = query.filter(
            (Article.title.ilike(f"%{search}%")) | 
            (Article.content.ilike(f"%{search}%"))
        )
    
    # Get articles
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    return articles

@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """
    Get an article by ID.
    
    Args:
        article_id: ID of the article
        db: Database session
        
    Returns:
        Article
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.get("/url/{url:path}", response_model=ArticleResponse)
async def get_article_by_url(url: str, db: Session = Depends(get_db)):
    """
    Get an article by URL.
    
    Args:
        url: URL of the article
        db: Database session
        
    Returns:
        Article
    """
    article = db.query(Article).filter(Article.url == url).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
