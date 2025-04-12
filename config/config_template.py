from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import timedelta

class Crawl4AIConfig(BaseModel):
    """Crawl4AI configuration settings"""
    max_depth: int = Field(default=2, description="Maximum crawl depth")
    stream: bool = Field(default=True, description="Stream results")
    rate_limit: Dict[str, int] = Field(
        default={"requests_per_second": 2},
        description="Rate limiting configuration"
    )
    retry_options: Dict[str, int] = Field(
        default={"max_retries": 3, "backoff_factor": 2},
        description="Retry configuration"
    )
    proxy_rotation: bool = Field(default=True, description="Enable proxy rotation")
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        description="User agent string"
    )

class DatabaseConfig(BaseModel):
    """Database configuration settings"""
    host: str = Field(..., description="Database host")
    port: int = Field(default=5432, description="Database port")
    database: str = Field(..., description="Database name")
    user: str = Field(..., description="Database user")
    password: str = Field(..., description="Database password")
    pool_size: int = Field(default=20, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Maximum overflow connections")

class APIConfig(BaseModel):
    """API configuration settings"""
    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8000, description="API port")
    debug: bool = Field(default=False, description="Debug mode")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins"
    )

class NigerianNewsConfig(BaseModel):
    """Nigerian news specific configuration"""
    date_formats: List[str] = Field(
        default=[
            "%Y-%m-%d %H:%M:%S",
            "%d %B %Y",
            "%B %d, %Y",
            "%d/%m/%Y",
            "%Y-%m-%d"
        ],
        description="Supported date formats"
    )
    languages: List[str] = Field(
        default=["en", "yo", "ig", "ha"],
        description="Supported languages"
    )
    content_validation: Dict[str, str] = Field(
        default={
            "title": r"^[A-Za-z0-9\s\-.,:;()]+$",
            "author": r"^[A-Za-z\s\-.,]+$",
            "content": r"^[\w\s\-.,:;()!?]+$"
        },
        description="Content validation patterns"
    )
    error_handling: Dict[str, int] = Field(
        default={
            "max_retries": 3,
            "timeout": 30,
            "backoff_factor": 2
        },
        description="Error handling configuration"
    )

class ProxyConfig(BaseModel):
    """Proxy configuration settings"""
    enabled: bool = Field(default=True, description="Enable proxy rotation")
    proxy_list: List[str] = Field(default=[], description="List of proxy servers")
    rotation_interval: int = Field(
        default=300,
        description="Proxy rotation interval in seconds"
    )
    max_failures: int = Field(
        default=3,
        description="Maximum failures before proxy is marked as bad"
    )

class ScraperConfig(BaseModel):
    """Scraper configuration settings"""
    max_articles_per_run: int = Field(default=10, description="Maximum number of articles to scrape per run")
    max_concurrent_requests: int = Field(default=5, description="Maximum number of concurrent requests")
    default_timeout: int = Field(default=30, description="Default timeout for requests in seconds")
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        description="User agent string"
    )
    retry_count: int = Field(default=3, description="Number of retries for failed requests")
    retry_delay: int = Field(default=2, description="Delay between retries in seconds")
    extract_images: bool = Field(default=True, description="Extract images from articles")
    extract_videos: bool = Field(default=True, description="Extract videos from articles")
    extract_links: bool = Field(default=True, description="Extract links from articles")
    extract_metadata: bool = Field(default=True, description="Extract metadata from articles")
    extract_categories: bool = Field(default=True, description="Extract categories from articles")
    extract_tags: bool = Field(default=True, description="Extract tags from articles")
    extract_authors: bool = Field(default=True, description="Extract authors from articles")
    extract_published_date: bool = Field(default=True, description="Extract published date from articles")
    extract_modified_date: bool = Field(default=True, description="Extract modified date from articles")
    extract_content: bool = Field(default=True, description="Extract content from articles")
    extract_comments: bool = Field(default=False, description="Extract comments from articles")
    extract_related: bool = Field(default=False, description="Extract related articles")
    extract_social: bool = Field(default=False, description="Extract social media links")
    extract_share_count: bool = Field(default=False, description="Extract share count")
    extract_view_count: bool = Field(default=False, description="Extract view count")
    extract_comment_count: bool = Field(default=False, description="Extract comment count")

class Config(BaseModel):
    """Main configuration class"""
    crawl4ai: Crawl4AIConfig = Field(default_factory=Crawl4AIConfig)
    database: DatabaseConfig
    api: APIConfig = Field(default_factory=APIConfig)
    nigerian_news: NigerianNewsConfig = Field(default_factory=NigerianNewsConfig)
    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    scraper: ScraperConfig = Field(default_factory=ScraperConfig)

    class Config:
        env_prefix = "NAIJA_NEWS_"
        env_file = ".env"
        env_file_encoding = "utf-8"

# Example usage:
"""
config = Config(
    database=DatabaseConfig(
        host="localhost",
        database="naija_news",
        user="postgres",
        password="password"
    )
)
"""