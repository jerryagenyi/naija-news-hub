# Crawl4AI Best Practices

**Last Updated:** April 19, 2025

## Overview

This document outlines best practices for using Crawl4AI in the Naija News Hub project. These practices are based on the latest Crawl4AI documentation and are designed to maximize the effectiveness of web scraping and article extraction.

## Key Components

1. **URL Discovery** (`src/web_scraper/url_discovery_updated.py`)
2. **Article Extraction** (`src/web_scraper/article_extractor_updated.py`)
3. **Extraction Strategies** (`src/web_scraper/extraction_strategies_updated.py`)

## Best Practices

### 1. URL Discovery

#### Use Crawl4AI's Built-in Link Extraction

Instead of manually parsing HTML with regex to find links, use Crawl4AI's built-in link extraction:

```python
# Use result.links which contains all links found on the page
if result.links and isinstance(result.links, dict) and 'internal' in result.links:
    # Get internal links (same domain)
    internal_links = result.links['internal']
    logger.info(f"Found {len(internal_links)} internal links")
    
    # Add all internal links to our list
    urls.extend(internal_links)
```

#### Optimize Crawler Configuration for Different Tasks

Use different crawler configurations for different tasks:

```python
# For homepage crawling
crawler_run_config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    excluded_selector="nav, footer, header, .sidebar, .menu, .navigation",
    excluded_tags=["script", "style", "noscript", "iframe"],
    exclude_external_links=False,
    exclude_social_media_links=True,
    scan_full_page=True,
    wait_until="networkidle"
)

# For sitemap parsing
crawler_run_config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    excluded_selector="nav, footer, header, .sidebar, .menu, .navigation",
    excluded_tags=["script", "style", "noscript", "iframe"],
    exclude_external_links=False,
    exclude_social_media_links=True,
    wait_until="networkidle",
    content_type="xml"  # Specify XML content type for sitemaps
)
```

### 2. Article Extraction

#### Use Extraction Strategies

Use specialized extraction strategies for different websites:

```python
# Get extraction strategy for the website
extraction_strategy = get_extraction_strategy_for_website(website_id)
if not extraction_strategy:
    logger.warning(f"No extraction strategy found for website ID {website_id}, using fallback strategy")
    extraction_strategy = get_fallback_extraction_strategy()

# Create crawler run config
crawler_run_config = CrawlerRunConfig(
    # ...
    extraction_strategy=extraction_strategy,
    # ...
)
```

#### Use Fit Markdown for Better Content Extraction

Enable fit markdown for better content extraction:

```python
crawler_run_config = CrawlerRunConfig(
    # ...
    fit_markdown=True,  # Enable fit markdown for better content extraction
    # ...
)

# Use fit_markdown for better content extraction if available
content_markdown = result.markdown.fit_markdown if result.markdown and hasattr(result.markdown, 'fit_markdown') else \
                  result.markdown.raw_markdown if result.markdown else ""
```

#### Use Adaptive Memory Management

Use adaptive memory management to prevent browser crashes:

```python
browser_config = BrowserConfig(
    headless=True,
    user_agent=config.get("user_agent", crawl_config.user_agent) if config else crawl_config.user_agent,
    memory_limit="adaptive",  # Adaptive memory management
    viewport={"width": 1280, "height": 800},
    timeout=30000  # 30 seconds timeout
)
```

#### Use Media Extraction

Use Crawl4AI's built-in media extraction:

```python
# Try to find image URLs in the media if not found in extraction strategy
if not image_url and result.media and 'images' in result.media and result.media['images']:
    # Use the first image with the highest score
    images = sorted(result.media['images'], key=lambda x: x.get('score', 0), reverse=True)
    if images:
        image_url = images[0].get('src')
```

### 3. Extraction Strategies

#### Use JsonCssExtractionStrategy for Known Websites

Use JsonCssExtractionStrategy for known websites with predictable structure:

```python
schema = {
    "name": "Article",
    "baseSelector": "article, .article, .post, .entry, main",
    "fields": [
        {
            "name": "title",
            "selector": "h1.entry-title, h1, meta[property='og:title']",
            "type": "text"
        },
        # ...
    ]
}

return JsonCssExtractionStrategy(schema)
```

#### Use CosineStrategy for Unknown Websites

Use CosineStrategy for unknown websites as a faster alternative to LLM:

```python
return CosineStrategy(
    semantic_filter="main article content",
    word_count_threshold=100,  # Longer blocks for articles
    top_k=1,                   # Usually want single main content
    sim_threshold=0.3          # Similarity threshold for clustering
)
```

#### Use LLMExtractionStrategy as a Fallback

Use LLMExtractionStrategy as a fallback for complex cases:

```python
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
    instruction="Extract the article information from the HTML..."
)
```

## Implementation

The updated implementation includes:

1. **URL Discovery** (`src/web_scraper/url_discovery_updated.py`)
   - Uses Crawl4AI's built-in link extraction
   - Optimizes crawler configuration for different tasks
   - Implements robust error handling

2. **Article Extraction** (`src/web_scraper/article_extractor_updated.py`)
   - Uses extraction strategies
   - Uses fit markdown for better content extraction
   - Uses adaptive memory management
   - Uses media extraction
   - Implements robust error handling and fallback mechanisms

3. **Extraction Strategies** (`src/web_scraper/extraction_strategies_updated.py`)
   - Uses JsonCssExtractionStrategy for known websites
   - Uses CosineStrategy for unknown websites
   - Uses LLMExtractionStrategy as a fallback

## Conclusion

By following these best practices, the Naija News Hub project can maximize the effectiveness of web scraping and article extraction using Crawl4AI. The updated implementation is more robust, efficient, and aligned with the latest Crawl4AI documentation.
