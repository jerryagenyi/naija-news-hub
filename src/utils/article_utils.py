#!/usr/bin/env python
"""
Utility functions for working with articles in the new schema.
"""
import json
import datetime
from typing import Dict, List, Any, Optional, Union

def create_article_metadata(
    content: str,
    title: str,
    author: Optional[str] = None,
    published_date: Optional[Union[datetime.datetime, str]] = None,
    source_website: Optional[str] = None,
    source_url: Optional[str] = None,
    image_url: Optional[str] = None,
    categories: Optional[List[Dict[str, str]]] = None,
    word_count: Optional[int] = None,
    reading_time: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a structured article metadata object for storage in the database.
    
    Args:
        content: The article content in Markdown format
        title: The article title
        author: The article author
        published_date: The publication date (datetime or ISO format string)
        source_website: The source website name
        source_url: The source URL
        image_url: The image URL
        categories: List of category objects with name and URL
        word_count: Word count of the article
        reading_time: Estimated reading time in minutes
        
    Returns:
        A structured metadata object ready for JSON serialization
    """
    # Calculate word count if not provided
    if word_count is None and content:
        word_count = len(content.split())
    
    # Calculate reading time if not provided (average reading speed: 200 words per minute)
    if reading_time is None and word_count:
        reading_time = max(1, round(word_count / 200))
    
    # Format published date if it's a datetime object
    if isinstance(published_date, datetime.datetime):
        published_date = published_date.isoformat()
    
    # Create the metadata structure
    metadata = {
        "content": {
            "markdown": content,
            "word_count": word_count,
            "reading_time": reading_time
        },
        "metadata": {
            "title": title,
            "author": author,
            "published_date": published_date,
            "source_website": source_website,
            "source_url": source_url,
            "image_url": image_url,
            "categories": categories or []
        }
    }
    
    return metadata

def format_tags(tags: List[str], base_url: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Format a list of tag strings into tag objects with names and URLs.
    
    Args:
        tags: List of tag strings
        base_url: Base URL for tag links (optional)
        
    Returns:
        List of tag objects with name and URL
    """
    formatted_tags = []
    
    for tag in tags:
        tag_obj = {"name": tag}
        
        if base_url:
            # Convert tag to URL-friendly format
            tag_slug = tag.lower().replace(' ', '-')
            tag_obj["url"] = f"{base_url}/tag/{tag_slug}"
            
        formatted_tags.append(tag_obj)
    
    return formatted_tags

def extract_content_from_metadata(article_metadata: Union[str, Dict[str, Any]]) -> str:
    """
    Extract the Markdown content from article metadata.
    
    Args:
        article_metadata: Article metadata as JSON string or dict
        
    Returns:
        Markdown content as string
    """
    # Parse JSON if needed
    if isinstance(article_metadata, str):
        metadata = json.loads(article_metadata)
    else:
        metadata = article_metadata
    
    # Extract content
    return metadata.get("content", {}).get("markdown", "")

def extract_metadata_field(
    article_metadata: Union[str, Dict[str, Any]], 
    field: str
) -> Any:
    """
    Extract a specific metadata field from article metadata.
    
    Args:
        article_metadata: Article metadata as JSON string or dict
        field: Field name to extract
        
    Returns:
        Field value or None if not found
    """
    # Parse JSON if needed
    if isinstance(article_metadata, str):
        metadata = json.loads(article_metadata)
    else:
        metadata = article_metadata
    
    # Extract field
    return metadata.get("metadata", {}).get(field)

def update_article_content(
    article_metadata: Union[str, Dict[str, Any]], 
    new_content: str
) -> Dict[str, Any]:
    """
    Update the content in article metadata.
    
    Args:
        article_metadata: Article metadata as JSON string or dict
        new_content: New Markdown content
        
    Returns:
        Updated metadata dict
    """
    # Parse JSON if needed
    if isinstance(article_metadata, str):
        metadata = json.loads(article_metadata)
    else:
        metadata = dict(article_metadata)  # Create a copy
    
    # Calculate word count
    word_count = len(new_content.split())
    
    # Calculate reading time
    reading_time = max(1, round(word_count / 200))
    
    # Update content
    if "content" not in metadata:
        metadata["content"] = {}
    
    metadata["content"]["markdown"] = new_content
    metadata["content"]["word_count"] = word_count
    metadata["content"]["reading_time"] = reading_time
    
    return metadata
