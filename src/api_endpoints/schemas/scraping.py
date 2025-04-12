"""
Scraping job schemas for Naija News Hub API.

This module provides Pydantic models for scraping job data.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ScrapingJobBase(BaseModel):
    """Base schema for scraping job data."""
    website_id: int = Field(..., description="ID of the website")
    status: str = Field("pending", description="Status of the job")
    articles_found: int = Field(0, description="Number of articles found")
    articles_scraped: int = Field(0, description="Number of articles scraped")
    error_message: Optional[str] = Field(None, description="Error message if job failed")
    config: Optional[Dict[str, Any]] = Field(None, description="Configuration for the job")

class ScrapingJobCreate(BaseModel):
    """Schema for creating a scraping job."""
    config: Optional[Dict[str, Any]] = Field(None, description="Configuration for the job")

class ScrapingJobUpdate(BaseModel):
    """Schema for updating a scraping job."""
    status: Optional[str] = Field(None, description="Status of the job")
    articles_found: Optional[int] = Field(None, description="Number of articles found")
    articles_scraped: Optional[int] = Field(None, description="Number of articles scraped")
    error_message: Optional[str] = Field(None, description="Error message if job failed")

class ScrapingJobResponse(ScrapingJobBase):
    """Schema for scraping job response."""
    id: int = Field(..., description="ID of the job")
    start_time: Optional[datetime] = Field(None, description="When the job started")
    end_time: Optional[datetime] = Field(None, description="When the job ended")
    created_at: datetime = Field(..., description="When the job was created")
    updated_at: datetime = Field(..., description="When the job was last updated")
    
    class Config:
        orm_mode = True
