#!/usr/bin/env python3
"""
Script to fix the article_service.py file to properly handle categories.

This script:
1. Updates the extract_and_store_article method to properly handle categories
2. Ensures categories are extracted from article_metadata
"""

import sys
import logging
import re

# Add the project root to the Python path
sys.path.append(".")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def fix_article_service():
    """Fix the article_service.py file to properly handle categories."""
    file_path = "src/service_layer/article_service.py"
    
    logger.info(f"Fixing {file_path}")
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
    
    # Check if the file already has the fix
    if "categories = article_data.get(\"article_metadata\", {}).get(\"categories\", [])" in content:
        logger.info(f"File {file_path} already has the fix")
        return
    
    # Update the categories extraction
    old_pattern = r"# Add categories if available\s+categories = article_data\.get\(\"categories\", \[\]\)"
    new_pattern = """# Add categories if available
            categories = article_data.get("article_metadata", {}).get("categories", [])
            category_urls = article_data.get("article_metadata", {}).get("category_urls", [])
            
            # If no categories in article_metadata, check top-level (for backward compatibility)
            if not categories:
                categories = article_data.get("categories", [])
                category_urls = article_data.get("category_urls", [])"""
    
    content = re.sub(old_pattern, new_pattern, content)
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {file_path}")

def fix_article_extractor():
    """Fix the article_extractor.py file to properly handle categories."""
    file_path = "src/web_scraper/article_extractor.py"
    
    logger.info(f"Fixing {file_path}")
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
    
    # Check if the file already has the fix
    if "# Categorize the article if no categories were extracted" in content:
        logger.info(f"File {file_path} already has the fix")
        return
    
    # Update the article data creation
    old_pattern = r"# Create article data\s+article_data = \{\s+\"title\": title,\s+\"url\": url,\s+\"content\": content_markdown,\s+\"content_markdown\": content_markdown,\s+\"content_html\": content_html,\s+\"author\": author,\s+\"published_at\": published_at,\s+\"image_url\": image_url,\s+\"website_id\": website_id,\s+\"article_metadata\": \{\s+\"word_count\": word_count,\s+\"reading_time\": reading_time,\s+\"categories\": categories,\s+\"tags\": tags,\s+\"schema\": \{\},\s+\"extraction_method\": \"strategy\" if extracted_data else \"fallback\"\s+\},\s+\"active\": True,\s+\}"
    new_pattern = """# Create article data
                article_data = {
                    "title": title,
                    "url": url,
                    "content": content_markdown,  # Use markdown for content
                    "content_markdown": content_markdown,
                    "content_html": content_html,
                    "author": author,
                    "published_at": published_at,
                    "image_url": image_url,
                    "website_id": website_id,
                    "article_metadata": {
                        "word_count": word_count,
                        "reading_time": reading_time,
                        "categories": categories,
                        "tags": tags,
                        "schema": {},
                        "extraction_method": "strategy" if extracted_data else "fallback"
                    },
                    "active": True,
                }
                
                # Get website base URL for category URL generation
                website_base_url = url
                # Extract domain from URL
                parsed_url = urlparse(url)
                website_base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                
                # Categorize the article if no categories were extracted
                if not categories:
                    article_data = categorize_article(article_data, website_base_url)"""
    
    content = re.sub(old_pattern, new_pattern, content)
    
    # Add import for categorize_article if not already present
    if "from src.web_scraper.category_extractor import categorize_article" not in content:
        import_pattern = r"from src\.web_scraper\.category_extractor import extract_categories_from_html, extract_tags_from_html"
        import_replacement = "from src.web_scraper.category_extractor import extract_categories_from_html, extract_tags_from_html, categorize_article"
        content = re.sub(import_pattern, import_replacement, content)
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {file_path}")

def main():
    """Main function to fix the article service and extractor."""
    logger.info("Starting to fix article service and extractor")
    
    # Fix article_service.py
    fix_article_service()
    
    # Fix article_extractor.py
    fix_article_extractor()
    
    logger.info("Successfully fixed article service and extractor")

if __name__ == "__main__":
    main()
