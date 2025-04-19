"""
Scraping API routes for Naija News Hub.

This module provides API routes for managing scraping jobs.
"""

import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from src.database_management.connection import get_db
from src.database_management.models import ScrapingJob, Website
from src.api_endpoints.schemas.scraping import ScrapingJobResponse, ScrapingJobCreate
from src.web_scraper.main import scrape_website, scrape_all_websites

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/jobs", response_model=List[ScrapingJobResponse])
async def get_scraping_jobs(
    skip: int = 0,
    limit: int = 100,
    website_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get all scraping jobs.

    Args:
        skip: Number of jobs to skip
        limit: Maximum number of jobs to return
        website_id: Filter by website ID
        status: Filter by job status
        db: Database session

    Returns:
        List of scraping jobs
    """
    query = db.query(ScrapingJob)

    # Apply filters
    if website_id:
        query = query.filter(ScrapingJob.website_id == website_id)

    if status:
        query = query.filter(ScrapingJob.status == status)

    # Get jobs
    jobs = query.order_by(ScrapingJob.created_at.desc()).offset(skip).limit(limit).all()
    return jobs

@router.get("/jobs/{job_id}", response_model=ScrapingJobResponse)
async def get_scraping_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a scraping job by ID.

    Args:
        job_id: ID of the job
        db: Database session

    Returns:
        Scraping job
    """
    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Scraping job not found")
    return job

@router.post("/website/{website_id}", response_model=ScrapingJobResponse)
async def start_website_scraping(
    website_id: int,
    background_tasks: BackgroundTasks,
    job: ScrapingJobCreate = None,
    db: Session = Depends(get_db),
):
    """
    Start scraping a website.

    Args:
        website_id: ID of the website to scrape
        background_tasks: FastAPI background tasks
        job: Optional scraping job configuration
        db: Database session

    Returns:
        Created scraping job
    """
    # Check if website exists
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    # Create scraping job
    config = job.model_dump() if job else {}

    # Start scraping in background
    background_tasks.add_task(scrape_website, website_id, config)

    # Return initial job status
    return {
        "id": 0,  # Placeholder ID
        "website_id": website_id,
        "status": "pending",
        "articles_found": 0,
        "articles_scraped": 0,
        "config": config,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

@router.post("/all", response_model=List[ScrapingJobResponse])
async def start_all_websites_scraping(
    background_tasks: BackgroundTasks,
    job: ScrapingJobCreate = None,
    db: Session = Depends(get_db),
):
    """
    Start scraping all active websites.

    Args:
        background_tasks: FastAPI background tasks
        job: Optional scraping job configuration
        db: Database session

    Returns:
        List of created scraping jobs
    """
    # Get all active websites
    websites = db.query(Website).filter(Website.active == True).all()

    # Create scraping jobs
    config = job.model_dump() if job else {}

    # Start scraping in background
    background_tasks.add_task(scrape_all_websites, config)

    # Return initial job statuses
    return [
        {
            "id": 0,  # Placeholder ID
            "website_id": website.id,
            "status": "pending",
            "articles_found": 0,
            "articles_scraped": 0,
            "config": config,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        for website in websites
    ]
