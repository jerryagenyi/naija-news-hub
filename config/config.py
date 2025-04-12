"""
Configuration loader for Naija News Hub.

This module loads the configuration from environment variables and .env file.
"""

import os
from typing import Optional
from pathlib import Path

from config.config_template import Config, DatabaseConfig

def load_config() -> Config:
    """
    Load configuration from environment variables and .env file.
    
    Returns:
        Config: Configuration object
    """
    # Ensure database configuration is provided
    database_config = DatabaseConfig(
        host=os.getenv("NAIJA_NEWS_DB_HOST", "localhost"),
        port=int(os.getenv("NAIJA_NEWS_DB_PORT", "5432")),
        database=os.getenv("NAIJA_NEWS_DB_NAME", "naija_news"),
        user=os.getenv("NAIJA_NEWS_DB_USER", "postgres"),
        password=os.getenv("NAIJA_NEWS_DB_PASSWORD", ""),
    )
    
    # Create and return the config object
    return Config(database=database_config)

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
