#!/usr/bin/env python3
"""
MCP Server Time - A simple MCP server for providing time information.
This module can be used with the MCP configuration to provide current time
and date information to AI assistants.
"""

import argparse
import datetime
import json
import sys
from typing import Dict, Any, Optional

def get_current_time(timezone: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the current time, optionally in a specific timezone.
    
    Args:
        timezone: Optional IANA timezone name (e.g., 'America/New_York')
                 If None, uses the system timezone.
    
    Returns:
        Dictionary with timezone, datetime, and is_dst information
    """
    now = datetime.datetime.now()
    
    # Try to use the specified timezone if provided
    if timezone:
        try:
            import pytz
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
        except (ImportError, Exception) as e:
            print(f"Warning: Could not use timezone {timezone}: {e}", file=sys.stderr)
    
    # Format the response
    response = {
        "timezone": timezone or "System Timezone",
        "datetime": now.isoformat(),
        "is_dst": False  # We can't easily determine DST without pytz
    }
    
    return response

def convert_time(source_timezone: str, time_str: str, target_timezone: str) -> Dict[str, Any]:
    """
    Convert time between timezones.
    
    Args:
        source_timezone: Source IANA timezone name
        time_str: Time in 24-hour format (HH:MM)
        target_timezone: Target IANA timezone name
    
    Returns:
        Dictionary with source and target time information
    """
    try:
        import pytz
        
        # Parse the time string
        hour, minute = map(int, time_str.split(':'))
        
        # Use today's date with the specified time
        today = datetime.datetime.now().date()
        source_time = datetime.datetime.combine(today, datetime.time(hour, minute))
        
        # Apply source timezone
        source_tz = pytz.timezone(source_timezone)
        source_time = source_tz.localize(source_time)
        
        # Convert to target timezone
        target_tz = pytz.timezone(target_timezone)
        target_time = source_time.astimezone(target_tz)
        
        # Calculate time difference
        time_diff_hours = (target_time.utcoffset() - source_time.utcoffset()).total_seconds() / 3600
        time_diff_str = f"{'+' if time_diff_hours >= 0 else ''}{time_diff_hours}h"
        
        # Format the response
        response = {
            "source": {
                "timezone": source_timezone,
                "datetime": source_time.isoformat(),
                "is_dst": source_time.dst() != datetime.timedelta(0)
            },
            "target": {
                "timezone": target_timezone,
                "datetime": target_time.isoformat(),
                "is_dst": target_time.dst() != datetime.timedelta(0)
            },
            "time_difference": time_diff_str
        }
        
        return response
        
    except ImportError:
        print("Warning: pytz not installed, cannot convert timezones", file=sys.stderr)
        return {"error": "pytz not installed"}
    except Exception as e:
        print(f"Error converting time: {e}", file=sys.stderr)
        return {"error": str(e)}

def handle_request(request_json: str) -> Dict[str, Any]:
    """
    Handle an MCP request.
    
    Args:
        request_json: JSON string containing the request
        
    Returns:
        Response dictionary
    """
    try:
        request = json.loads(request_json)
        name = request.get("name")
        arguments = request.get("arguments", {})
        
        if name == "get_current_time":
            timezone = arguments.get("timezone")
            return get_current_time(timezone)
        elif name == "convert_time":
            source_timezone = arguments.get("source_timezone")
            time_str = arguments.get("time")
            target_timezone = arguments.get("target_timezone")
            return convert_time(source_timezone, time_str, target_timezone)
        else:
            return {"error": f"Unknown function: {name}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}
    except Exception as e:
        return {"error": str(e)}

def main():
    """Main function to run the MCP server."""
    parser = argparse.ArgumentParser(description="MCP Server for time and timezone conversion")
    parser.add_argument("--local-timezone", type=str, help="Override system timezone")
    args = parser.parse_args()
    
    # Print server information
    print("MCP Server Time - Running", file=sys.stderr)
    print("Available functions:", file=sys.stderr)
    print("  - get_current_time: Get current time in a timezone", file=sys.stderr)
    print("  - convert_time: Convert time between timezones", file=sys.stderr)
    
    # Simple request-response loop
    try:
        while True:
            request = input()
            if not request:
                continue
                
            response = handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("MCP Server Time - Shutting down", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
