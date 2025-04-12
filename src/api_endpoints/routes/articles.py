"""
Articles API routes for Naija News Hub.

This module provides API routes for managing articles.
"""

import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from src.database_management.models import Article
from src.database_management.connection import get_db
from src.service_layer.article_service import ArticleService
from src.api_endpoints.schemas.article import ArticleResponse, ArticleUpdateResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Background task for updating articles
async def update_article_task(article_id: int, url: str, website_id: int, force_update: bool, db: Session):
    """Background task for updating an article."""
    try:
        article_service = ArticleService(db)
        result = await article_service.extract_and_store_article(url, website_id, force_update)
        if result:
            logger.info(f"Article update completed: {result}")
        else:
            logger.error(f"Failed to update article: {url}")
    except Exception as e:
        logger.error(f"Error updating article {url}: {str(e)}")

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

@router.post("/{article_id}/update", response_model=ArticleUpdateResponse)
async def update_article(
    article_id: int,
    background_tasks: BackgroundTasks,
    force_update: bool = False,
    db: Session = Depends(get_db),
):
    """
    Update an article by ID.

    Args:
        article_id: Article ID
        background_tasks: Background tasks
        force_update: Force update even if article was recently updated
        db: Database session

    Returns:
        Update status
    """
    # Get the article
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Update the article in the background
    background_tasks.add_task(
        update_article_task,
        article_id=article_id,
        url=article.url,
        website_id=article.website_id,
        force_update=force_update,
        db=db
    )

    return {
        "id": article.id,
        "title": article.title,
        "url": article.url,
        "status": "pending",
        "last_checked_at": article.last_checked_at,
        "message": "Article update has been scheduled"
    }

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
