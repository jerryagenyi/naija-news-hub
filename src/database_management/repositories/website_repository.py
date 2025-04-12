"""
Website repository module for Naija News Hub.

This module provides functions to interact with the websites table in the database.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.database.models import Website, Category


class WebsiteRepository:
    """Repository for website operations."""

    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.
        
        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db

    def create_website(self, website_data: Dict[str, Any]) -> Website:
        """
        Create a new website in the database.
        
        Args:
            website_data (Dict[str, Any]): Website data
            
        Returns:
            Website: Created website
            
        Raises:
            IntegrityError: If the website already exists
        """
        website = Website(**website_data)
        self.db.add(website)
        try:
            self.db.commit()
            self.db.refresh(website)
            return website
        except IntegrityError:
            self.db.rollback()
            raise

    def get_website_by_id(self, website_id: int) -> Optional[Website]:
        """
        Get a website by ID.
        
        Args:
            website_id (int): Website ID
            
        Returns:
            Optional[Website]: Website if found, None otherwise
        """
        return self.db.query(Website).filter(Website.id == website_id).first()

    def get_website_by_url(self, base_url: str) -> Optional[Website]:
        """
        Get a website by base URL.
        
        Args:
            base_url (str): Website base URL
            
        Returns:
            Optional[Website]: Website if found, None otherwise
        """
        return self.db.query(Website).filter(Website.base_url == base_url).first()

    def get_all_websites(self, active_only: bool = True) -> List[Website]:
        """
        Get all websites.
        
        Args:
            active_only (bool, optional): Only return active websites. Defaults to True.
            
        Returns:
            List[Website]: List of websites
        """
        query = self.db.query(Website)
        if active_only:
            query = query.filter(Website.active == True)
        return query.all()

    def update_website(self, website_id: int, website_data: Dict[str, Any]) -> Optional[Website]:
        """
        Update a website.
        
        Args:
            website_id (int): Website ID
            website_data (Dict[str, Any]): Website data to update
            
        Returns:
            Optional[Website]: Updated website if found, None otherwise
        """
        website = self.get_website_by_id(website_id)
        if not website:
            return None
            
        for key, value in website_data.items():
            setattr(website, key, value)
            
        website.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(website)
        return website

    def delete_website(self, website_id: int) -> bool:
        """
        Delete a website.
        
        Args:
            website_id (int): Website ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        website = self.get_website_by_id(website_id)
        if not website:
            return False
            
        self.db.delete(website)
        self.db.commit()
        return True

    def create_category(self, website_id: int, category_data: Dict[str, Any]) -> Category:
        """
        Create a new category for a website.
        
        Args:
            website_id (int): Website ID
            category_data (Dict[str, Any]): Category data
            
        Returns:
            Category: Created category
            
        Raises:
            IntegrityError: If the category already exists
        """
        category_data['website_id'] = website_id
        category = Category(**category_data)
        self.db.add(category)
        try:
            self.db.commit()
            self.db.refresh(category)
            return category
        except IntegrityError:
            self.db.rollback()
            raise

    def get_website_categories(self, website_id: int, active_only: bool = True) -> List[Category]:
        """
        Get categories for a website.
        
        Args:
            website_id (int): Website ID
            active_only (bool, optional): Only return active categories. Defaults to True.
            
        Returns:
            List[Category]: List of categories
        """
        query = self.db.query(Category).filter(Category.website_id == website_id)
        if active_only:
            query = query.filter(Category.active == True)
        return query.all()

    def get_category_by_url(self, website_id: int, url: str) -> Optional[Category]:
        """
        Get a category by URL.
        
        Args:
            website_id (int): Website ID
            url (str): Category URL
            
        Returns:
            Optional[Category]: Category if found, None otherwise
        """
        return self.db.query(Category).filter(
            Category.website_id == website_id,
            Category.url == url
        ).first()

    def get_category_by_name(self, website_id: int, name: str) -> Optional[Category]:
        """
        Get a category by name.
        
        Args:
            website_id (int): Website ID
            name (str): Category name
            
        Returns:
            Optional[Category]: Category if found, None otherwise
        """
        return self.db.query(Category).filter(
            Category.website_id == website_id,
            Category.name == name
        ).first()

    def get_websites_count(self) -> int:
        """
        Get the count of websites.
        
        Returns:
            int: Count of websites
        """
        return self.db.query(func.count(Website.id)).scalar() or 0

    def create_or_update_website(self, website_data: Dict[str, Any]) -> Website:
        """
        Create a new website or update an existing one.
        
        Args:
            website_data (Dict[str, Any]): Website data
            
        Returns:
            Website: Created or updated website
        """
        base_url = website_data.get('base_url')
        if not base_url:
            raise ValueError("Website base URL is required")
            
        existing_website = self.get_website_by_url(base_url)
        
        if existing_website:
            # Update existing website
            for key, value in website_data.items():
                setattr(existing_website, key, value)
                
            existing_website.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing_website)
            return existing_website
        else:
            # Create new website
            return self.create_website(website_data)

    def create_or_update_category(self, website_id: int, category_data: Dict[str, Any]) -> Category:
        """
        Create a new category or update an existing one.
        
        Args:
            website_id (int): Website ID
            category_data (Dict[str, Any]): Category data
            
        Returns:
            Category: Created or updated category
        """
        url = category_data.get('url')
        if not url:
            raise ValueError("Category URL is required")
            
        existing_category = self.get_category_by_url(website_id, url)
        
        if existing_category:
            # Update existing category
            for key, value in category_data.items():
                setattr(existing_category, key, value)
                
            existing_category.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing_category)
            return existing_category
        else:
            # Create new category
            return self.create_category(website_id, category_data)
