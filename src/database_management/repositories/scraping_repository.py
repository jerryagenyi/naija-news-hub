"""
Scraping repository module for Naija News Hub.

This module provides functions to interact with the scraping_jobs and scraping_errors tables in the database.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

from src.database.models import ScrapingJob, ScrapingError, Website


class ScrapingRepository:
    """Repository for scraping job operations."""

    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.
        
        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db

    def create_job(self, job_data: Dict[str, Any]) -> ScrapingJob:
        """
        Create a new scraping job in the database.
        
        Args:
            job_data (Dict[str, Any]): Job data
            
        Returns:
            ScrapingJob: Created job
        """
        job = ScrapingJob(**job_data)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job_by_id(self, job_id: int) -> Optional[ScrapingJob]:
        """
        Get a scraping job by ID.
        
        Args:
            job_id (int): Job ID
            
        Returns:
            Optional[ScrapingJob]: Job if found, None otherwise
        """
        return self.db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()

    def get_jobs_by_website(self, website_id: int, limit: int = 10, offset: int = 0) -> List[ScrapingJob]:
        """
        Get scraping jobs for a website.
        
        Args:
            website_id (int): Website ID
            limit (int, optional): Maximum number of jobs to return. Defaults to 10.
            offset (int, optional): Offset for pagination. Defaults to 0.
            
        Returns:
            List[ScrapingJob]: List of jobs
        """
        return self.db.query(ScrapingJob).filter(
            ScrapingJob.website_id == website_id
        ).order_by(
            ScrapingJob.created_at.desc()
        ).limit(limit).offset(offset).all()

    def get_latest_job_by_website(self, website_id: int) -> Optional[ScrapingJob]:
        """
        Get the latest scraping job for a website.
        
        Args:
            website_id (int): Website ID
            
        Returns:
            Optional[ScrapingJob]: Latest job if found, None otherwise
        """
        return self.db.query(ScrapingJob).filter(
            ScrapingJob.website_id == website_id
        ).order_by(
            ScrapingJob.created_at.desc()
        ).first()

    def update_job(self, job_id: int, job_data: Dict[str, Any]) -> Optional[ScrapingJob]:
        """
        Update a scraping job.
        
        Args:
            job_id (int): Job ID
            job_data (Dict[str, Any]): Job data to update
            
        Returns:
            Optional[ScrapingJob]: Updated job if found, None otherwise
        """
        job = self.get_job_by_id(job_id)
        if not job:
            return None
            
        for key, value in job_data.items():
            setattr(job, key, value)
            
        job.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(job)
        return job

    def start_job(self, job_id: int) -> Optional[ScrapingJob]:
        """
        Mark a job as started.
        
        Args:
            job_id (int): Job ID
            
        Returns:
            Optional[ScrapingJob]: Updated job if found, None otherwise
        """
        job = self.get_job_by_id(job_id)
        if not job:
            return None
            
        job.status = "running"
        job.start_time = datetime.utcnow()
        job.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(job)
        return job

    def complete_job(self, job_id: int, articles_found: int, articles_scraped: int) -> Optional[ScrapingJob]:
        """
        Mark a job as completed.
        
        Args:
            job_id (int): Job ID
            articles_found (int): Number of articles found
            articles_scraped (int): Number of articles scraped
            
        Returns:
            Optional[ScrapingJob]: Updated job if found, None otherwise
        """
        job = self.get_job_by_id(job_id)
        if not job:
            return None
            
        job.status = "completed"
        job.end_time = datetime.utcnow()
        job.articles_found = articles_found
        job.articles_scraped = articles_scraped
        job.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(job)
        return job

    def fail_job(self, job_id: int, error_message: str) -> Optional[ScrapingJob]:
        """
        Mark a job as failed.
        
        Args:
            job_id (int): Job ID
            error_message (str): Error message
            
        Returns:
            Optional[ScrapingJob]: Updated job if found, None otherwise
        """
        job = self.get_job_by_id(job_id)
        if not job:
            return None
            
        job.status = "failed"
        job.end_time = datetime.utcnow()
        job.error_message = error_message
        job.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(job)
        return job

    def create_error(self, error_data: Dict[str, Any]) -> ScrapingError:
        """
        Create a new scraping error in the database.
        
        Args:
            error_data (Dict[str, Any]): Error data
            
        Returns:
            ScrapingError: Created error
        """
        error = ScrapingError(**error_data)
        self.db.add(error)
        self.db.commit()
        self.db.refresh(error)
        return error

    def get_errors_by_job(self, job_id: int) -> List[ScrapingError]:
        """
        Get scraping errors for a job.
        
        Args:
            job_id (int): Job ID
            
        Returns:
            List[ScrapingError]: List of errors
        """
        return self.db.query(ScrapingError).filter(
            ScrapingError.job_id == job_id
        ).order_by(
            ScrapingError.created_at.desc()
        ).all()

    def get_job_stats(self, website_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get statistics for scraping jobs.
        
        Args:
            website_id (Optional[int], optional): Website ID. Defaults to None.
            
        Returns:
            Dict[str, Any]: Job statistics
        """
        query = self.db.query(ScrapingJob)
        if website_id:
            query = query.filter(ScrapingJob.website_id == website_id)
            
        total_jobs = query.count()
        completed_jobs = query.filter(ScrapingJob.status == "completed").count()
        failed_jobs = query.filter(ScrapingJob.status == "failed").count()
        running_jobs = query.filter(ScrapingJob.status == "running").count()
        pending_jobs = query.filter(ScrapingJob.status == "pending").count()
        
        total_articles_found = query.with_entities(func.sum(ScrapingJob.articles_found)).scalar() or 0
        total_articles_scraped = query.with_entities(func.sum(ScrapingJob.articles_scraped)).scalar() or 0
        
        return {
            "total_jobs": total_jobs,
            "completed_jobs": completed_jobs,
            "failed_jobs": failed_jobs,
            "running_jobs": running_jobs,
            "pending_jobs": pending_jobs,
            "total_articles_found": total_articles_found,
            "total_articles_scraped": total_articles_scraped
        }

    def get_recent_jobs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent scraping jobs with website information.
        
        Args:
            limit (int, optional): Maximum number of jobs to return. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of jobs with website information
        """
        jobs = self.db.query(
            ScrapingJob, Website.name.label("website_name")
        ).join(
            Website, ScrapingJob.website_id == Website.id
        ).order_by(
            ScrapingJob.created_at.desc()
        ).limit(limit).all()
        
        result = []
        for job, website_name in jobs:
            job_dict = {
                "id": job.id,
                "website_id": job.website_id,
                "website_name": website_name,
                "status": job.status,
                "start_time": job.start_time,
                "end_time": job.end_time,
                "articles_found": job.articles_found,
                "articles_scraped": job.articles_scraped,
                "created_at": job.created_at
            }
            result.append(job_dict)
            
        return result
