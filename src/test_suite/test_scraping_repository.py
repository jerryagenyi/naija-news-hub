"""
Tests for the ScrapingRepository class.

This module provides tests for the ScrapingRepository class.
"""

import pytest
from datetime import datetime, timedelta

from src.database_management.models import ScrapingJob, ErrorLog
from src.database_management.repositories.scraping_repository import ScrapingRepository
from src.utility_modules.enums import ErrorType, ErrorSeverity
import enum

class TestScrapingRepository:
    """Test cases for ScrapingRepository."""

    def test_create_job(self, scraping_repository, sample_website):
        """Test creating a scraping job."""
        # Prepare job data
        job_data = {
            "website_id": sample_website.id,
            "status": "pending",
            "config": {
                "max_articles": 10,
                "max_concurrent": 5
            },
            "articles_found": 0,
            "articles_scraped": 0
        }

        # Create job
        job = scraping_repository.create_job(job_data)

        # Verify job was created
        assert job.id is not None
        assert job.website_id == sample_website.id
        assert job.status == "pending"
        assert job.config["max_articles"] == 10
        assert job.config["max_concurrent"] == 5
        assert job.articles_found == 0
        assert job.articles_scraped == 0

    def test_get_job_by_id(self, scraping_repository, sample_scraping_job):
        """Test getting a scraping job by ID."""
        # Get job by ID
        job = scraping_repository.get_job_by_id(sample_scraping_job.id)

        # Verify job was retrieved
        assert job is not None
        assert job.id == sample_scraping_job.id
        assert job.website_id == sample_scraping_job.website_id
        assert job.status == sample_scraping_job.status

    def test_get_job_by_id_not_found(self, scraping_repository):
        """Test getting a scraping job by ID that doesn't exist."""
        # Get job by non-existent ID
        job = scraping_repository.get_job_by_id(999)

        # Verify job was not found
        assert job is None

    def test_get_jobs_by_website(self, scraping_repository, sample_website, sample_scraping_job):
        """Test getting scraping jobs by website ID."""
        # Create another job for the same website
        job_data = {
            "website_id": sample_website.id,
            "status": "completed",
            "config": {
                "max_articles": 5,
                "max_concurrent": 2
            },
            "articles_found": 5,
            "articles_scraped": 5
        }
        scraping_repository.create_job(job_data)

        # Get jobs by website ID
        jobs = scraping_repository.get_jobs_by_website(sample_website.id)

        # Verify jobs were retrieved
        assert len(jobs) == 2

    def test_filter_jobs_by_status(self, scraping_repository, sample_website, sample_scraping_job):
        """Test filtering jobs by status using direct query."""
        # Create jobs with different statuses
        statuses = ["pending", "running", "completed", "failed"]
        for status in statuses:
            job_data = {
                "website_id": sample_website.id,
                "status": status,
                "config": {
                    "max_articles": 5,
                    "max_concurrent": 2
                }
            }
            scraping_repository.create_job(job_data)

        # Get jobs by status using direct query
        for status in statuses:
            jobs = scraping_repository.db.query(ScrapingJob).filter(ScrapingJob.status == status).all()
            assert len(jobs) >= 1
            for job in jobs:
                assert job.status == status

    def test_update_job(self, scraping_repository, sample_scraping_job):
        """Test updating a scraping job."""
        # Prepare update data
        update_data = {
            "status": "running",
            "articles_found": 10,
            "articles_scraped": 5
        }

        # Update job
        updated_job = scraping_repository.update_job(sample_scraping_job.id, update_data)

        # Verify job was updated
        assert updated_job is not None
        assert updated_job.id == sample_scraping_job.id
        assert updated_job.status == "running"
        assert updated_job.articles_found == 10
        assert updated_job.articles_scraped == 5

    def test_update_job_not_found(self, scraping_repository):
        """Test updating a scraping job that doesn't exist."""
        # Prepare update data
        update_data = {
            "status": "running",
            "articles_found": 10,
            "articles_scraped": 5
        }

        # Update non-existent job
        updated_job = scraping_repository.update_job(999, update_data)

        # Verify job was not found
        assert updated_job is None

    def test_start_job(self, scraping_repository, sample_scraping_job):
        """Test starting a scraping job."""
        # Start job
        job = scraping_repository.start_job(sample_scraping_job.id)

        # Verify job was started
        assert job is not None
        assert job.id == sample_scraping_job.id
        assert job.status == "running"
        assert job.start_time is not None

    def test_complete_job(self, scraping_repository, sample_scraping_job):
        """Test completing a scraping job."""
        # Start job first
        scraping_repository.start_job(sample_scraping_job.id)

        # Complete job
        job = scraping_repository.complete_job(sample_scraping_job.id, 10, 8)

        # Verify job was completed
        assert job is not None
        assert job.id == sample_scraping_job.id
        assert job.status == "completed"
        assert job.end_time is not None
        assert job.articles_found == 10
        assert job.articles_scraped == 8

    def test_fail_job(self, scraping_repository, sample_scraping_job):
        """Test failing a scraping job."""
        # Start job first
        scraping_repository.start_job(sample_scraping_job.id)

        # Fail job
        error_message = "Connection timeout"
        job = scraping_repository.fail_job(sample_scraping_job.id, error_message)

        # Verify job was failed
        assert job is not None
        assert job.id == sample_scraping_job.id
        assert job.status == "failed"
        assert job.end_time is not None
        assert job.error_message == error_message

    def test_get_recent_jobs(self, scraping_repository, sample_website):
        """Test getting recent scraping jobs."""
        # Create multiple jobs with different timestamps
        now = datetime.utcnow()
        for i in range(5):
            job_data = {
                "website_id": sample_website.id,
                "status": "completed",
                "start_time": now - timedelta(hours=i),
                "end_time": now - timedelta(hours=i) + timedelta(minutes=30),
                "articles_found": 10,
                "articles_scraped": 8
            }
            scraping_repository.create_job(job_data)

        # Get recent jobs
        limit = 3
        jobs = scraping_repository.get_recent_jobs(limit=limit)

        # Verify jobs were retrieved
        assert len(jobs) == limit

        # Verify jobs are ordered by created_at desc (most recent first)
        for i in range(len(jobs) - 1):
            assert jobs[i]["created_at"] >= jobs[i + 1]["created_at"]

    def test_get_job_stats(self, scraping_repository, sample_website):
        """Test getting scraping job statistics."""
        # Create jobs with different statuses
        statuses = {
            "pending": 2,
            "running": 1,
            "completed": 3,
            "failed": 2
        }

        for status, count in statuses.items():
            for _ in range(count):
                job_data = {
                    "website_id": sample_website.id,
                    "status": status,
                    "articles_found": 10 if status in ["completed", "failed"] else 0,
                    "articles_scraped": 8 if status == "completed" else 0
                }
                scraping_repository.create_job(job_data)

        # Get job stats
        stats = scraping_repository.get_job_stats()

        # Verify stats are correct
        assert stats["total_jobs"] == sum(statuses.values())
        assert stats["pending_jobs"] == statuses["pending"]
        assert stats["running_jobs"] == statuses["running"]
        assert stats["completed_jobs"] == statuses["completed"]
        assert stats["failed_jobs"] == statuses["failed"]
        assert stats["total_articles_found"] == (statuses["completed"] + statuses["failed"]) * 10
        assert stats["total_articles_scraped"] == statuses["completed"] * 8

    def test_create_error(self, scraping_repository, sample_scraping_job):
        """Test creating a scraping error."""
        # Prepare error data
        error_data = {
            "job_id": sample_scraping_job.id,
            "error_type": ErrorType.NETWORK,  # Use enum value
            "severity": ErrorSeverity.MEDIUM,  # Use enum value
            "error_message": "Connection timeout",
            "url": "https://example.com/test-article",
            "context": "Trying to fetch article content",
            "stack_trace": "Traceback..."
        }

        # Create error
        error = scraping_repository.create_error(error_data)

        # Verify error was created
        assert error.id is not None
        assert error.job_id == sample_scraping_job.id
        assert error.error_type == ErrorType.NETWORK
        assert error.severity == ErrorSeverity.MEDIUM
        assert error.error_message == "Connection timeout"
        assert error.url == "https://example.com/test-article"

    def test_get_errors_by_job(self, scraping_repository, sample_scraping_job):
        """Test getting errors for a scraping job."""
        # Create errors for the job
        for i in range(3):
            error_data = {
                "job_id": sample_scraping_job.id,
                "error_type": ErrorType.CONTENT,  # Use enum value
                "severity": ErrorSeverity.LOW,    # Use enum value
                "error_message": f"Parsing error {i+1}",
                "url": f"https://example.com/test-article-{i+1}",
                "context": "Trying to parse article content"
            }
            scraping_repository.create_error(error_data)

        # Get errors by job ID
        errors = scraping_repository.get_errors_by_job(sample_scraping_job.id)

        # Verify errors were retrieved
        assert len(errors) == 3

        # Verify errors have the correct job_id
        for error in errors:
            assert error.job_id == sample_scraping_job.id
