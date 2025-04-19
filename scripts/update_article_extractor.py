#!/usr/bin/env python3
"""
Script to update the article_extractor.py file with datetime handling fixes.
"""

import sys
import re
import os

# Add the project root to the Python path
sys.path.append(".")

def update_article_extractor():
    """Update the article_extractor.py file with datetime handling fixes."""
    # Path to the article_extractor.py file
    file_path = "src/web_scraper/article_extractor.py"
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
    
    # Add the import for datetime_utils
    import_pattern = r"from urllib\.parse import urlparse, urljoin"
    import_replacement = "from urllib.parse import urlparse, urljoin\nfrom src.utility_modules.datetime_utils import parse_datetime, convert_to_db_datetime"
    content = re.sub(import_pattern, import_replacement, content)
    
    # Update the published_at handling in the main extraction method
    published_at_pattern = r"# Get published date from extraction strategy or fallback to meta tag\s+published_at = extracted_data\.get\(\"published_date\"\)\s+if not published_at:\s+date_match = re\.search\(r'<meta\\\\s\+property=\[\"\\\\\'\]article:published_time\[\"\\\\\'\]\(\\\\s\+content=\|>\)\[\"\\\\\'\]\(.*?\)\[\"\\\\\'\]\(/\?>\|\\\\s\)', result\.html, re\.IGNORECASE \| re\.DOTALL\)\s+published_at = date_match\.group\(2\) if date_match else datetime\.now\(timezone\.utc\)\.isoformat\(\)"
    published_at_replacement = """# Get published date from extraction strategy or fallback to meta tag
                published_at = extracted_data.get("published_date")
                if not published_at:
                    date_match = re.search(r'<meta\\\\s+property=[\\"\\']article:published_time[\\"\\']\\\\s+content=[\\"\\'](.+?)[\\"\\']', result.html, re.IGNORECASE | re.DOTALL)
                    published_at = date_match.group(1) if date_match else None
                
                # Parse the published_at date to ensure it's in ISO format
                published_at = parse_datetime(published_at)"""
    content = re.sub(published_at_pattern, published_at_replacement, content)
    
    # Update the published_at handling in the fallback method
    fallback_pattern = r"\"published_at\": datetime\.now\(timezone\.utc\)\.isoformat\(\),"
    fallback_replacement = "\"published_at\": parse_datetime(None),"
    content = re.sub(fallback_pattern, fallback_replacement, content)
    
    # Update the published_at handling in the metadata extraction method
    metadata_pattern = r"\"published_at\": result\.metadata\.get\(\"published_date\", datetime\.now\(timezone\.utc\)\.isoformat\(\)\),"
    metadata_replacement = "\"published_at\": parse_datetime(result.metadata.get(\"published_date\")),"
    content = re.sub(metadata_pattern, metadata_replacement, content)
    
    # Update the published_at handling in the fallback metadata extraction
    fallback_metadata_pattern = r"date_match = re\.search\(r'<meta\\\\s\+property=\[\"\\\\\'\]article:published_time\[\"\\\\\'\]\(\\\\s\+content=\|>\)\[\"\\\\\'\]\(.*?\)\[\"\\\\\'\]\(/\?>\|\\\\s\)', result\.html, re\.IGNORECASE \| re\.DOTALL\)\s+published_at = date_match\.group\(2\) if date_match else datetime\.now\(timezone\.utc\)\.isoformat\(\)"
    fallback_metadata_replacement = """date_match = re.search(r'<meta\\\\s+property=[\\"\\']article:published_time[\\"\\']\\\\s+content=[\\"\\'](.+?)[\\"\\']', result.html, re.IGNORECASE | re.DOTALL)
                published_at = parse_datetime(date_match.group(1) if date_match else None)"""
    content = re.sub(fallback_metadata_pattern, fallback_metadata_replacement, content)
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"Updated {file_path} with datetime handling fixes")

if __name__ == "__main__":
    update_article_extractor()
