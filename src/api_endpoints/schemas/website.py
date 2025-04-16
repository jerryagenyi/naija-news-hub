"""
Website schemas for Naija News Hub API.

This module provides Pydantic models for website data.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

class WebsiteBase(BaseModel):
    """Base schema for website data."""
    name: str = Field(..., description="Name of the website")
    base_url: HttpUrl = Field(..., description="Base URL of the website")
    description: Optional[str] = Field(None, description="Description of the website")
    logo_url: Optional[HttpUrl] = Field(None, description="URL of the website logo")
    sitemap_url: Optional[HttpUrl] = Field(None, description="URL of the website sitemap")
    active: bool = Field(True, description="Whether the website is active")

    def model_dump(self, *args, **kwargs):
        """Convert HttpUrl fields to strings for SQLAlchemy compatibility."""
        d = super().model_dump(*args, **kwargs)
        if d.get('base_url'):
            d['base_url'] = str(d['base_url'])
        if d.get('logo_url'):
            d['logo_url'] = str(d['logo_url'])
        if d.get('sitemap_url'):
            d['sitemap_url'] = str(d['sitemap_url'])
        return d

    # For backward compatibility
    def dict(self, *args, **kwargs):
        """Deprecated: Use model_dump instead."""
        return self.model_dump(*args, **kwargs)

class WebsiteCreate(WebsiteBase):
    """Schema for creating a website."""
    pass

class WebsiteUpdate(BaseModel):
    """Schema for updating a website."""
    name: Optional[str] = Field(None, description="Name of the website")
    base_url: Optional[HttpUrl] = Field(None, description="Base URL of the website")
    description: Optional[str] = Field(None, description="Description of the website")
    logo_url: Optional[HttpUrl] = Field(None, description="URL of the website logo")
    sitemap_url: Optional[HttpUrl] = Field(None, description="URL of the website sitemap")
    active: Optional[bool] = Field(None, description="Whether the website is active")

    def model_dump(self, *args, **kwargs):
        """Convert HttpUrl fields to strings for SQLAlchemy compatibility."""
        d = super().model_dump(*args, **kwargs)
        if d.get('base_url'):
            d['base_url'] = str(d['base_url'])
        if d.get('logo_url'):
            d['logo_url'] = str(d['logo_url'])
        if d.get('sitemap_url'):
            d['sitemap_url'] = str(d['sitemap_url'])
        return d

    # For backward compatibility
    def dict(self, *args, **kwargs):
        """Deprecated: Use model_dump instead."""
        return self.model_dump(*args, **kwargs)

class WebsiteResponse(WebsiteBase):
    """Schema for website response."""
    id: int = Field(..., description="ID of the website")
    created_at: datetime = Field(..., description="When the website was created")
    updated_at: datetime = Field(..., description="When the website was last updated")

    class Config:
        from_attributes = True
