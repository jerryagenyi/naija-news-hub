"""
Core functionality for scraping news articles from websites.
"""

import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from newspaper import Article as NewspaperArticle
from newspaper import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ArticleScraper:
    """
    A class for scraping news articles from a website.
    """
    
    def __init__(self, base_url: str, user_agent: Optional[str] = None):
        """
        Initialize the ArticleScraper with a base URL.
        
        Args:
            base_url: The base URL of the news website
            user_agent: Custom user agent string (optional)
        """
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        
        # Configure newspaper
        self.config = Config()
        self.config.browser_user_agent = user_agent or 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        self.config.request_timeout = 10
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config.browser_user_agent})
        
        logger.info(f"Initialized scraper for {self.domain}")
    
    def get_article_links(self, limit: int = 10) -> List[str]:
        """
        Extract article links from the homepage or sitemap.
        
        Args:
            limit: Maximum number of links to return
            
        Returns:
            List of article URLs
        """
        try:
            # First try to get the homepage
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for article links - common patterns in news sites
            article_links = []
            
            # Find all links
            for link in soup.find_all('a', href=True):
                url = link['href']
                
                # Make relative URLs absolute
                if not url.startswith(('http://', 'https://')):
                    url = urljoin(self.base_url, url)
                
                # Skip if not from the same domain
                if self.domain not in urlparse(url).netloc:
                    continue
                
                # Skip common non-article URLs
                if any(pattern in url for pattern in [
                    '/tag/', '/category/', '/author/', '/about/', '/contact/',
                    '/search', '/page/', '/wp-content/', '/wp-admin/', '/feed/',
                    'javascript:', 'mailto:', '#', '?s=', '/wp-json/'
                ]):
                    continue
                
                # Look for patterns that suggest this is an article
                # Most news sites have URLs with dates, slugs, or IDs
                if (
                    re.search(r'/\d{4}/\d{2}/\d{2}/', url) or  # Date pattern
                    re.search(r'/news/|/article/|/story/', url) or  # Common article paths
                    re.search(r'-news$|-article$|-story$|\.html$', url)  # Common endings
                ):
                    if url not in article_links:
                        article_links.append(url)
            
            # Try to find article containers
            article_containers = soup.select('article, .article, .post, .story, .news-item, .entry')
            for container in article_containers:
                links = container.find_all('a', href=True)
                for link in links:
                    url = link['href']
                    if not url.startswith(('http://', 'https://')):
                        url = urljoin(self.base_url, url)
                    if url not in article_links and self.domain in urlparse(url).netloc:
                        article_links.append(url)
            
            logger.info(f"Found {len(article_links)} potential article links")
            return article_links[:limit]
            
        except Exception as e:
            logger.error(f"Error getting article links: {e}")
            return []
    
    def scrape_article(self, url: str) -> Optional[Dict[str, Union[str, datetime, List[str]]]]:
        """
        Scrape a single article from the given URL.
        
        Args:
            url: The URL of the article to scrape
            
        Returns:
            Dictionary containing article data or None if scraping failed
        """
        try:
            logger.info(f"Scraping article: {url}")
            
            # Use newspaper3k to extract article content
            article = NewspaperArticle(url, config=self.config)
            article.download()
            article.parse()
            article.nlp()  # Extract keywords and summary
            
            # Create article data dictionary
            article_data = {
                'url': url,
                'title': article.title,
                'text': article.text,
                'summary': article.summary,
                'keywords': article.keywords,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'top_image': article.top_image,
                'scraped_at': datetime.now()
            }
            
            # If newspaper3k couldn't extract some data, try with BeautifulSoup
            if not article.title or not article.text:
                logger.info(f"Using fallback extraction for {url}")
                response = self.session.get(url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try to extract title if missing
                if not article_data['title']:
                    title_tag = soup.find('h1') or soup.find('title')
                    if title_tag:
                        article_data['title'] = title_tag.get_text().strip()
                
                # Try to extract content if missing
                if not article_data['text']:
                    # Look for common content containers
                    content_selectors = [
                        'article', '.article-content', '.post-content', 
                        '.entry-content', '.story-content', '.news-content',
                        '[itemprop="articleBody"]', '.content-area'
                    ]
                    
                    for selector in content_selectors:
                        content = soup.select_one(selector)
                        if content:
                            # Remove unwanted elements
                            for unwanted in content.select('script, style, .ad, .advertisement, .social-share, .related-posts'):
                                unwanted.decompose()
                            
                            paragraphs = [p.get_text().strip() for p in content.find_all('p') if p.get_text().strip()]
                            if paragraphs:
                                article_data['text'] = '\n\n'.join(paragraphs)
                                break
            
            # Check if we have the minimum required data
            if not article_data['title'] or not article_data['text']:
                logger.warning(f"Could not extract essential content from {url}")
                return None
                
            logger.info(f"Successfully scraped article: {article_data['title']}")
            return article_data
            
        except Exception as e:
            logger.error(f"Error scraping article {url}: {e}")
            return None
    
    def scrape_multiple_articles(self, urls: List[str]) -> List[Dict[str, Union[str, datetime, List[str]]]]:
        """
        Scrape multiple articles from the given URLs.
        
        Args:
            urls: List of article URLs to scrape
            
        Returns:
            List of dictionaries containing article data
        """
        articles = []
        for url in urls:
            article_data = self.scrape_article(url)
            if article_data:
                articles.append(article_data)
        
        logger.info(f"Successfully scraped {len(articles)} articles")
        return articles
