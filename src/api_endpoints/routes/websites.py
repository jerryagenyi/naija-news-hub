"""
Websites API routes for Naija News Hub.

This module provides API routes for managing websites.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database_management.connection import get_db
from src.database_management.models import Website
from src.api_endpoints.schemas.website import WebsiteCreate, WebsiteResponse, WebsiteUpdate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/", response_model=List[WebsiteResponse])
async def get_websites(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    """
    Get all websites.
    
    Args:
        skip: Number of websites to skip
        limit: Maximum number of websites to return
        active_only: If True, only return active websites
        db: Database session
        
    Returns:
        List of websites
    """
    query = db.query(Website)
    
    if active_only:
        query = query.filter(Website.active == True)
    
    websites = query.offset(skip).limit(limit).all()
    return websites

@router.get("/{website_id}", response_model=WebsiteResponse)
async def get_website(website_id: int, db: Session = Depends(get_db)):
    """
    Get a website by ID.
    
    Args:
        website_id: ID of the website
        db: Database session
        
    Returns:
        Website
    """
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    return website

@router.post("/", response_model=WebsiteResponse)
async def create_website(website: WebsiteCreate, db: Session = Depends(get_db)):
    """
    Create a new website.
    
    Args:
        website: Website data
        db: Database session
        
    Returns:
        Created website
    """
    # Check if website with same base_url already exists
    existing_website = db.query(Website).filter(Website.base_url == website.base_url).first()
    if existing_website:
        raise HTTPException(status_code=400, detail="Website with this base URL already exists")
    
    # Create new website
    db_website = Website(**website.dict())
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    
    logger.info(f"Created website {db_website.name} ({db_website.base_url})")
    
    return db_website

@router.put("/{website_id}", response_model=WebsiteResponse)
async def update_website(website_id: int, website: WebsiteUpdate, db: Session = Depends(get_db)):
    """
    Update a website.
    
    Args:
        website_id: ID of the website to update
        website: Website data
        db: Database session
        
    Returns:
        Updated website
    """
    db_website = db.query(Website).filter(Website.id == website_id).first()
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    # Update website
    for key, value in website.dict(exclude_unset=True).items():
        setattr(db_website, key, value)
    
    db.commit()
    db.refresh(db_website)
    
    logger.info(f"Updated website {db_website.name} ({db_website.base_url})")
    
    return db_website

@router.delete("/{website_id}")
async def delete_website(website_id: int, db: Session = Depends(get_db)):
    """
    Delete a website.
    
    Args:
        website_id: ID of the website to delete
        db: Database session
        
    Returns:
        Success message
    """
    db_website = db.query(Website).filter(Website.id == website_id).first()
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    # Delete website
    db.delete(db_website)
    db.commit()
    
    logger.info(f"Deleted website {db_website.name} ({db_website.base_url})")
    
    return {"message": "Website deleted successfully"}
