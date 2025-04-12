"""
Tests for the error handling system.

This module provides tests for error handling functionality.
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Error as PlaywrightError
from sqlalchemy.exc import SQLAlchemyError

from src.utility_modules.error_handling import (
    ScrapingError,
    ScrapingErrorHandler,
    BrowserErrorHandler
)
from src.utility_modules.enums import ErrorType, ErrorSeverity
from src.database_management.models import ScrapingJob, ErrorLog

@pytest.fixture
def mock_db():
    """Create a mock database session."""
    with patch('src.utils.error_handling.get_db') as mock:
        db_session = MagicMock()
        mock.return_value.__enter__.return_value = db_session
        yield db_session

@pytest.fixture
def error_handler(mock_db):
    """Create an error handler instance."""
    return ScrapingErrorHandler(job_id=1)

def test_error_type_determination():
    """Test error type determination for different exceptions."""
    # Test browser errors
    timeout_error = PlaywrightTimeoutError("timeout")
    assert ScrapingErrorHandler.determine_error_type(timeout_error) == ErrorType.BROWSER

    playwright_error = PlaywrightError("browser error")
    assert ScrapingErrorHandler.determine_error_type(playwright_error) == ErrorType.BROWSER

    # Test database errors
    db_error = SQLAlchemyError("database error")
    assert ScrapingErrorHandler.determine_error_type(db_error) == ErrorType.DATABASE

    # Test custom scraping error
    scraping_error = ScrapingError("content error", ErrorType.CONTENT)
    assert ScrapingErrorHandler.determine_error_type(scraping_error) == ErrorType.CONTENT

    # Test unknown error
    unknown_error = Exception("unknown error")
    assert ScrapingErrorHandler.determine_error_type(unknown_error) == ErrorType.UNKNOWN

def test_error_severity_determination():
    """Test error severity determination for different error types."""
    assert ScrapingErrorHandler.determine_severity(ErrorType.BROWSER) == ErrorSeverity.HIGH
    assert ScrapingErrorHandler.determine_severity(ErrorType.DATABASE) == ErrorSeverity.CRITICAL
    assert ScrapingErrorHandler.determine_severity(ErrorType.RATE_LIMIT) == ErrorSeverity.MEDIUM
    assert ScrapingErrorHandler.determine_severity(ErrorType.AUTHENTICATION) == ErrorSeverity.HIGH
    assert ScrapingErrorHandler.determine_severity(ErrorType.VALIDATION) == ErrorSeverity.LOW
    assert ScrapingErrorHandler.determine_severity(ErrorType.NETWORK) == ErrorSeverity.MEDIUM
    assert ScrapingErrorHandler.determine_severity(ErrorType.CONTENT) == ErrorSeverity.LOW
    assert ScrapingErrorHandler.determine_severity(ErrorType.UNKNOWN) == ErrorSeverity.HIGH

def test_recovery_actions(error_handler):
    """Test recovery actions generation."""
    # Test browser error recovery actions
    actions = error_handler._get_recovery_actions(ErrorType.BROWSER_ERROR, ErrorSeverity.HIGH)
    assert "Retry with increased timeout" in actions
    assert "Check browser configuration" in actions
    assert "Verify page load conditions" in actions
    assert "Review and resolve before next run" in actions
    
    # Test network error recovery actions
    actions = error_handler._get_recovery_actions(ErrorType.NETWORK_ERROR, ErrorSeverity.MEDIUM)
    assert "Retry with exponential backoff" in actions
    assert "Check network connectivity" in actions
    assert "Verify proxy settings if used" in actions
    
    # Test database error recovery actions
    actions = error_handler._get_recovery_actions(ErrorType.DATABASE_ERROR, ErrorSeverity.CRITICAL)
    assert "Check database connection" in actions
    assert "Verify database schema" in actions
    assert "Review transaction handling" in actions
    assert "Requires immediate attention" in actions

def test_error_handling(mock_db):
    """Test error handling and logging."""
    # Create a mock job
    job = MagicMock(spec=ScrapingJob)
    job.id = 1
    job.status = "running"
    job.error_count = 0

    error = PlaywrightTimeoutError("timeout")
    url = "https://example.com"
    context = {"page": "home"}

    # Handle the error
    ScrapingErrorHandler.handle_error(error, job, url, context)

    # Verify error log was created
    mock_db.add.assert_called()
    calls = mock_db.add.call_args_list
    error_log = None
    for call in calls:
        args = call[0]
        if isinstance(args[0], ErrorLog):
            error_log = args[0]
            break
    
    assert error_log is not None
    assert error_log.error_type == ErrorType.BROWSER
    assert error_log.severity == ErrorSeverity.HIGH
    assert error_log.url == url
    assert error_log.context == str(context)
    assert error_log.recovery_actions is not None

    # Verify job was updated
    assert job.error_count == 1
    mock_db.commit.assert_called()

def test_critical_error_handling(mock_db):
    """Test handling of critical errors."""
    job = MagicMock(spec=ScrapingJob)
    job.id = 1
    job.status = "running"
    job.error_count = 0

    error = SQLAlchemyError("database error")

    ScrapingErrorHandler.handle_error(error, job)

    assert job.status == "failed"
    assert job.end_time is not None
    assert job.error_count == 1
    mock_db.commit.assert_called()

def test_browser_error_recovery_actions():
    """Test recovery action generation for browser errors."""
    # Test timeout error
    timeout_error = PlaywrightTimeoutError("timeout")
    actions = BrowserErrorHandler.get_recovery_actions(timeout_error)
    assert "timeout value" in actions
    assert "retry mechanism" in actions

    # Test general browser error
    browser_error = PlaywrightError("browser error")
    actions = BrowserErrorHandler.get_recovery_actions(browser_error)
    assert "browser instance" in actions
    assert "network connectivity" in actions

    # Test unknown error
    unknown_error = Exception("unknown error")
    actions = BrowserErrorHandler.get_recovery_actions(unknown_error)
    assert "No specific recovery actions" in actions

def test_error_summary(mock_db):
    """Test error summary generation."""
    # Create mock error logs
    error_logs = [
        MagicMock(
            spec=ErrorLog,
            job_id=1,
            error_type=ErrorType.BROWSER,
            severity=ErrorSeverity.HIGH,
            error_message="timeout",
            created_at=datetime.utcnow(),
            resolved_at=None
        ),
        MagicMock(
            spec=ErrorLog,
            job_id=1,
            error_type=ErrorType.DATABASE,
            severity=ErrorSeverity.CRITICAL,
            error_message="connection error",
            created_at=datetime.utcnow(),
            resolved_at=None
        ),
        MagicMock(
            spec=ErrorLog,
            job_id=1,
            error_type=ErrorType.CONTENT,
            severity=ErrorSeverity.LOW,
            error_message="missing field",
            created_at=datetime.utcnow(),
            resolved_at=datetime.utcnow()
        )
    ]

    # Mock database query
    mock_db.query.return_value.filter.return_value.all.return_value = error_logs

    # Get summary
    summary = ScrapingErrorHandler.get_error_summary(1)

    assert summary["total_errors"] == 3
    assert summary["by_type"]["browser"] == 1
    assert summary["by_type"]["database"] == 1
    assert summary["by_type"]["content"] == 1
    assert summary["by_severity"]["high"] == 1
    assert summary["by_severity"]["critical"] == 1
    assert summary["by_severity"]["low"] == 1
    assert summary["unresolved_critical"] == 1

def test_browser_error_handler():
    """Test browser error handler."""
    # Test timeout error handling
    error_info = BrowserErrorHandler.handle_browser_error(PlaywrightTimeoutError())
    assert error_info["error_type"] == "browser_error"
    assert "Retry with increased timeout" in error_info["recovery_actions"]
    assert "Check network connectivity" in error_info["recovery_actions"]
    assert "Verify page load conditions" in error_info["recovery_actions"]
    
    # Test generic browser error handling
    error_info = BrowserErrorHandler.handle_browser_error(Exception("Browser error"))
    assert error_info["error_type"] == "browser_error"
    assert "Check browser configuration" in error_info["recovery_actions"]
    assert "Verify page load conditions" in error_info["recovery_actions"]
    assert "Review error logs for patterns" in error_info["recovery_actions"] 