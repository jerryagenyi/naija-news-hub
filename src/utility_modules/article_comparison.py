"""
Article comparison module for Naija News Hub.

This module provides functions to compare articles and determine if an update is needed.
"""

import logging
import re
import difflib
from typing import Dict, Any, Tuple, Optional, List
from datetime import datetime, timedelta
from src.database_management.models import Article

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def should_update_article(existing_article: Article, new_data: Dict[str, Any], 
                          force_update: bool = False, 
                          min_update_interval_hours: int = 24) -> Tuple[bool, List[str]]:
    """
    Determine if an article should be updated based on comparison with new data.
    
    Args:
        existing_article: Existing article from the database
        new_data: New article data from scraping
        force_update: If True, update regardless of other conditions
        min_update_interval_hours: Minimum hours between updates
        
    Returns:
        Tuple of (should_update, reasons)
    """
    reasons = []
    
    # If force update is enabled, always update
    if force_update:
        reasons.append("Force update enabled")
        return True, reasons
    
    # Check if the article was recently updated
    if existing_article.last_checked_at:
        time_since_last_check = datetime.utcnow() - existing_article.last_checked_at
        if time_since_last_check < timedelta(hours=min_update_interval_hours):
            logger.info(f"Article {existing_article.id} was checked recently ({time_since_last_check.total_seconds() / 3600:.2f} hours ago)")
            return False, ["Article was checked recently"]
    
    # Check for significant content changes
    if has_significant_content_changes(existing_article, new_data):
        reasons.append("Significant content changes detected")
        return True, reasons
    
    # Check for metadata changes
    if has_metadata_changes(existing_article, new_data):
        reasons.append("Metadata changes detected")
        return True, reasons
    
    # Check for category changes
    if 'categories' in new_data and new_data['categories']:
        reasons.append("New categories available")
        return True, reasons
    
    # Check for image changes
    if new_data.get('image_url') and new_data.get('image_url') != existing_article.image_url:
        reasons.append("Image URL changed")
        return True, reasons
    
    # Check for author changes
    if new_data.get('author') and new_data.get('author') != existing_article.author:
        reasons.append("Author information changed")
        return True, reasons
    
    # Check for published date changes
    if new_data.get('published_at') and new_data.get('published_at') != existing_article.published_at:
        reasons.append("Published date changed")
        return True, reasons
    
    return False, ["No significant changes detected"]

def has_significant_content_changes(existing_article: Article, new_data: Dict[str, Any]) -> bool:
    """
    Check if there are significant changes in the article content.
    
    Args:
        existing_article: Existing article from the database
        new_data: New article data from scraping
        
    Returns:
        True if significant changes are detected, False otherwise
    """
    # Get content from both articles
    existing_content = existing_article.content or ""
    new_content = new_data.get('content', "")
    
    # If either content is empty, check if the other has content
    if not existing_content and new_content:
        return True
    if not new_content:
        return False
    
    # Calculate content length difference
    length_diff = abs(len(new_content) - len(existing_content))
    length_diff_percentage = length_diff / max(len(existing_content), 1) * 100
    
    # If content length changed by more than 10%, consider it significant
    if length_diff_percentage > 10:
        logger.info(f"Content length changed by {length_diff_percentage:.2f}%")
        return True
    
    # Use difflib to calculate similarity
    similarity = difflib.SequenceMatcher(None, existing_content, new_content).ratio()
    
    # If similarity is less than 0.9 (90%), consider it significant
    if similarity < 0.9:
        logger.info(f"Content similarity is {similarity:.2f}")
        return True
    
    # Check for new paragraphs
    existing_paragraphs = set(re.split(r'\n\s*\n', existing_content))
    new_paragraphs = set(re.split(r'\n\s*\n', new_content))
    
    # If there are new paragraphs, consider it significant
    if len(new_paragraphs - existing_paragraphs) > 0:
        logger.info(f"Found {len(new_paragraphs - existing_paragraphs)} new paragraphs")
        return True
    
    return False

def has_metadata_changes(existing_article: Article, new_data: Dict[str, Any]) -> bool:
    """
    Check if there are changes in the article metadata.
    
    Args:
        existing_article: Existing article from the database
        new_data: New article data from scraping
        
    Returns:
        True if metadata changes are detected, False otherwise
    """
    # Get metadata from both articles
    existing_metadata = existing_article.article_metadata or {}
    new_metadata = new_data.get('article_metadata', {})
    
    # If new metadata is empty, no changes
    if not new_metadata:
        return False
    
    # Check for new keys in metadata
    for key in new_metadata:
        if key not in existing_metadata:
            logger.info(f"New metadata key found: {key}")
            return True
        
        # Check for changes in existing keys
        if key in existing_metadata and new_metadata[key] != existing_metadata[key]:
            # Skip validation metadata as it might change on each check
            if key == 'validation':
                continue
                
            logger.info(f"Metadata value changed for key: {key}")
            return True
    
    return False

def merge_article_data(existing_article: Article, new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge existing article data with new data, preserving important existing data.
    
    Args:
        existing_article: Existing article from the database
        new_data: New article data from scraping
        
    Returns:
        Merged article data
    """
    # Start with existing article data
    merged_data = {
        'title': existing_article.title,
        'url': existing_article.url,
        'content': existing_article.content,
        'content_markdown': existing_article.content_markdown,
        'content_html': existing_article.content_html,
        'author': existing_article.author,
        'published_at': existing_article.published_at,
        'image_url': existing_article.image_url,
        'website_id': existing_article.website_id,
        'article_metadata': existing_article.article_metadata or {},
        'active': existing_article.active,
        'last_checked_at': datetime.utcnow(),
        'update_count': existing_article.update_count + 1
    }
    
    # Update with new data
    for key, value in new_data.items():
        if key == 'article_metadata' and value:
            # Merge metadata instead of replacing
            if not merged_data['article_metadata']:
                merged_data['article_metadata'] = {}
                
            for meta_key, meta_value in value.items():
                merged_data['article_metadata'][meta_key] = meta_value
        elif value:  # Only update if value is not empty
            merged_data[key] = value
    
    return merged_data

def get_article_changes_summary(existing_article: Article, new_data: Dict[str, Any]) -> str:
    """
    Get a summary of changes between existing article and new data.
    
    Args:
        existing_article: Existing article from the database
        new_data: New article data from scraping
        
    Returns:
        Summary of changes
    """
    changes = []
    
    # Check title changes
    if new_data.get('title') and new_data['title'] != existing_article.title:
        changes.append(f"Title changed: '{existing_article.title}' -> '{new_data['title']}'")
    
    # Check content length changes
    existing_content = existing_article.content or ""
    new_content = new_data.get('content', "")
    if new_content and len(new_content) != len(existing_content):
        length_diff = len(new_content) - len(existing_content)
        changes.append(f"Content length changed by {length_diff} characters ({length_diff / max(len(existing_content), 1) * 100:.2f}%)")
    
    # Check author changes
    if new_data.get('author') and new_data['author'] != existing_article.author:
        changes.append(f"Author changed: '{existing_article.author}' -> '{new_data['author']}'")
    
    # Check published date changes
    if new_data.get('published_at') and new_data['published_at'] != existing_article.published_at:
        changes.append(f"Published date changed: '{existing_article.published_at}' -> '{new_data['published_at']}'")
    
    # Check image changes
    if new_data.get('image_url') and new_data['image_url'] != existing_article.image_url:
        changes.append(f"Image URL changed: '{existing_article.image_url}' -> '{new_data['image_url']}'")
    
    # Check metadata changes
    existing_metadata = existing_article.article_metadata or {}
    new_metadata = new_data.get('article_metadata', {})
    
    if new_metadata:
        for key in new_metadata:
            if key not in existing_metadata:
                changes.append(f"New metadata key: '{key}'")
            elif key in existing_metadata and new_metadata[key] != existing_metadata[key]:
                if key != 'validation':  # Skip validation metadata
                    changes.append(f"Metadata value changed for key: '{key}'")
    
    # Check category changes
    if 'categories' in new_data and new_data['categories']:
        changes.append(f"New categories: {', '.join(new_data['categories'])}")
    
    if not changes:
        return "No significant changes detected"
    
    return "\n".join(changes)
