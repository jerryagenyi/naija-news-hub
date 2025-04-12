"""
Test suite for the dashboard service.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch, MagicMock
import os
from dotenv import load_dotenv

from src.service_layer.dashboard_service import DashboardService
from src.database_management.models import ScrapingJob, ErrorLog

# Load environment variables
load_dotenv()

@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return Mock(spec=Session)

@pytest.fixture
def dashboard_service(mock_db):
    """Create a dashboard service instance with mock database."""
    # Create mock repositories
    scraping_repo = MagicMock()
    article_repo = MagicMock()
    
    # Create service instance
    service = DashboardService(mock_db)
    service.scraping_repo = scraping_repo
    service.article_repo = article_repo
    
    return service

def test_get_overview_stats(dashboard_service, mock_db):
    """Test getting overview statistics."""
    # Mock repository responses
    dashboard_service.scraping_repo.get_job_stats.return_value = {
        "total": 100,
        "completed": 80,
        "failed": 20
    }
    dashboard_service.article_repo.get_articles_count.return_value = 500
    dashboard_service.scraping_repo.get_recent_jobs.return_value = [
        {"id": 1, "status": "completed"},
        {"id": 2, "status": "failed"}
    ]
    
    # Get overview stats
    stats = dashboard_service.get_overview_stats()
    
    # Verify results
    assert stats["job_stats"]["total"] == 100
    assert stats["total_articles"] == 500
    assert len(stats["recent_jobs"]) == 2

def test_get_website_stats(dashboard_service, mock_db):
    """Test getting website-specific statistics."""
    # Mock repository responses
    dashboard_service.scraping_repo.get_job_stats.return_value = {
        "total": 50,
        "completed": 40,
        "failed": 10
    }
    dashboard_service.article_repo.get_articles_count.return_value = 200
    dashboard_service.article_repo.get_latest_article_date.return_value = datetime.utcnow()
    dashboard_service.scraping_repo.get_jobs_by_website.return_value = [
        {"id": 1, "status": "completed"},
        {"id": 2, "status": "failed"}
    ]
    
    # Get website stats
    stats = dashboard_service.get_website_stats(website_id=1)
    
    # Verify results
    assert stats["job_stats"]["total"] == 50
    assert stats["total_articles"] == 200
    assert isinstance(stats["latest_article_date"], datetime)
    assert len(stats["recent_jobs"]) == 2

def test_get_error_summary(dashboard_service, mock_db):
    """Test getting error summary."""
    # Create mock errors
    mock_errors = [
        Mock(spec=ErrorLog, error_type="browser", created_at=datetime.utcnow()),
        Mock(spec=ErrorLog, error_type="browser", created_at=datetime.utcnow()),
        Mock(spec=ErrorLog, error_type="network", created_at=datetime.utcnow())
    ]
    dashboard_service.scraping_repo.get_errors_by_job.return_value = mock_errors
    
    # Get error summary
    summary = dashboard_service.get_error_summary(days=7)
    
    # Verify results
    assert summary["total_errors"] == 3
    assert summary["error_types"]["browser"] == 2
    assert summary["error_types"]["network"] == 1
    assert len(summary["recent_errors"]) <= 10

def test_get_performance_metrics(dashboard_service, mock_db):
    """Test getting performance metrics."""
    # Create mock jobs
    now = datetime.utcnow()
    mock_jobs = [
        {
            "status": "completed",
            "articles_scraped": 10,
            "start_time": now - timedelta(hours=1),
            "end_time": now
        },
        {
            "status": "failed",
            "articles_scraped": 0,
            "start_time": now - timedelta(hours=2),
            "end_time": now - timedelta(hours=1)
        }
    ]
    dashboard_service.scraping_repo.get_recent_jobs.return_value = mock_jobs
    
    # Get performance metrics
    metrics = dashboard_service.get_performance_metrics(days=7)
    
    # Verify results
    assert metrics["total_jobs"] == 2
    assert metrics["success_rate"] == 50.0
    assert metrics["failure_rate"] == 50.0
    assert metrics["avg_articles_per_job"] == 5.0
    assert metrics["avg_job_duration"] > 0 