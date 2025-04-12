"""
Dashboard service for Naija News Hub.

This module provides services for monitoring and displaying scraping operations.
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database_management.repositories.scraping_repository import ScrapingRepository
from src.database_management.repositories.article_repository import ArticleRepository

class DashboardService:
    """Service for dashboard operations."""

    def __init__(self, db: Session):
        """
        Initialize the service with a database session.

        Args:
            db (Session): SQLAlchemy database session
        """
        self.scraping_repo = ScrapingRepository(db)
        self.article_repo = ArticleRepository(db)

    def get_overview_stats(self) -> Dict[str, Any]:
        """
        Get overview statistics for the dashboard.

        Returns:
            Dict[str, Any]: Overview statistics
        """
        # Get job statistics
        job_stats = self.scraping_repo.get_job_stats()
        
        # Get article statistics
        total_articles = self.article_repo.get_articles_count()
        
        # Get recent jobs
        recent_jobs = self.scraping_repo.get_recent_jobs(limit=5)
        
        return {
            "job_stats": job_stats,
            "total_articles": total_articles,
            "recent_jobs": recent_jobs
        }

    def get_website_stats(self, website_id: int) -> Dict[str, Any]:
        """
        Get statistics for a specific website.

        Args:
            website_id (int): Website ID

        Returns:
            Dict[str, Any]: Website statistics
        """
        # Get job statistics for website
        job_stats = self.scraping_repo.get_job_stats(website_id)
        
        # Get article statistics for website
        total_articles = self.article_repo.get_articles_count(website_id)
        
        # Get latest article date
        latest_article_date = self.article_repo.get_latest_article_date(website_id)
        
        # Get recent jobs for website
        recent_jobs = self.scraping_repo.get_jobs_by_website(website_id, limit=5)
        
        return {
            "job_stats": job_stats,
            "total_articles": total_articles,
            "latest_article_date": latest_article_date,
            "recent_jobs": recent_jobs
        }

    def get_error_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Get error summary for the specified number of days.

        Args:
            days (int, optional): Number of days to look back. Defaults to 7.

        Returns:
            Dict[str, Any]: Error summary
        """
        # Get recent errors
        recent_errors = self.scraping_repo.get_errors_by_job(None)  # Get all errors
        
        # Filter by date
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        recent_errors = [error for error in recent_errors if error.created_at >= cutoff_date]
        
        # Group by error type
        error_types = {}
        for error in recent_errors:
            error_type = error.error_type
            if error_type not in error_types:
                error_types[error_type] = 0
            error_types[error_type] += 1
        
        return {
            "total_errors": len(recent_errors),
            "error_types": error_types,
            "recent_errors": recent_errors[:10]  # Get 10 most recent errors
        }

    def get_performance_metrics(self, days: int = 7) -> Dict[str, Any]:
        """
        Get performance metrics for scraping operations.

        Args:
            days (int, optional): Number of days to look back. Defaults to 7.

        Returns:
            Dict[str, Any]: Performance metrics
        """
        # Get all jobs within the time period
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        jobs = self.scraping_repo.get_recent_jobs(limit=100)  # Adjust limit as needed
        
        # Calculate metrics
        total_jobs = len(jobs)
        successful_jobs = sum(1 for job in jobs if job["status"] == "completed")
        failed_jobs = sum(1 for job in jobs if job["status"] == "failed")
        
        # Calculate average articles per job
        total_articles = sum(job["articles_scraped"] for job in jobs)
        avg_articles_per_job = total_articles / total_jobs if total_jobs > 0 else 0
        
        # Calculate average job duration
        durations = []
        for job in jobs:
            if job["start_time"] and job["end_time"]:
                duration = (job["end_time"] - job["start_time"]).total_seconds()
                durations.append(duration)
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_jobs": total_jobs,
            "success_rate": (successful_jobs / total_jobs * 100) if total_jobs > 0 else 0,
            "failure_rate": (failed_jobs / total_jobs * 100) if total_jobs > 0 else 0,
            "avg_articles_per_job": avg_articles_per_job,
            "avg_job_duration": avg_duration
        } 