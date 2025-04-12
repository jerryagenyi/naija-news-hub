#!/usr/bin/env python3
"""
Example script demonstrating how to use the MCP time utility.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.mcp.time import (
    get_current_time,
    get_current_date,
    get_current_year,
    get_current_month,
    get_current_day,
    get_time_info
)

def main():
    """Demonstrate the MCP time utility functions."""
    print("Naija News Hub - MCP Time Utility Example")
    print("=========================================")
    
    print(f"\nCurrent Date: {get_current_date()}")
    print(f"Current Time: {get_current_time('%H:%M:%S')}")
    print(f"Current Year: {get_current_year()}")
    print(f"Current Month: {get_current_month()}")
    print(f"Current Day: {get_current_day()}")
    
    print("\nFormatting Examples:")
    print(f"  ISO Format: {get_current_time()}")
    print(f"  Custom Format: {get_current_time('%Y-%m-%d %H:%M:%S')}")
    print(f"  Date Only: {get_current_date()}")
    print(f"  Custom Date: {get_current_date('%B %d, %Y')}")
    
    print("\nComplete Time Information:")
    time_info = get_time_info()
    for key, value in time_info.items():
        print(f"  {key}: {value}")
    
    print("\nUsage in Documentation:")
    print("  When updating documentation, use:")
    print("  from utils.mcp.time import get_current_date")
    print("  last_updated = get_current_date()")
    print(f"  # Result: {get_current_date()}")

if __name__ == "__main__":
    main()
