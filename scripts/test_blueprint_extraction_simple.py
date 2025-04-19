#!/usr/bin/env python3
"""
Simple test script to extract articles from blueprint.ng using specific URLs.
"""

import sys
import asyncio
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

# Add the project root to the Python path
sys.path.append(".")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def extract_article(url: str) -> Dict[str, Any]:
    """Extract article from URL using requests and BeautifulSoup."""
    logger.info(f"Extracting article from {url}")
    
    try:
        # Get the page content
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.title.text if soup.title else f"Article from {url}"
        
        # Extract content
        content_element = soup.find('article') or soup.find(class_='post-content') or soup.find(class_='entry-content') or soup.find('main')
        content = content_element.text if content_element else "Content could not be extracted"
        content_html = str(content_element) if content_element else ""
        
        # Extract author
        author_element = soup.find(class_='author') or soup.find(class_='byline') or soup.find(rel='author')
        author = author_element.text if author_element else "Unknown Author"
        
        # Extract image
        image_element = soup.find('meta', property='og:image') or soup.find('img', class_='wp-post-image')
        image_url = image_element['content'] if image_element and 'content' in image_element.attrs else \
                   image_element['src'] if image_element and 'src' in image_element.attrs else None
        
        # Calculate word count and reading time
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)
        
        # Create article data
        article_data = {
            "title": title,
            "url": url,
            "content": content,
            "content_html": content_html,
            "author": author,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "image_url": image_url,
            "word_count": word_count,
            "reading_time": reading_time,
        }
        
        logger.info(f"Successfully extracted article: {article_data['title']}")
        return article_data
    
    except Exception as e:
        logger.error(f"Error extracting article from {url}: {str(e)}")
        return {
            "title": f"Error extracting article from {url}",
            "url": url,
            "content": f"Error: {str(e)}",
            "content_html": "",
            "author": "Unknown",
            "published_at": datetime.now(timezone.utc).isoformat(),
            "image_url": None,
            "word_count": 0,
            "reading_time": 0,
        }

async def test_blueprint_extraction():
    """Test article extraction from blueprint.ng using specific URLs."""
    # Use specific article URLs from blueprint.ng
    urls = [
        "https://blueprint.ng/csos-laud-tinubu-matawalle-for-progress-in-fight-against-insecurity/",
        "https://blueprint.ng/maikalangus-defection-to-apc-game-changer-for-amac-residents-bravo-oluohu/",
        "https://blueprint.ng/nerc-electricity-value-chain-and-power-sector-overview/",
        "https://blueprint.ng/easter-imbibe-spirit-of-love-togetherness-nnpp-chieftain-urges-nigerians/",
        "https://blueprint.ng/we-have-expanded-access-to-tertiary-education-in-kaduna-state-gov-sani/"
    ]
    
    logger.info(f"Selected {len(urls)} URLs for extraction")
    
    # Extract articles
    articles = []
    for url in urls:
        article_data = await extract_article(url)
        articles.append(article_data)
    
    # Print the extracted articles
    logger.info(f"Extracted {len(articles)} articles")
    for i, article in enumerate(articles):
        logger.info(f"Article {i+1}:")
        logger.info(f"Title: {article['title']}")
        logger.info(f"URL: {article['url']}")
        logger.info(f"Author: {article['author']}")
        logger.info(f"Published at: {article['published_at']}")
        logger.info(f"Word count: {article['word_count']}")
        logger.info(f"Content preview: {article['content'][:200]}...")
        logger.info("-" * 80)
    
    return articles

if __name__ == "__main__":
    asyncio.run(test_blueprint_extraction())
