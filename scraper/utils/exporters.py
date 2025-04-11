"""
Functions for exporting scraped articles to various formats.
"""

import csv
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Union

logger = logging.getLogger(__name__)

def save_to_json(articles: List[Dict[str, Union[str, datetime, List[str]]]], output_path: str) -> str:
    """
    Save scraped articles to a JSON file.
    
    Args:
        articles: List of article dictionaries
        output_path: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    os.makedirs(output_path, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"articles_{timestamp}.json"
    filepath = os.path.join(output_path, filename)
    
    # Convert datetime objects to strings
    serializable_articles = []
    for article in articles:
        serializable_article = {}
        for key, value in article.items():
            if isinstance(value, datetime):
                serializable_article[key] = value.isoformat()
            else:
                serializable_article[key] = value
        serializable_articles.append(serializable_article)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(serializable_articles, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Saved {len(articles)} articles to {filepath}")
    return filepath

def save_to_csv(articles: List[Dict[str, Union[str, datetime, List[str]]]], output_path: str) -> str:
    """
    Save scraped articles to a CSV file.
    
    Args:
        articles: List of article dictionaries
        output_path: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    os.makedirs(output_path, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"articles_{timestamp}.csv"
    filepath = os.path.join(output_path, filename)
    
    if not articles:
        logger.warning("No articles to save")
        return ""
    
    # Get all possible fields from all articles
    fieldnames = set()
    for article in articles:
        fieldnames.update(article.keys())
    fieldnames = sorted(list(fieldnames))
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for article in articles:
            # Convert datetime objects to strings
            row = {}
            for key, value in article.items():
                if isinstance(value, datetime):
                    row[key] = value.isoformat()
                elif isinstance(value, list):
                    row[key] = ', '.join(str(item) for item in value)
                else:
                    row[key] = value
            writer.writerow(row)
    
    logger.info(f"Saved {len(articles)} articles to {filepath}")
    return filepath
