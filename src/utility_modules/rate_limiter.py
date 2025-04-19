"""
Rate limiter module for Naija News Hub.

This module provides functions to implement rate limiting and retries for web scraping.
"""

import logging
import time
import asyncio
import random
from typing import Dict, Any, Callable, Awaitable, Optional, TypeVar, List
from urllib.parse import urlparse
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)

# Type variable for generic function
T = TypeVar('T')

class RateLimiter:
    """Rate limiter for web scraping."""
    
    def __init__(self, 
                 requests_per_minute: int = 10, 
                 max_retries: int = 3, 
                 retry_delay: float = 2.0,
                 jitter: float = 0.5,
                 domain_specific_limits: Optional[Dict[str, int]] = None):
        """
        Initialize the rate limiter.
        
        Args:
            requests_per_minute: Maximum number of requests per minute
            max_retries: Maximum number of retries for failed requests
            retry_delay: Base delay between retries in seconds
            jitter: Random jitter to add to delays (0-1)
            domain_specific_limits: Domain-specific rate limits (requests per minute)
        """
        self.requests_per_minute = requests_per_minute
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.jitter = jitter
        self.domain_specific_limits = domain_specific_limits or {}
        
        # Track request timestamps by domain
        self.request_history: Dict[str, List[datetime]] = {}
        
        # Track domain-specific semaphores
        self.domain_semaphores: Dict[str, asyncio.Semaphore] = {}
        
        logger.info(f"Rate limiter initialized with {requests_per_minute} requests per minute")
        if domain_specific_limits:
            for domain, limit in domain_specific_limits.items():
                logger.info(f"Domain-specific limit for {domain}: {limit} requests per minute")
    
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
    
    def _get_domain_limit(self, domain: str) -> int:
        """
        Get rate limit for a domain.
        
        Args:
            domain: Domain name
            
        Returns:
            Rate limit (requests per minute)
        """
        return self.domain_specific_limits.get(domain, self.requests_per_minute)
    
    def _get_domain_semaphore(self, domain: str) -> asyncio.Semaphore:
        """
        Get or create a semaphore for a domain.
        
        Args:
            domain: Domain name
            
        Returns:
            Semaphore for the domain
        """
        if domain not in self.domain_semaphores:
            limit = self._get_domain_limit(domain)
            # Allow concurrent requests up to the limit
            self.domain_semaphores[domain] = asyncio.Semaphore(max(1, limit // 2))
        return self.domain_semaphores[domain]
    
    async def _wait_for_rate_limit(self, domain: str) -> None:
        """
        Wait if necessary to comply with rate limits.
        
        Args:
            domain: Domain name
        """
        # Get domain-specific rate limit
        limit = self._get_domain_limit(domain)
        
        # Initialize request history for domain if not exists
        if domain not in self.request_history:
            self.request_history[domain] = []
        
        # Clean up old requests (older than 1 minute)
        now = datetime.now()
        self.request_history[domain] = [
            timestamp for timestamp in self.request_history[domain]
            if now - timestamp < timedelta(minutes=1)
        ]
        
        # Check if we need to wait
        if len(self.request_history[domain]) >= limit:
            # Calculate wait time
            oldest_timestamp = self.request_history[domain][0]
            wait_time = 60 - (now - oldest_timestamp).total_seconds()
            
            if wait_time > 0:
                # Add some jitter to avoid thundering herd
                jitter_amount = random.uniform(0, self.jitter * wait_time)
                total_wait = wait_time + jitter_amount
                
                logger.info(f"Rate limit reached for {domain}, waiting {total_wait:.2f} seconds")
                await asyncio.sleep(total_wait)
        
        # Add current timestamp to history
        self.request_history[domain].append(datetime.now())
    
    async def execute_with_rate_limit(self, 
                                     func: Callable[..., Awaitable[T]], 
                                     url: str, 
                                     *args: Any, 
                                     **kwargs: Any) -> Optional[T]:
        """
        Execute a function with rate limiting and retries.
        
        Args:
            func: Async function to execute
            url: URL to scrape
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the function or None if all retries failed
        """
        domain = self._get_domain(url)
        semaphore = self._get_domain_semaphore(domain)
        
        # Use semaphore to limit concurrent requests to the same domain
        async with semaphore:
            # Wait for rate limit
            await self._wait_for_rate_limit(domain)
            
            # Try to execute the function with retries
            for attempt in range(self.max_retries + 1):
                try:
                    return await func(url, *args, **kwargs)
                except Exception as e:
                    if attempt < self.max_retries:
                        # Calculate retry delay with exponential backoff and jitter
                        delay = self.retry_delay * (2 ** attempt)
                        jitter_amount = random.uniform(0, self.jitter * delay)
                        total_delay = delay + jitter_amount
                        
                        logger.warning(f"Request to {url} failed (attempt {attempt + 1}/{self.max_retries + 1}): {str(e)}")
                        logger.info(f"Retrying in {total_delay:.2f} seconds")
                        
                        await asyncio.sleep(total_delay)
                    else:
                        logger.error(f"Request to {url} failed after {self.max_retries + 1} attempts: {str(e)}")
                        return None

# Create a singleton instance
rate_limiter = RateLimiter()

async def execute_with_rate_limit(func: Callable[..., Awaitable[T]], 
                                 url: str, 
                                 *args: Any, 
                                 **kwargs: Any) -> Optional[T]:
    """
    Execute a function with rate limiting and retries.
    
    Args:
        func: Async function to execute
        url: URL to scrape
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
        
    Returns:
        Result of the function or None if all retries failed
    """
    return await rate_limiter.execute_with_rate_limit(func, url, *args, **kwargs)

def configure_rate_limiter(requests_per_minute: int = 10, 
                          max_retries: int = 3, 
                          retry_delay: float = 2.0,
                          jitter: float = 0.5,
                          domain_specific_limits: Optional[Dict[str, int]] = None) -> None:
    """
    Configure the rate limiter.
    
    Args:
        requests_per_minute: Maximum number of requests per minute
        max_retries: Maximum number of retries for failed requests
        retry_delay: Base delay between retries in seconds
        jitter: Random jitter to add to delays (0-1)
        domain_specific_limits: Domain-specific rate limits (requests per minute)
    """
    global rate_limiter
    rate_limiter = RateLimiter(
        requests_per_minute=requests_per_minute,
        max_retries=max_retries,
        retry_delay=retry_delay,
        jitter=jitter,
        domain_specific_limits=domain_specific_limits
    )
