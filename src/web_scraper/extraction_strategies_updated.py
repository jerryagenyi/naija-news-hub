"""
Extraction strategies for Naija News Hub.

This module provides extraction strategies for different news websites.
"""

import logging
import os
from typing import Dict, Any, Optional
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, LLMExtractionStrategy
from crawl4ai import LLMConfig
from config.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def get_blueprint_extraction_strategy() -> JsonCssExtractionStrategy:
    """
    Get extraction strategy for Blueprint.ng.
    
    Returns:
        JsonCssExtractionStrategy: Extraction strategy for Blueprint.ng
    """
    schema = {
        "name": "Article",
        "baseSelector": "article, .article, .post, .entry, main",
        "fields": [
            {
                "name": "title",
                "selector": "h1.entry-title, h1, meta[property='og:title']",
                "type": "text"
            },
            {
                "name": "author",
                "selector": "a[rel='author'], .author-name, .entry-author, meta[name='author']",
                "type": "text",
                "default": "Unknown Author"
            },
            {
                "name": "published_date",
                "selector": "time.entry-date, .entry-date, meta[property='article:published_time']",
                "type": "datetime"
            },
            {
                "name": "content",
                "selector": ".entry-content, article",
                "type": "html",
                "exclude_selector": ".related-posts, .share-buttons, .advertisement, script, style"
            },
            {
                "name": "image_url",
                "selector": "img.wp-post-image, .post-thumbnail img, meta[property='og:image']",
                "type": "attribute",
                "attribute": "src"
            },
            {
                "name": "categories",
                "selector": ".cat-links a, .categories a",
                "type": "text",
                "multiple": True
            },
            {
                "name": "tags",
                "selector": ".tags-links a, .tags a",
                "type": "text",
                "multiple": True
            }
        ]
    }
    
    return JsonCssExtractionStrategy(schema)

def get_dailytrust_extraction_strategy() -> JsonCssExtractionStrategy:
    """
    Get extraction strategy for Daily Trust.
    
    Returns:
        JsonCssExtractionStrategy: Extraction strategy for Daily Trust
    """
    schema = {
        "name": "Article",
        "baseSelector": "article, .article, .post, .entry, main",
        "fields": [
            {
                "name": "title",
                "selector": "h1, meta[property='og:title']",
                "type": "text"
            },
            {
                "name": "author",
                "selector": ".author-name, .author, .entry-author, meta[name='author']",
                "type": "text",
                "default": "Unknown Author"
            },
            {
                "name": "published_date",
                "selector": ".entry-date, .date, .published-date, meta[property='article:published_time']",
                "type": "datetime"
            },
            {
                "name": "content",
                "selector": ".entry-content, .content, article",
                "type": "html",
                "exclude_selector": ".related-posts, .share-buttons, .advertisement, script, style"
            },
            {
                "name": "image_url",
                "selector": ".featured-image img, .post-thumbnail img, article img, meta[property='og:image']",
                "type": "attribute",
                "attribute": "src"
            },
            {
                "name": "categories",
                "selector": ".cat-links a, .categories a",
                "type": "text",
                "multiple": True
            },
            {
                "name": "tags",
                "selector": ".tags-links a, .tags a",
                "type": "text",
                "multiple": True
            }
        ]
    }
    
    return JsonCssExtractionStrategy(schema)

def get_llm_extraction_strategy() -> LLMExtractionStrategy:
    """
    Get LLM-based extraction strategy for complex cases.
    
    Returns:
        LLMExtractionStrategy: LLM-based extraction strategy
    """
    # Get configuration
    app_config = get_config()
    
    # Define the schema for article extraction
    schema = {
        "title": "Article",
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the article"
            },
            "author": {
                "type": "string",
                "description": "The author of the article. Look for bylines, author tags, or metadata."
            },
            "published_date": {
                "type": "string",
                "description": "The publication date of the article in ISO format (YYYY-MM-DD)"
            },
            "content": {
                "type": "string",
                "description": "The main content of the article, excluding navigation, ads, and related content"
            },
            "image_url": {
                "type": "string",
                "description": "The URL of the main image of the article"
            },
            "categories": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Categories or sections the article belongs to"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Tags associated with the article"
            }
        },
        "required": ["title", "content"]
    }
    
    # Use OpenAI if API key is available, otherwise use a fallback
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        llm_config = LLMConfig(
            provider="openai/gpt-4o-mini",
            api_token=api_key
        )
    else:
        # Fallback to a local model if available
        llm_config = LLMConfig(
            provider="ollama/llama3",
            api_token=None  # No token needed for Ollama
        )
    
    return LLMExtractionStrategy(
        llm_config=llm_config,
        schema=schema,
        extraction_type="schema",
        instruction="Extract the article information from the HTML. Focus on finding the author information from any location in the HTML, including bylines, metadata, or structured data."
    )

def get_cosine_extraction_strategy():
    """
    Get cosine similarity extraction strategy for content extraction.
    
    Returns:
        CosineStrategy: Cosine similarity extraction strategy
    """
    from crawl4ai.extraction_strategy import CosineStrategy
    
    return CosineStrategy(
        semantic_filter="main article content",
        word_count_threshold=100,  # Longer blocks for articles
        top_k=1,                   # Usually want single main content
        sim_threshold=0.3          # Similarity threshold for clustering
    )

def get_extraction_strategy_for_website(website_id: int) -> Optional[JsonCssExtractionStrategy]:
    """
    Get extraction strategy for a website.
    
    Args:
        website_id: ID of the website
        
    Returns:
        Optional[JsonCssExtractionStrategy]: Extraction strategy for the website
    """
    # Map website IDs to extraction strategies
    # In a real implementation, this would be stored in the database
    strategies = {
        1: get_blueprint_extraction_strategy(),
        2: get_dailytrust_extraction_strategy()
    }
    
    return strategies.get(website_id)

def get_fallback_extraction_strategy():
    """
    Get fallback extraction strategy for unknown websites.
    
    Returns:
        Extraction strategy: Fallback extraction strategy
    """
    # Try cosine similarity first as it's faster than LLM
    try:
        return get_cosine_extraction_strategy()
    except ImportError:
        # If cosine strategy is not available, fall back to LLM
        return get_llm_extraction_strategy()
