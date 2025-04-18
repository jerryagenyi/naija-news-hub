"""
Configuration loader for Naija News Hub.

This module loads the configuration from environment variables and .env file.
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

from config.config_template import Config, DatabaseConfig, APIConfig, NigerianNewsConfig, ProxyConfig, Crawl4AIConfig, ScraperConfig, ContentValidationConfig

# Load environment variables from .env file
load_dotenv()

def load_config() -> Config:
    """
    Load configuration from environment variables and .env file.

    Returns:
        Config: Configuration object
    """
    # Ensure database configuration is provided
    # Get database name and replace hyphens with underscores for PostgreSQL compatibility
    db_name = os.getenv("NAIJA_NEWS_DB_NAME", "naija_news_hub")
    db_name = db_name.replace("-", "_")

    database_config = DatabaseConfig(
        host=os.getenv("NAIJA_NEWS_DB_HOST", "localhost"),
        port=int(os.getenv("NAIJA_NEWS_DB_PORT", "5432")),
        database=db_name,
        user=os.getenv("NAIJA_NEWS_DB_USER", "jeremiah"),
        password=os.getenv("NAIJA_NEWS_DB_PASSWORD", "naija1"),
    )

    # Create API configuration
    api_config = APIConfig(
        host=os.getenv("NAIJA_NEWS_API_HOST", "0.0.0.0"),
        port=int(os.getenv("NAIJA_NEWS_API_PORT", "8000")),
        debug=os.getenv("NAIJA_NEWS_API_DEBUG", "False").lower() == "true",
        cors_origins=os.getenv("NAIJA_NEWS_API_CORS_ORIGINS", "http://localhost:3000").split(","),
    )

    # Create Crawl4AI configuration
    crawl4ai_config = Crawl4AIConfig(
        max_depth=int(os.getenv("NAIJA_NEWS_CRAWL4AI_MAX_DEPTH", "2")),
        stream=os.getenv("NAIJA_NEWS_CRAWL4AI_STREAM", "True").lower() == "true",
        rate_limit={
            "requests_per_second": int(os.getenv("NAIJA_NEWS_CRAWL4AI_RATE_LIMIT", "2")),
        },
        retry_options={
            "max_retries": int(os.getenv("NAIJA_NEWS_CRAWL4AI_MAX_RETRIES", "3")),
            "backoff_factor": int(os.getenv("NAIJA_NEWS_CRAWL4AI_BACKOFF_FACTOR", "2")),
        },
        proxy_rotation=os.getenv("NAIJA_NEWS_CRAWL4AI_PROXY_ROTATION", "True").lower() == "true",
        user_agent=os.getenv("NAIJA_NEWS_CRAWL4AI_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"),
    )

    # Create Nigerian news configuration
    nigerian_news_config = NigerianNewsConfig()

    # Create proxy configuration
    proxy_config = ProxyConfig(
        enabled=os.getenv("NAIJA_NEWS_PROXY_ENABLED", "True").lower() == "true",
        proxy_list=os.getenv("NAIJA_NEWS_PROXY_LIST", "").split(",") if os.getenv("NAIJA_NEWS_PROXY_LIST") else [],
        rotation_interval=int(os.getenv("NAIJA_NEWS_PROXY_ROTATION_INTERVAL", "300")),
        max_failures=int(os.getenv("NAIJA_NEWS_PROXY_MAX_FAILURES", "3")),
    )

    # Create scraper configuration
    scraper_config = ScraperConfig(
        max_articles_per_run=int(os.getenv("NAIJA_NEWS_SCRAPER_MAX_ARTICLES", "10")),
        max_concurrent_requests=int(os.getenv("NAIJA_NEWS_SCRAPER_MAX_CONCURRENT", "5")),
        default_timeout=int(os.getenv("NAIJA_NEWS_SCRAPER_TIMEOUT", "30")),
        user_agent=os.getenv("NAIJA_NEWS_SCRAPER_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"),
        retry_count=int(os.getenv("NAIJA_NEWS_SCRAPER_RETRY_COUNT", "3")),
        retry_delay=int(os.getenv("NAIJA_NEWS_SCRAPER_RETRY_DELAY", "2")),
    )

    # Create content validation configuration
    content_validation_config = ContentValidationConfig(
        enabled=os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_ENABLED", "True").lower() == "true",
        min_quality_score=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MIN_QUALITY_SCORE", "50")),
        reject_low_quality=os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_REJECT_LOW_QUALITY", "True").lower() == "true",
        min_title_length=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MIN_TITLE_LENGTH", "10")),
        max_title_length=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MAX_TITLE_LENGTH", "200")),
        min_content_length=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MIN_CONTENT_LENGTH", "100")),
        max_content_length=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MAX_CONTENT_LENGTH", "100000")),
        min_word_count=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MIN_WORD_COUNT", "50")),
        min_paragraph_count=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MIN_PARAGRAPH_COUNT", "2")),
        max_duplicate_paragraph_ratio=float(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MAX_DUPLICATE_PARAGRAPH_RATIO", "0.3")),
        max_ad_content_ratio=float(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MAX_AD_CONTENT_RATIO", "0.2")),
        min_image_count=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MIN_IMAGE_COUNT", "0")),
        max_recent_date_days=int(os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_MAX_RECENT_DATE_DAYS", "1825")),
        detect_clickbait=os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_DETECT_CLICKBAIT", "True").lower() == "true",
        detect_spam=os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_DETECT_SPAM", "True").lower() == "true",
        detect_placeholder=os.getenv("NAIJA_NEWS_CONTENT_VALIDATION_DETECT_PLACEHOLDER", "True").lower() == "true"
    )

    # Create and return the config object
    return Config(
        database=database_config,
        api=api_config,
        crawl4ai=crawl4ai_config,
        nigerian_news=nigerian_news_config,
        proxy=proxy_config,
        scraper=scraper_config,
        content_validation=content_validation_config
    )

# Global configuration instance
config: Optional[Config] = None

def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config: Configuration object
    """
    global config
    if config is None:
        config = load_config()
    return config
