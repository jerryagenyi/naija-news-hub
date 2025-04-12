"""
Error handling utilities for the scraping process.
"""
from typing import Optional, Dict, Any
from datetime import datetime
import traceback
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from sqlalchemy.exc import SQLAlchemyError

from src.utility_modules.enums import ErrorType, ErrorSeverity
from src.database_management.models import ScrapingJob, ErrorLog
from src.database_management.connection import get_db

class ScrapingError(Exception):
    """Base exception for scraping errors."""
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

class ScrapingErrorHandler:
    """Handles errors during the scraping process."""

    @staticmethod
    def determine_error_type(error: Exception) -> ErrorType:
        """Determine the type of error based on the exception."""
        if isinstance(error, PlaywrightTimeoutError):
            return ErrorType.BROWSER
        elif isinstance(error, PlaywrightError):
            return ErrorType.BROWSER
        elif isinstance(error, SQLAlchemyError):
            return ErrorType.DATABASE
        elif isinstance(error, ScrapingError):
            return error.error_type
        return ErrorType.UNKNOWN

    @staticmethod
    def determine_severity(error_type: ErrorType) -> ErrorSeverity:
        """Determine the severity of an error based on its type."""
        severity_map = {
            ErrorType.BROWSER: ErrorSeverity.HIGH,
            ErrorType.DATABASE: ErrorSeverity.CRITICAL,
            ErrorType.RATE_LIMIT: ErrorSeverity.MEDIUM,
            ErrorType.AUTHENTICATION: ErrorSeverity.HIGH,
            ErrorType.VALIDATION: ErrorSeverity.LOW,
            ErrorType.NETWORK: ErrorSeverity.MEDIUM,
            ErrorType.CONTENT: ErrorSeverity.LOW,
            ErrorType.UNKNOWN: ErrorSeverity.HIGH
        }
        return severity_map.get(error_type, ErrorSeverity.HIGH)

    @staticmethod
    def handle_error(error: Exception, job: ScrapingJob, url: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> None:
        """Handle an error by logging it and updating the job status."""
        error_type = ScrapingErrorHandler.determine_error_type(error)
        severity = ScrapingErrorHandler.determine_severity(error_type)

        # Create error log
        error_log = ErrorLog(
            job_id=job.id,
            error_type=error_type,
            severity=severity,
            error_message=str(error),
            url=url,
            context=str(context) if context else None,
            stack_trace=traceback.format_exc(),
            recovery_actions=BrowserErrorHandler.get_recovery_actions(error) if error_type == ErrorType.BROWSER else None
        )

        # Update job status based on severity
        if severity == ErrorSeverity.CRITICAL:
            job.status = "failed"
            job.end_time = datetime.utcnow()

        job.error_count += 1

        # Save to database
        with get_db() as db:
            db.add(error_log)
            db.add(job)
            db.commit()

    @staticmethod
    def get_error_summary(job_id: int) -> Dict[str, Any]:
        """Get a summary of errors for a specific job."""
        with get_db() as db:
            errors = db.query(ErrorLog).filter(ErrorLog.job_id == job_id).all()

            summary = {
                "total_errors": len(errors),
                "by_type": {},
                "by_severity": {},
                "unresolved_critical": 0
            }

            for error in errors:
                # Count by type
                error_type = error.error_type.value
                summary["by_type"][error_type] = summary["by_type"].get(error_type, 0) + 1

                # Count by severity
                severity = error.severity.value
                summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1

                # Count unresolved critical errors
                if error.severity == ErrorSeverity.CRITICAL and not error.resolved_at:
                    summary["unresolved_critical"] += 1

            return summary

class BrowserErrorHandler:
    """Handles browser-specific errors."""

    @staticmethod
    def get_recovery_actions(error: Exception) -> str:
        """Get recovery actions for browser errors."""
        if isinstance(error, PlaywrightTimeoutError):
            return (
                "1. Increase the timeout value\n"
                "2. Check if the page is loading too slowly\n"
                "3. Verify if the selector exists on the page\n"
                "4. Consider implementing a retry mechanism"
            )
        elif isinstance(error, PlaywrightError):
            return (
                "1. Check if the browser instance is still running\n"
                "2. Verify network connectivity\n"
                "3. Restart the browser instance\n"
                "4. Check for any browser console errors"
            )
        return "No specific recovery actions available for this error type."