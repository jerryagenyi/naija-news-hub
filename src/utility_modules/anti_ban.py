"""
Anti-ban module for Naija News Hub.

This module provides functions to implement anti-ban measures for web scraping.
"""

import logging
import random
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlparse

# Configure logging
logger = logging.getLogger(__name__)

# List of common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
]

# List of common headers
COMMON_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}

class AntiBanManager:
    """Anti-ban manager for web scraping."""
    
    def __init__(self, 
                 rotate_user_agents: bool = True,
                 use_random_headers: bool = True,
                 custom_user_agents: Optional[List[str]] = None,
                 custom_headers: Optional[Dict[str, str]] = None,
                 domain_specific_config: Optional[Dict[str, Dict[str, Any]]] = None):
        """
        Initialize the anti-ban manager.
        
        Args:
            rotate_user_agents: Whether to rotate user agents
            use_random_headers: Whether to use random headers
            custom_user_agents: Custom user agents to use
            custom_headers: Custom headers to use
            domain_specific_config: Domain-specific configurations
        """
        self.rotate_user_agents = rotate_user_agents
        self.use_random_headers = use_random_headers
        self.user_agents = custom_user_agents or USER_AGENTS
        self.common_headers = custom_headers or COMMON_HEADERS
        self.domain_specific_config = domain_specific_config or {}
        
        logger.info(f"Anti-ban manager initialized with {len(self.user_agents)} user agents")
    
    def _get_domain(self, url: str) -> str:
        """
        Extract domain from URL.
        
        Args:
            url: URL to extract domain from
            
        Returns:
            Domain name
        """
        parsed_url = urlparse(url)
        return parsed_url.netloc
    
    def get_user_agent(self, url: str) -> str:
        """
        Get a user agent for a URL.
        
        Args:
            url: URL to get user agent for
            
        Returns:
            User agent string
        """
        domain = self._get_domain(url)
        
        # Check if there's a domain-specific user agent
        if domain in self.domain_specific_config and "user_agent" in self.domain_specific_config[domain]:
            return self.domain_specific_config[domain]["user_agent"]
        
        # Rotate user agents if enabled
        if self.rotate_user_agents:
            return random.choice(self.user_agents)
        
        # Default to first user agent
        return self.user_agents[0]
    
    def get_headers(self, url: str) -> Dict[str, str]:
        """
        Get headers for a URL.
        
        Args:
            url: URL to get headers for
            
        Returns:
            Headers dictionary
        """
        domain = self._get_domain(url)
        headers = {}
        
        # Add common headers
        headers.update(self.common_headers)
        
        # Add random Accept header variations if enabled
        if self.use_random_headers:
            # Randomize accept header slightly
            accept_variations = [
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            ]
            headers["Accept"] = random.choice(accept_variations)
            
            # Randomize accept-language
            lang_variations = [
                "en-US,en;q=0.9",
                "en-GB,en;q=0.9",
                "en-US,en;q=0.8",
                "en;q=0.9",
            ]
            headers["Accept-Language"] = random.choice(lang_variations)
        
        # Add referer for some requests
        if random.random() < 0.7:  # 70% chance to add referer
            domain_name = domain.split(".")
            if len(domain_name) >= 2:
                base_domain = f"{domain_name[-2]}.{domain_name[-1]}"
                headers["Referer"] = f"https://www.google.com/search?q=site:{base_domain}"
        
        # Add user agent
        headers["User-Agent"] = self.get_user_agent(url)
        
        # Check if there are domain-specific headers
        if domain in self.domain_specific_config and "headers" in self.domain_specific_config[domain]:
            headers.update(self.domain_specific_config[domain]["headers"])
        
        return headers
    
    def get_browser_config(self, url: str) -> Dict[str, Any]:
        """
        Get browser configuration for a URL.
        
        Args:
            url: URL to get browser configuration for
            
        Returns:
            Browser configuration dictionary
        """
        domain = self._get_domain(url)
        
        # Default browser configuration
        config = {
            "headless": True,
            "user_agent": self.get_user_agent(url),
            "viewport_width": random.choice([1280, 1366, 1440, 1920]),
            "viewport_height": random.choice([720, 768, 900, 1080]),
        }
        
        # Check if there's a domain-specific browser configuration
        if domain in self.domain_specific_config and "browser_config" in self.domain_specific_config[domain]:
            config.update(self.domain_specific_config[domain]["browser_config"])
        
        return config
    
    def get_crawler_config(self, url: str) -> Dict[str, Any]:
        """
        Get crawler configuration for a URL.
        
        Args:
            url: URL to get crawler configuration for
            
        Returns:
            Crawler configuration dictionary
        """
        domain = self._get_domain(url)
        
        # Default crawler configuration
        config = {}
        
        # Check if there's a domain-specific crawler configuration
        if domain in self.domain_specific_config and "crawler_config" in self.domain_specific_config[domain]:
            config.update(self.domain_specific_config[domain]["crawler_config"])
        
        return config

# Create a singleton instance
anti_ban_manager = AntiBanManager()

def get_user_agent(url: str) -> str:
    """
    Get a user agent for a URL.
    
    Args:
        url: URL to get user agent for
        
    Returns:
        User agent string
    """
    return anti_ban_manager.get_user_agent(url)

def get_headers(url: str) -> Dict[str, str]:
    """
    Get headers for a URL.
    
    Args:
        url: URL to get headers for
        
    Returns:
        Headers dictionary
    """
    return anti_ban_manager.get_headers(url)

def get_browser_config(url: str) -> Dict[str, Any]:
    """
    Get browser configuration for a URL.
    
    Args:
        url: URL to get browser configuration for
        
    Returns:
        Browser configuration dictionary
    """
    return anti_ban_manager.get_browser_config(url)

def get_crawler_config(url: str) -> Dict[str, Any]:
    """
    Get crawler configuration for a URL.
    
    Args:
        url: URL to get crawler configuration for
        
    Returns:
        Crawler configuration dictionary
    """
    return anti_ban_manager.get_crawler_config(url)

def configure_anti_ban(rotate_user_agents: bool = True,
                      use_random_headers: bool = True,
                      custom_user_agents: Optional[List[str]] = None,
                      custom_headers: Optional[Dict[str, str]] = None,
                      domain_specific_config: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
    """
    Configure the anti-ban manager.
    
    Args:
        rotate_user_agents: Whether to rotate user agents
        use_random_headers: Whether to use random headers
        custom_user_agents: Custom user agents to use
        custom_headers: Custom headers to use
        domain_specific_config: Domain-specific configurations
    """
    global anti_ban_manager
    anti_ban_manager = AntiBanManager(
        rotate_user_agents=rotate_user_agents,
        use_random_headers=use_random_headers,
        custom_user_agents=custom_user_agents,
        custom_headers=custom_headers,
        domain_specific_config=domain_specific_config
    )
