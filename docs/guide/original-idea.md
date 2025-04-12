# Naija News Hub - Original Concept

## Project Overview

I am initiating a Nigerian news scraping project in Python. The challenge is that most Nigerian news websites have varying levels of accessibility and different technical implementations. This includes:

- Varying post/article URL formats
- Different sitemap indexing formats
- Some sitemaps being inaccessible
- Dynamic article listing instead of pagination
- Inconsistent website structures

The project aims to scrape news from at least 28 websites, developing a system that can take a base URL and automatically scrape all articles.

## User Interface

The frontend (implemented in Next.js) will present users with a multi-step form:
1. Input the base URL
2. System runs initial checks
3. If successful, proceed to next steps
4. Configure scraping parameters
5. Monitor scraping progress

## System Architecture

### Core Components

1. **Sitemap Generator**
   - Generates a sitemap of all available article URLs
   - Handles various sitemap formats and structures
   - Validates URLs and checks accessibility

2. **Article Scraper**
   - Uses generated sitemap to parse pages
   - Extracts article metadata:
     - Title
     - Author
     - Publication date
     - Category/categories
     - Article content

### Database Schema

1. **websites table**
   - Stores base URLs for each website
   - Tracks sitemap index information
   - Records first and last archive URLs

2. **sitemaps table**
   - Stores article URLs scraped from websites
   - Tracks URL validation status
   - Records last modification dates

3. **categories table**
   - Stores article categories from websites
   - Links categories to websites
   - Tracks category URLs

4. **articles table**
   - Stores scraped articles based on sitemaps
   - Contains full article content and metadata
   - Links to categories and websites

## Workflow

### Sitemap Generation Process

1. Receive base URL
2. Check for sitemap index
3. If available and accessible (200 status):
   - Store index in websites table
   - Check index range (e.g., post-sitemap.xml, post-sitemap-1.xml)
   - Store first and last archive URLs
   - Track for new pages based on last entry

4. If successful:
   - Complete first step of multi-stage form
   - Enable URL scraping functionality
   - Track completion status

### Error Handling and Monitoring

- Log errors in dedicated table
- Track error resolution status
- Implement monthly URL validation
- Monitor for new articles based on publication dates

## Future Enhancements

1. **Article Scraping Interface**
   - Form for inputting CSS selectors
   - LLM-assisted element identification
   - Progress tracking and status monitoring
   - Error handling and recovery

2. **Dynamic URL Discovery**
   - For websites without sitemaps:
     - Retrieve and validate category URLs
     - Store in categories table
     - Analyze pagination patterns
     - Generate article URLs
     - Track scraping progress
     - Implement resume functionality

3. **Automation and Maintenance**
   - n8n AI agents for:
     - New article detection
     - Error tracking
     - System maintenance
   - Automated workflows
   - Continuous monitoring

4. **Research Capabilities**
   - Vectorize stored information
   - LLM integration for research queries
   - Natural language interaction
   - Data analysis and insights

# The information is vectorised and stored for LLM to use. Based on all of the above, we develop an LLM that can interact with the vectorise information to allow researchers to chat with LLM for the content. For research purposes, etc. 