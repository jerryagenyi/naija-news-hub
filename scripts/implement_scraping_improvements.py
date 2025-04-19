#!/usr/bin/env python3
"""
Script to implement scraping improvements for the Naija News Hub project.

This script:
1. Fixes datetime handling issues
2. Implements rate limiting and anti-ban measures
3. Enhances URL discovery
4. Updates the article extractor to use the improved components
"""

import sys
import os
import logging
import shutil
from typing import List

# Add the project root to the Python path
sys.path.append(".")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def fix_datetime_issues():
    """Fix datetime handling issues."""
    logger.info("Fixing datetime handling issues")
    
    # Run the fix_datetime_issues.py script
    from scripts.fix_datetime_issues import main as fix_datetime_main
    fix_datetime_main()
    
    logger.info("Successfully fixed datetime issues")

def implement_enhanced_scraping():
    """Implement enhanced scraping with rate limiting and anti-ban measures."""
    logger.info("Implementing enhanced scraping")
    
    # Check if the utility modules directory exists
    utility_modules_dir = "src/utility_modules"
    if not os.path.exists(utility_modules_dir):
        os.makedirs(utility_modules_dir)
        logger.info(f"Created directory: {utility_modules_dir}")
    
    # Check if the rate_limiter.py file exists
    rate_limiter_path = os.path.join(utility_modules_dir, "rate_limiter.py")
    if not os.path.exists(rate_limiter_path):
        # Copy the rate_limiter.py file from the scripts directory
        shutil.copy("src/utility_modules/rate_limiter.py", rate_limiter_path)
        logger.info(f"Created file: {rate_limiter_path}")
    
    # Check if the anti_ban.py file exists
    anti_ban_path = os.path.join(utility_modules_dir, "anti_ban.py")
    if not os.path.exists(anti_ban_path):
        # Copy the anti_ban.py file from the scripts directory
        shutil.copy("src/utility_modules/anti_ban.py", anti_ban_path)
        logger.info(f"Created file: {anti_ban_path}")
    
    logger.info("Successfully implemented enhanced scraping")

def implement_enhanced_url_discovery():
    """Implement enhanced URL discovery."""
    logger.info("Implementing enhanced URL discovery")
    
    # Check if the web_scraper directory exists
    web_scraper_dir = "src/web_scraper"
    if not os.path.exists(web_scraper_dir):
        os.makedirs(web_scraper_dir)
        logger.info(f"Created directory: {web_scraper_dir}")
    
    # Check if the category_discovery.py file exists
    category_discovery_path = os.path.join(web_scraper_dir, "category_discovery.py")
    if not os.path.exists(category_discovery_path):
        # Copy the category_discovery.py file
        shutil.copy("src/web_scraper/category_discovery.py", category_discovery_path)
        logger.info(f"Created file: {category_discovery_path}")
    
    # Check if the enhanced_url_discovery.py file exists
    enhanced_url_discovery_path = os.path.join(web_scraper_dir, "enhanced_url_discovery.py")
    if not os.path.exists(enhanced_url_discovery_path):
        # Copy the enhanced_url_discovery.py file
        shutil.copy("src/web_scraper/enhanced_url_discovery.py", enhanced_url_discovery_path)
        logger.info(f"Created file: {enhanced_url_discovery_path}")
    
    logger.info("Successfully implemented enhanced URL discovery")

def implement_enhanced_article_extractor():
    """Implement enhanced article extractor."""
    logger.info("Implementing enhanced article extractor")
    
    # Check if the web_scraper directory exists
    web_scraper_dir = "src/web_scraper"
    if not os.path.exists(web_scraper_dir):
        os.makedirs(web_scraper_dir)
        logger.info(f"Created directory: {web_scraper_dir}")
    
    # Check if the enhanced_article_extractor.py file exists
    enhanced_article_extractor_path = os.path.join(web_scraper_dir, "enhanced_article_extractor.py")
    if not os.path.exists(enhanced_article_extractor_path):
        # Copy the enhanced_article_extractor.py file
        shutil.copy("src/web_scraper/enhanced_article_extractor.py", enhanced_article_extractor_path)
        logger.info(f"Created file: {enhanced_article_extractor_path}")
    
    logger.info("Successfully implemented enhanced article extractor")

def update_requirements():
    """Update requirements.txt with new dependencies."""
    logger.info("Updating requirements.txt")
    
    # New dependencies to add
    new_dependencies = [
        "aiohttp>=3.8.0",
        "feedparser>=6.0.0",
        "crawl4ai>=0.5.0",
        "playwright>=1.30.0",
    ]
    
    # Read existing requirements
    requirements_path = "requirements.txt"
    existing_dependencies = []
    if os.path.exists(requirements_path):
        with open(requirements_path, "r") as f:
            existing_dependencies = [line.strip() for line in f.readlines()]
    
    # Add new dependencies if they don't already exist
    updated_dependencies = existing_dependencies.copy()
    for dependency in new_dependencies:
        # Check if the dependency already exists (ignoring version)
        dependency_name = dependency.split(">=")[0].split("==")[0].strip()
        if not any(dep.startswith(dependency_name) for dep in existing_dependencies):
            updated_dependencies.append(dependency)
    
    # Write updated requirements
    with open(requirements_path, "w") as f:
        for dependency in updated_dependencies:
            f.write(f"{dependency}\n")
    
    logger.info(f"Updated {requirements_path} with new dependencies")

def create_test_script():
    """Create a test script for the enhanced URL discovery and article extractor."""
    logger.info("Creating test script")
    
    # Check if the scripts directory exists
    scripts_dir = "scripts"
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
        logger.info(f"Created directory: {scripts_dir}")
    
    # Check if the test_enhanced_url_discovery.py file exists
    test_script_path = os.path.join(scripts_dir, "test_enhanced_url_discovery.py")
    if not os.path.exists(test_script_path):
        # Copy the test_enhanced_url_discovery.py file
        shutil.copy("scripts/test_enhanced_url_discovery.py", test_script_path)
        logger.info(f"Created file: {test_script_path}")
    
    # Make the test script executable
    os.chmod(test_script_path, 0o755)
    
    logger.info("Successfully created test script")

def main():
    """Main function to implement all improvements."""
    logger.info("Starting implementation of scraping improvements")
    
    # 1. Fix datetime issues
    fix_datetime_issues()
    
    # 2. Implement enhanced scraping
    implement_enhanced_scraping()
    
    # 3. Implement enhanced URL discovery
    implement_enhanced_url_discovery()
    
    # 4. Implement enhanced article extractor
    implement_enhanced_article_extractor()
    
    # 5. Update requirements.txt
    update_requirements()
    
    # 6. Create test script
    create_test_script()
    
    logger.info("Successfully implemented all scraping improvements")
    logger.info("To test the improvements, run: python scripts/test_enhanced_url_discovery.py")

if __name__ == "__main__":
    main()
