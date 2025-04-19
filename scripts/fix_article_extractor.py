#!/usr/bin/env python3
"""
Script to fix the article_extractor.py file to use parse_datetime for the published_at field.
"""

import re

def fix_article_extractor():
    """Fix the article_extractor.py file to use parse_datetime for the published_at field."""
    # Path to the article_extractor.py file
    file_path = "src/web_scraper/article_extractor.py"
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
    
    # Fix the published_at field in the main extraction method
    pattern1 = r"# Get published date from extraction strategy or fallback to meta tag\s+published_at = extracted_data\.get\(\"published_date\"\)\s+if not published_at:\s+date_match = re\.search\(r'<meta\\\\s\+property=\[\"\\\\'\]article:published_time\[\"\\\\'\]\(\\\\s\+content=\|>\)\[\"\\\\'\]\(\.\*\)\[\"\\\\'\]\(/\?>\|\\\\s\)', result\.html, re\.IGNORECASE \| re\.DOTALL\)\s+published_at = date_match\.group\(2\) if date_match else datetime\.now\(timezone\.utc\)\.isoformat\(\)"
    replacement1 = """# Get published date from extraction strategy or fallback to meta tag
                published_at = extracted_data.get("published_date")
                if not published_at:
                    date_match = re.search(r'<meta\\\\s+property=[\\"\\']article:published_time[\\"\\']\\\\s+content=[\\"\\'](.+?)[\\"\\']', result.html, re.IGNORECASE | re.DOTALL)
                    published_at = date_match.group(1) if date_match else None
                
                # Parse the published_at date to ensure it's in ISO format
                published_at = parse_datetime(published_at)"""
    
    content = re.sub(pattern1, replacement1, content)
    
    # Fix the published_at field in the metadata extraction method
    pattern2 = r"# Try to extract publication date\s+date_match = re\.search\(r'<meta\\\\s\+property=\[\"\\\\'\]article:published_time\[\"\\\\'\]\(\\\\s\+content=\|>\)\[\"\\\\'\]\(\.\*\?\)\[\"\\\\'\]\(/\?>\|\\\\s\)', result\.html, re\.IGNORECASE \| re\.DOTALL\)\s+published_at = date_match\.group\(2\) if date_match else datetime\.now\(timezone\.utc\)\.isoformat\(\)"
    replacement2 = """# Try to extract publication date
                date_match = re.search(r'<meta\\\\s+property=[\\"\\']article:published_time[\\"\\']\\\\s+content=[\\"\\'](.+?)[\\"\\']', result.html, re.IGNORECASE | re.DOTALL)
                published_at = parse_datetime(date_match.group(1) if date_match else None)"""
    
    content = re.sub(pattern2, replacement2, content)
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"Fixed {file_path} to use parse_datetime for the published_at field")

if __name__ == "__main__":
    fix_article_extractor()
