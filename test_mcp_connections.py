#!/usr/bin/env python3
"""
Test script to check MCP server connections to Brave Search and Context7.
"""

import json
import requests
import sys
from typing import Dict, Any, List, Optional

def test_mcp_connection(server_name: str, url: str) -> Dict[str, Any]:
    """
    Test connection to an MCP server.
    
    Args:
        server_name: Name of the MCP server
        url: URL of the MCP server
        
    Returns:
        Dictionary with test results
    """
    print(f"Testing connection to {server_name} MCP server at {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        status_code = response.status_code
        
        if status_code == 200:
            print(f"✅ Connection to {server_name} successful (Status code: {status_code})")
            return {
                "server": server_name,
                "url": url,
                "status": "success",
                "status_code": status_code,
                "response": response.text[:100] + "..." if len(response.text) > 100 else response.text
            }
        else:
            print(f"❌ Connection to {server_name} failed (Status code: {status_code})")
            return {
                "server": server_name,
                "url": url,
                "status": "failed",
                "status_code": status_code,
                "error": f"HTTP Error: {status_code}"
            }
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection to {server_name} failed: {str(e)}")
        return {
            "server": server_name,
            "url": url,
            "status": "failed",
            "error": str(e)
        }

def main():
    """Main function to test MCP server connections."""
    # Define MCP servers to test
    mcp_servers = [
        {
            "name": "Brave Search",
            "url": "https://mcp.so/server/brave-search/modelcontextprotocol"
        },
        {
            "name": "Context7",
            "url": "https://mcp.so/server/context7/modelcontextprotocol"
        }
    ]
    
    # Test connections
    results = []
    for server in mcp_servers:
        result = test_mcp_connection(server["name"], server["url"])
        results.append(result)
    
    # Print summary
    print("\nSummary:")
    for result in results:
        status = "✅ Connected" if result.get("status") == "success" else "❌ Failed"
        print(f"{status} - {result['server']}")
    
    # Return success if all connections are successful
    return all(result.get("status") == "success" for result in results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
