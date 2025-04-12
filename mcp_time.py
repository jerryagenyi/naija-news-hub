#!/usr/bin/env python3
"""
MCP Time module for the Naija News Hub project.
This module provides functions to get the current time and date,
which can be used throughout the project to ensure consistent time references.
"""

import datetime
import subprocess
import json
import os
import sys
from typing import Dict, Any, Optional, Union

def get_current_time(timezone: Optional[str] = None) -> str:
    """
    Get the current time in ISO format.
    
    Args:
        timezone: Optional timezone name
        
    Returns:
        Current time in ISO format
    """
    return datetime.datetime.now().isoformat()

def get_current_date(format_str: str = '%Y-%m-%d') -> str:
    """
    Get the current date in the specified format.
    
    Args:
        format_str: Format string for datetime.strftime
        
    Returns:
        Formatted date string
    """
    return datetime.datetime.now().strftime(format_str)

def get_current_year() -> int:
    """
    Get the current year.
    
    Returns:
        Current year as an integer
    """
    return datetime.datetime.now().year

def get_current_month() -> int:
    """
    Get the current month.
    
    Returns:
        Current month as an integer (1-12)
    """
    return datetime.datetime.now().month

def get_current_day() -> int:
    """
    Get the current day of the month.
    
    Returns:
        Current day as an integer
    """
    return datetime.datetime.now().day

def get_formatted_timestamp(format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Get a formatted timestamp.
    
    Args:
        format_str: Format string for datetime.strftime
        
    Returns:
        Formatted timestamp string
    """
    return datetime.datetime.now().strftime(format_str)

def get_time_info() -> Dict[str, Any]:
    """
    Get comprehensive time information.
    
    Returns:
        Dictionary with various time-related information
    """
    now = datetime.datetime.now()
    return {
        'iso_datetime': now.isoformat(),
        'year': now.year,
        'month': now.month,
        'month_name': now.strftime('%B'),
        'day': now.day,
        'weekday': now.strftime('%A'),
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'microsecond': now.microsecond,
        'timestamp': now.timestamp(),
        'formatted_date': now.strftime('%Y-%m-%d'),
        'formatted_time': now.strftime('%H:%M:%S'),
        'formatted_datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
    }

# For testing
if __name__ == "__main__":
    print(f"Current Time: {get_current_time()}")
    print(f"Current Date: {get_current_date()}")
    print(f"Current Year: {get_current_year()}")
    print(f"Current Month: {get_current_month()}")
    print(f"Current Day: {get_current_day()}")
    print(f"Formatted Timestamp: {get_formatted_timestamp()}")
    print("\nTime Info:")
    time_info = get_time_info()
    for key, value in time_info.items():
        print(f"  {key}: {value}")
