# Crawl4AI Integration

**Last Updated:** April 13, 2025

## Overview

This document describes the integration of Crawl4AI into the Naija News Hub project for web scraping and article extraction. Crawl4AI is a powerful web scraping library that provides advanced capabilities for handling dynamic content, JavaScript-rendered pages, and complex website structures.

## Integration Components

The Crawl4AI integration consists of the following components:

1. **URL Discovery Module** (`src/scraper/url_discovery.py`)
   - Discovers article URLs from news websites
   - Handles sitemap parsing
   - Processes category pages
   - Validates article URLs

2. **Article Extraction Module** (`src/scraper/article_extractor.py`)
   - Extracts article content from URLs
   - Cleans and normalizes content
   - Converts HTML to Markdown
   - Extracts metadata (title, author, date, etc.)

3. **Configuration** (`config/config.py` and `config/config_template.py`)
   - Configures Crawl4AI parameters
   - Sets up rate limiting
   - Configures proxy rotation
   - Sets user agents

## Implementation Details

### URL Discovery

The URL discovery module uses Crawl4AI's `AsyncWebCrawler` to discover article URLs from news websites. It implements three main functions:

1. `discover_urls(base_url, config)`: Discovers article URLs from a website's homepage
2. `discover_urls_from_sitemap(sitemap_url, config)`: Discovers article URLs from a sitemap
3. `discover_urls_from_category_pages(base_url, category_urls, config)`: Discovers article URLs from category pages

The module also includes a `is_valid_article_url(url, base_url)` function to validate discovered URLs and filter out non-article URLs.

### Article Extraction

The article extraction module uses Crawl4AI's `AsyncWebCrawler` to extract article content from URLs. It implements two main functions:

1. `extract_article(url, website_id, config)`: Extracts full article content including title, author, date, content, and metadata
2. `extract_article_metadata(url, config)`: Extracts only article metadata for quick processing

The module also includes helper functions:

1. `clean_article_content(content)`: Cleans article content by removing ads, navigation, etc.
2. `convert_to_markdown(content)`: Converts HTML content to Markdown

### Configuration

The Crawl4AI configuration is defined in `config/config_template.py` and implemented in `config/config.py`. The configuration includes:

```python
crawl4ai = CrawlConfig(
    max_depth=3,
    rate_limit={
        "requests_per_second": 2,
    },
    retry_options={
        "max_retries": 3,
        "backoff_factor": 2,
    },
    proxy_rotation=False,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
)
```

## Usage

### Testing the Scraper

The project includes a test command to test the scraper functionality:

```bash
python main.py test --url https://example.com/ --discover
python main.py test --url https://example.com/article/123 --extract
```

The `--discover` flag tests URL discovery, and the `--extract` flag tests article extraction.

### Running the Scraper

The scraper can be run using the following command:

```bash
python main.py scrape --website-id 1
```

To scrape all active websites:

```bash
python main.py scrape
```

## Error Handling

The Crawl4AI integration includes robust error handling:

1. **Retry Mechanism**: Implements exponential backoff for failed requests
2. **Fallback Mechanisms**: Returns dummy data when extraction fails
3. **Error Logging**: Logs detailed error messages for debugging
4. **Error Recovery**: Attempts to recover from common errors

## Future Improvements

1. **Circuit Breaker Pattern**: Implement circuit breaker pattern to prevent repeated failures
2. **Retry Queue**: Create a retry queue for failed scrapes
3. **Advanced Content Extraction**: Improve content extraction for different article formats
4. **Pipeline Monitoring**: Add monitoring for the scraping pipeline
5. **Proxy Rotation**: Implement proxy rotation for high-volume scraping

## Related Files

- `src/scraper/url_discovery.py`: URL discovery implementation
- `src/scraper/article_extractor.py`: Article extraction implementation
- `config/config.py`: Configuration implementation
- `config/config_template.py`: Configuration template
- `main.py`: Command-line interface for running the scraper
- `requirements.txt`: Project dependencies including Crawl4AI

## Dependencies

- `crawl4ai>=0.5.0`: The Crawl4AI library
- `playwright>=1.51.0`: Required by Crawl4AI for browser automation

## References

- [Crawl4AI Documentation](https://docs.crawl4ai.com/)
- [AsyncWebCrawler API](https://docs.crawl4ai.com/api/async-webcrawler/)
- [CrawlerRunConfig Parameters](https://docs.crawl4ai.com/api/crawler-run-config/)
- [BrowserConfig Parameters](https://docs.crawl4ai.com/api/browser-config/)
