#!/usr/bin/env python3
"""
Script to fix datetime handling issues in the Naija News Hub project.

This script updates the article_extractor.py file to properly use the datetime_utils
functions for parsing and converting datetime values.
"""

import sys
import re
import os
import logging

# Add the project root to the Python path
sys.path.append(".")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def fix_article_extractor():
    """Fix datetime handling in article_extractor.py."""
    file_path = "src/web_scraper/article_extractor.py"
    
    logger.info(f"Fixing datetime handling in {file_path}")
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
    
    # Check if the import is already present
    if "from src.utility_modules.datetime_utils import parse_datetime, convert_to_db_datetime" not in content:
        # Add the import
        import_pattern = r"from urllib\.parse import urlparse, urljoin"
        import_replacement = "from urllib.parse import urlparse, urljoin\nfrom src.utility_modules.datetime_utils import parse_datetime, convert_to_db_datetime"
        content = re.sub(import_pattern, import_replacement, content)
        logger.info("Added datetime_utils import")
    
    # Update the published_at handling in the main extraction method
    published_at_pattern = r"# Get published date from extraction strategy or fallback to meta tag\s+published_at = extracted_data\.get\(\"published_date\"\)\s+if not published_at:\s+date_match = re\.search\(r'<meta\\s\+property=\[\"\'\]article:published_time\[\"\'\]\(\\s\+content=\|>\)\[\"\'\]\(.*?\)\[\"\'\]\(/\?>\|\\s\)', result\.html, re\.IGNORECASE \| re\.DOTALL\)\s+published_at = date_match\.group\(2\) if date_match else datetime\.now\(timezone\.utc\)\.isoformat\(\)"
    published_at_replacement = """# Get published date from extraction strategy or fallback to meta tag
                published_at = extracted_data.get("published_date")
                if not published_at:
                    date_match = re.search(r'<meta\\s+property=["\']article:published_time["\']\\s+content=["\'](.*?)["\']', result.html, re.IGNORECASE | re.DOTALL)
                    published_at = date_match.group(1) if date_match else None
                
                # Parse the published_at date to ensure it's in ISO format
                published_at = parse_datetime(published_at)"""
    
    # Try to update the pattern, but don't fail if it doesn't match
    try:
        new_content = re.sub(published_at_pattern, published_at_replacement, content)
        if new_content != content:
            content = new_content
            logger.info("Updated published_at handling in main extraction method")
        else:
            logger.warning("Could not update published_at handling in main extraction method using regex")
            # Manual fallback: replace the specific line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "published_at = date_match.group(2) if date_match else datetime.now(timezone.utc).isoformat()" in line:
                    lines[i] = "                    published_at = date_match.group(2) if date_match else None"
                    # Add the parse_datetime line after this line
                    lines.insert(i + 1, "                # Parse the published_at date to ensure it's in ISO format")
                    lines.insert(i + 2, "                published_at = parse_datetime(published_at)")
                    content = '\n'.join(lines)
                    logger.info("Updated published_at handling using line-by-line replacement")
                    break
    except Exception as e:
        logger.error(f"Error updating published_at handling: {str(e)}")
    
    # Update the published_at handling in the fallback method
    fallback_pattern = r"\"published_at\": datetime\.now\(timezone\.utc\)\.isoformat\(\),"
    fallback_replacement = "\"published_at\": parse_datetime(None),"
    content = re.sub(fallback_pattern, fallback_replacement, content)
    logger.info("Updated published_at handling in fallback method")
    
    # Update the published_at handling in the metadata extraction method
    try:
        metadata_pattern = r"# Try to extract publication date\s+date_match = re\.search\(r'<meta\\s\+property=\[\"\'\]article:published_time\[\"\'\]\(\\s\+content=\|>\)\[\"\'\]\(.*?\)\[\"\'\]\(/\?>\|\\s\)', result\.html, re\.IGNORECASE \| re\.DOTALL\)\s+published_at = date_match\.group\(2\) if date_match else datetime\.now\(timezone\.utc\)\.isoformat\(\)"
        metadata_replacement = """# Try to extract publication date
                date_match = re.search(r'<meta\\s+property=["\']article:published_time["\']\\s+content=["\'](.*?)["\']', result.html, re.IGNORECASE | re.DOTALL)
                published_at = parse_datetime(date_match.group(1) if date_match else None)"""
        
        new_content = re.sub(metadata_pattern, metadata_replacement, content)
        if new_content != content:
            content = new_content
            logger.info("Updated published_at handling in metadata extraction method")
        else:
            logger.warning("Could not update published_at handling in metadata extraction method using regex")
            # Manual fallback: replace the specific line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "published_at = date_match.group(2) if date_match else datetime.now(timezone.utc).isoformat()" in line:
                    lines[i] = "                published_at = parse_datetime(date_match.group(1) if date_match else None)"
                    content = '\n'.join(lines)
                    logger.info("Updated metadata published_at handling using line-by-line replacement")
                    break
    except Exception as e:
        logger.error(f"Error updating metadata published_at handling: {str(e)}")
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {file_path}")

def fix_content_validation():
    """Fix datetime handling in content_validation.py."""
    file_path = "src/utility_modules/content_validation.py"
    
    logger.info(f"Fixing datetime handling in {file_path}")
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
    
    # Update the _validate_published_date method
    validate_pattern = r"# Check if date is in the future\s+if published_date > datetime\.utcnow\(\):"
    validate_replacement = "# Check if date is in the future\n        now = datetime.now(timezone.utc)\n        if published_date > now:"
    content = re.sub(validate_pattern, validate_replacement, content)
    
    # Update the max_age calculation
    max_age_pattern = r"# Check if date is too old\s+max_age = datetime\.utcnow\(\) - timedelta\(days=self\.max_recent_date_days\)"
    max_age_replacement = "# Check if date is too old\n        max_age = now - timedelta(days=self.max_recent_date_days)"
    content = re.sub(max_age_pattern, max_age_replacement, content)
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {file_path}")

def fix_article_service():
    """Fix datetime handling in article_service.py."""
    file_path = "src/service_layer/article_service.py"
    
    logger.info(f"Fixing datetime handling in {file_path}")
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
    
    # Check if the import is already present
    if "from src.utility_modules.datetime_utils import convert_to_db_datetime" not in content:
        # Add the import
        import_pattern = r"from datetime import datetime"
        import_replacement = "from datetime import datetime\nfrom src.utility_modules.datetime_utils import convert_to_db_datetime"
        content = re.sub(import_pattern, import_replacement, content)
        logger.info("Added datetime_utils import")
    
    # Update all datetime.utcnow() calls to use convert_to_db_datetime(None)
    content = re.sub(r"datetime\.utcnow\(\)", "convert_to_db_datetime(None)", content)
    logger.info("Updated datetime.utcnow() calls")
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {file_path}")

def fix_database_models():
    """Fix datetime handling in database models."""
    file_path = "src/database_management/models.py"
    
    logger.info(f"Fixing datetime handling in {file_path}")
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
    
    # Add timezone import
    if "from datetime import datetime, timezone" not in content:
        # Update the import
        import_pattern = r"from datetime import datetime"
        import_replacement = "from datetime import datetime, timezone"
        content = re.sub(import_pattern, import_replacement, content)
        logger.info("Added timezone import")
    
    # Update all datetime.utcnow calls to use timezone
    content = re.sub(r"datetime\.utcnow", "datetime.now(timezone.utc)", content)
    logger.info("Updated datetime.utcnow calls to use timezone")
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {file_path}")

def main():
    """Main function to fix datetime issues."""
    logger.info("Starting to fix datetime issues")
    
    # Fix article_extractor.py
    fix_article_extractor()
    
    # Fix content_validation.py
    fix_content_validation()
    
    # Fix article_service.py
    fix_article_service()
    
    # Fix database models
    fix_database_models()
    
    logger.info("Successfully fixed datetime issues")

if __name__ == "__main__":
    main()
