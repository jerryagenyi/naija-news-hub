"""
Enums used throughout the application.
"""
from enum import Enum

class ErrorType(Enum):
    """Types of errors that can occur during scraping."""
    BROWSER = "browser"
    DATABASE = "database"
    RATE_LIMIT = "rate_limit"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    NETWORK = "network"
    CONTENT = "content"
    UNKNOWN = "unknown"

class ErrorSeverity(Enum):
    """Severity levels for errors."""
    CRITICAL = "critical"  # Requires immediate attention, stops the process
    HIGH = "high"         # Serious issue but process can continue
    MEDIUM = "medium"     # Notable issue that should be investigated
    LOW = "low"          # Minor issue that doesn't affect core functionality
    INFO = "info"        # Informational message about potential issues 