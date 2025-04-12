"""
Category API endpoints for Naija News Hub.

This module provides API endpoints for category management.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database_management.connection import get_db
from src.database_management.models import Category, Website
from src.database_management.repositories.website_repository import WebsiteRepository
from src.database_management.repositories.article_repository import ArticleRepository

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Pydantic models for request/response
class CategoryBase(BaseModel):
    """Base model for category data."""
    name: str
    url: str

class CategoryCreate(CategoryBase):
    """Model for creating a category."""
    pass

class CategoryUpdate(BaseModel):
    """Model for updating a category."""
    name: Optional[str] = None
    url: Optional[str] = None
    active: Optional[bool] = None

class CategoryResponse(CategoryBase):
    """Model for category response."""
    id: int
    website_id: int
    active: bool
    
    class Config:
        from_attributes = True

class CategoryWithArticlesCount(CategoryResponse):
    """Model for category response with article count."""
    articles_count: int

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    website_id: Optional[int] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all categories.
    
    Args:
        website_id: Filter by website ID
        active_only: If True, only return active categories
        skip: Number of categories to skip
        limit: Maximum number of categories to return
        db: Database session
        
    Returns:
        List of categories
    """
    query = db.query(Category)
    
    if website_id:
        query = query.filter(Category.website_id == website_id)
    
    if active_only:
        query = query.filter(Category.active == True)
    
    categories = query.offset(skip).limit(limit).all()
    return categories

@router.get("/stats", response_model=List[CategoryWithArticlesCount])
async def get_categories_with_stats(
    website_id: Optional[int] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all categories with article counts.
    
    Args:
        website_id: Filter by website ID
        active_only: If True, only return active categories
        skip: Number of categories to skip
        limit: Maximum number of categories to return
        db: Database session
        
    Returns:
        List of categories with article counts
    """
    # Get categories
    website_repo = WebsiteRepository(db)
    article_repo = ArticleRepository(db)
    
    if website_id:
        categories = website_repo.get_website_categories(website_id, active_only)
    else:
        query = db.query(Category)
        if active_only:
            query = query.filter(Category.active == True)
        categories = query.offset(skip).limit(limit).all()
    
    # Get article counts for each category
    result = []
    for category in categories:
        articles = article_repo.get_articles_by_category(category.id, limit=0)
        result.append(CategoryWithArticlesCount(
            id=category.id,
            name=category.name,
            url=category.url,
            website_id=category.website_id,
            active=category.active,
            articles_count=len(articles)
        ))
    
    return result

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a category by ID.
    
    Args:
        category_id: Category ID
        db: Database session
        
    Returns:
        Category
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    website_id: int,
    db: Session = Depends(get_db),
):
    """
    Create a new category.
    
    Args:
        category: Category data
        website_id: Website ID
        db: Database session
        
    Returns:
        Created category
    """
    # Check if website exists
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    # Check if category with same name already exists
    existing_category = db.query(Category).filter(
        Category.website_id == website_id,
        Category.name == category.name
    ).first()
    
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists for this website")
    
    # Create new category
    db_category = Category(
        name=category.name,
        url=category.url,
        website_id=website_id,
        active=True
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    logger.info(f"Created category {db_category.name} for website {website_id}")
    
    return db_category

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a category.
    
    Args:
        category_id: Category ID
        category: Category data
        db: Database session
        
    Returns:
        Updated category
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Update category
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    
    logger.info(f"Updated category {db_category.name} (ID: {category_id})")
    
    return db_category

@router.delete("/{category_id}", response_model=dict)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a category.
    
    Args:
        category_id: Category ID
        db: Database session
        
    Returns:
        Success message
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Instead of deleting, mark as inactive
    db_category.active = False
    db.commit()
    
    logger.info(f"Marked category {db_category.name} (ID: {category_id}) as inactive")
    
    return {"message": "Category marked as inactive"}

@router.get("/{category_id}/articles", response_model=dict)
async def get_category_articles(
    category_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get articles for a category.
    
    Args:
        category_id: Category ID
        skip: Number of articles to skip
        limit: Maximum number of articles to return
        db: Database session
        
    Returns:
        List of articles
    """
    # Check if category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Get articles
    article_repo = ArticleRepository(db)
    articles = article_repo.get_articles_by_category(category_id, limit=limit, offset=skip)
    
    # Format response
    result = {
        "category": {
            "id": category.id,
            "name": category.name,
            "url": category.url,
            "website_id": category.website_id
        },
        "articles": [
            {
                "id": article.id,
                "title": article.title,
                "url": article.url,
                "published_at": article.published_at,
                "image_url": article.image_url
            }
            for article in articles
        ],
        "total": len(articles),
        "skip": skip,
        "limit": limit
    }
    
    return result
