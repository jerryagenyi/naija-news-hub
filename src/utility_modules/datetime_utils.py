"""
Datetime utility functions for Naija News Hub.

This module provides functions to handle datetime conversion and formatting.
"""

import logging
import re
from datetime import datetime, timezone
from typing import Optional, Union, Any

# Configure logging
logger = logging.getLogger(__name__)

def parse_datetime(date_value: Any) -> Optional[Union[str, datetime]]:
    """
    Parse a datetime value from various formats and return an ISO-formatted string.
    
    Args:
        date_value: The datetime value to parse (string, datetime, or None)
        
    Returns:
        ISO-formatted datetime string or None if parsing fails
    """
    if not date_value:
        return datetime.now(timezone.utc).isoformat()
        
    # If it's already a datetime object
    if isinstance(date_value, datetime):
        # Ensure it has timezone info
        if date_value.tzinfo is None:
            date_value = date_value.replace(tzinfo=timezone.utc)
        return date_value.isoformat()
        
    # If it's a string, try to parse it
    if isinstance(date_value, str):
        # Try ISO format first
        try:
            # Handle 'Z' timezone designator
            if date_value.endswith('Z'):
                date_value = date_value.replace('Z', '+00:00')
                
            dt = datetime.fromisoformat(date_value)
            # Ensure it has timezone info
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except ValueError:
            pass
            
        # Try common date formats
        formats = [
            "%Y-%m-%d", 
            "%Y/%m/%d", 
            "%d-%m-%Y", 
            "%d/%m/%Y", 
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S"
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_value, fmt)
                # Add UTC timezone
                dt = dt.replace(tzinfo=timezone.utc)
                return dt.isoformat()
            except ValueError:
                continue
                
        # Try to extract date using regex
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{2}/\d{2}/\d{4})',  # DD/MM/YYYY
            r'(\d{4}/\d{2}/\d{2})',  # YYYY/MM/DD
            r'(\w+ \d{1,2}, \d{4})'  # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_value)
            if match:
                extracted_date = match.group(1)
                return parse_datetime(extracted_date)  # Recursive call with extracted date
                
        # If all parsing attempts fail, log warning and return current time
        logger.warning(f"Could not parse datetime: {date_value}, using current time instead")
        
    # Default to current time
    return datetime.now(timezone.utc).isoformat()

def convert_to_db_datetime(date_value: Any) -> datetime:
    """
    Convert a datetime value to a datetime object suitable for database storage.
    
    Args:
        date_value: The datetime value to convert (string, datetime, or None)
        
    Returns:
        datetime object with timezone info
    """
    if not date_value:
        return datetime.now(timezone.utc)
        
    # If it's already a datetime object
    if isinstance(date_value, datetime):
        # Ensure it has timezone info
        if date_value.tzinfo is None:
            return date_value.replace(tzinfo=timezone.utc)
        return date_value
        
    # If it's a string, parse it first
    if isinstance(date_value, str):
        iso_str = parse_datetime(date_value)
        if isinstance(iso_str, datetime):
            return iso_str
        try:
            # Handle 'Z' timezone designator
            if iso_str.endswith('Z'):
                iso_str = iso_str.replace('Z', '+00:00')
            return datetime.fromisoformat(iso_str)
        except (ValueError, AttributeError):
            logger.warning(f"Could not convert to datetime: {date_value}, using current time instead")
            
    # Default to current time
    return datetime.now(timezone.utc)
