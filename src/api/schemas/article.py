"""
Article schemas for Naija News Hub API.

This module provides Pydantic models for article data.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

class ArticleBase(BaseModel):
    """Base schema for article data."""
    title: str = Field(..., description="Title of the article")
    url: HttpUrl = Field(..., description="URL of the article")
    content: Optional[str] = Field(None, description="Content of the article")
    content_markdown: Optional[str] = Field(None, description="Markdown content of the article")
    content_html: Optional[str] = Field(None, description="HTML content of the article")
    author: Optional[str] = Field(None, description="Author of the article")
    published_at: Optional[datetime] = Field(None, description="When the article was published")
    image_url: Optional[HttpUrl] = Field(None, description="URL of the article image")
    website_id: int = Field(..., description="ID of the website")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata of the article")
    active: bool = Field(True, description="Whether the article is active")

class ArticleCreate(ArticleBase):
    """Schema for creating an article."""
    pass

class ArticleUpdate(BaseModel):
    """Schema for updating an article."""
    title: Optional[str] = Field(None, description="Title of the article")
    url: Optional[HttpUrl] = Field(None, description="URL of the article")
    content: Optional[str] = Field(None, description="Content of the article")
    content_markdown: Optional[str] = Field(None, description="Markdown content of the article")
    content_html: Optional[str] = Field(None, description="HTML content of the article")
    author: Optional[str] = Field(None, description="Author of the article")
    published_at: Optional[datetime] = Field(None, description="When the article was published")
    image_url: Optional[HttpUrl] = Field(None, description="URL of the article image")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata of the article")
    active: Optional[bool] = Field(None, description="Whether the article is active")

class ArticleResponse(ArticleBase):
    """Schema for article response."""
    id: int = Field(..., description="ID of the article")
    created_at: datetime = Field(..., description="When the article was created")
    updated_at: datetime = Field(..., description="When the article was last updated")
    
    class Config:
        orm_mode = True
