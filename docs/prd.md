# Naija News Hub - Product Requirements Document (PRD)

## 1. Introduction

### 1.1 Project Overview
* Project Name: Naija News Hub  
* Simple Descriptor: Nigerian News Aggregation & Analysis Platform  
* Purpose: To build a robust, adaptable, and scalable system for aggregating news content from a diverse range of Nigerian online news sources, enabling data-driven research and analysis.  
* Target Audience: Researchers, analysts, journalists, and users seeking access to a consolidated source of Nigerian news.

### 1.2 Scope
The project will create a system capable of:
- Accepting a base URL through a user-friendly interface
- Automatically discovering article URLs through various methods (sitemap parsing, category page crawling)
- Extracting article content and metadata
- Storing the data in a structured format
- Providing mechanisms for monitoring, error handling, and maintenance
- Enabling research and analysis through LLM integration

### 1.3 Definitions and Acronyms
- **Sitemap**: An XML file that lists URLs for a site along with metadata about each URL
- **Crawler**: A program that visits websites and reads their pages to create entries for a search engine index
- **Scraper**: A tool that extracts data from websites
- **CSS Selector**: A pattern used to select HTML elements for data extraction
- **LLM**: Large Language Model, an AI system capable of understanding and generating human-like text
- **Crawl4AI**: The web scraping framework used for efficient data extraction

## 2. Goals and Objectives

### 2.1 Primary Goal
To create a reliable, scalable, and efficient platform for collecting, processing, and analyzing Nigerian news content, utilizing Crawl4AI for robust web scraping.

### 2.2 Specific Objectives
* Automate the discovery and extraction of article URLs from 28+ news websites, accommodating diverse website structures using Crawl4AI.  
* Develop a robust scraping mechanism for extracting key article metadata using Crawl4AI.  
* Implement efficient data storage and retrieval optimized for LLM integration.  
* Create an LLM-powered interface for natural language querying.  
* Automate maintenance, monitoring, and error resolution processes.  
* Minimize resource consumption and avoid triggering anti-scraping measures.  
* Provide real-time progress tracking and a comprehensive dashboard.

## 3. System Features and Requirements

### 3.1 Functional Requirements

#### 3.1.1 Crawl4AI Integration Module
* Implement Crawl4AI for URL discovery, article extraction, and dynamic content handling.  
* Configure Crawl4AI for optimal performance and anti-scraping measures.  
* Utilize Crawl4AI's LLM schema generation for extraction.  
* Implement intelligent retry mechanisms with exponential backoff.  
* Configure proxy rotation and rate limiting.

#### 3.1.2 Sitemap Generator Module
* User-friendly interface for inputting base URLs.  
* Automated sitemap index detection and parsing using Crawl4AI.  
* Support for various sitemap index formats (e.g., post-sitemap.xml, post-sitemap-1.xml).  
* Extraction of article URLs from sitemap files using Crawl4AI.  
* URL validation and status code checking.  
* Storage of URLs in the sitemaps table with relevant metadata.  
* Logging of errors and resolution status.  
* Functionality to check for new articles based on last published date.  
* Progress bar to indicate sitemap scraping progress.  
* Ability to resume interrupted sitemap generation from the last successful point.

#### 3.1.3 Dynamic URL Discovery Module
* Category URL extraction and validation using Crawl4AI.  
* Pagination pattern identification and URL generation using Crawl4AI.  
* Storage of dynamically generated URLs in the sitemaps table.  
* Way to save progress, so if script breaks it can restart from where it stopped.  
* Progress bar to indicate category scraping progress.  
* Checkpoint system to save progress at regular intervals.

#### 3.1.4 Article Scraper Module
* User interface for inputting CSS selectors or LLM generated selectors using Crawl4AI.  
* Extraction of article metadata (title, author, publication date, categories, content) using Crawl4AI.  
* Storage of scraped articles in the articles_data table.  
* Progress tracking and status updates.  
* Error logging and recovery.  
* Progress bar to indicate article scraping progress.  
* Ability to resume interrupted scraping sessions.  
* Automatic retry mechanism for failed article extractions.

#### 3.1.5 LLM Integration Module
* Integration with a suitable LLM for natural language querying.  
* Vectorisation of article content for efficient retrieval.  
* User-friendly interface for interacting with the LLM.  
* Support for research-oriented queries (e.g., topic analysis, trend detection, comparative studies).  
* Ability to generate research summaries and insights.

#### 3.1.6 Automation and Monitoring Module
* Automated URL discovery and content updates.  
* Error detection and resolution.  
* Performance monitoring and reporting.  
* Use of n8n for workflow orchestration.  
* Automated error resolution workflows.  
* Scheduled health checks for stored URLs.

#### 3.1.7 Dashboard Module
* Display base URLs and the status of each scraping stage (category, sitemap, article).  
* Display the number of articles scraped per URL.  
* Display the number of errors and their resolution status.  
* Provide visualizations of scraping progress.  
* A way to track the steps.  
* Display live status updates for each website's article scraping process.  
* Display enhanced metrics in maintenance mode.  
* Show overall progress of each website's setup process.  
* Provide detailed breakdown of setup step status.  
* Offer detailed live status page for each website.

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance
* The system should handle scraping of 28+ websites efficiently
* URL discovery should process at least 1000 URLs per minute
* Article extraction should process at least 10 articles per minute
* Minimal resource consumption during operations

#### 3.2.2 Reliability
* The system should be able to resume operations after interruptions
* Data integrity should be maintained even during errors
* Regular backups of the database should be performed
* Robust error handling and recovery mechanisms

#### 3.2.3 Security
* The system should not store or transmit sensitive information
* Access to the system should be restricted to authorized users
* API endpoints should be secured appropriately
* Data encryption at rest and in transit

#### 3.2.4 Scalability
* The system should be able to accommodate additional websites
* The database should be designed to handle millions of articles
* Processing should be distributable across multiple servers if needed

## 4. Database Schema

### 4.1 Core Tables
* **websites table**:
  - id: Primary key
  - website_name: Name of the website
  - website_url: Base URL of the website
  - sitemap_index_url: URL of the sitemap index (if available)
  - first_archive_url: URL of the first archive page
  - last_archive_url: URL of the last archive page
  - created_at: Timestamp of creation
  - updated_at: Timestamp of last update

* **sitemaps table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - article_url: URL of the article
  - last_mod: Last modification date from sitemap
  - is_valid: Boolean indicating if URL is valid (returns 200)
  - status_code: HTTP status code of the URL
  - last_checked: Timestamp of last validation
  - retry_count: Number of retry attempts
  - last_error: Last error message if any
  - created_at: Timestamp of creation

* **categories table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - category_name: Name of the category
  - category_url: URL of the category page
  - is_valid: Boolean indicating if URL is valid
  - last_checked: Timestamp of last validation
  - created_at: Timestamp of creation

* **articles_data table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - article_id: Unique identifier for the article
  - article_title: Title of the article
  - article_category: Category of the article
  - author: Author of the article
  - article_url: URL of the article
  - pub_date: Publication date
  - created_at: Timestamp of creation
  - article_content: Compressed article content
  - scraping_status: Status of scraping (completed, pending, failed)
  - retry_count: Number of retry attempts
  - last_error: Last error message if any

* **error_logs table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - error_message: Description of the error
  - error_type: Type of error (URL discovery, article extraction, etc.)
  - created_at: Timestamp of creation
  - resolved_at: Timestamp of resolution
  - resolution_notes: Notes about how the error was resolved
  - retry_count: Number of retry attempts

* **progress_tracking table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - category_scraping_status: Boolean indicating if category scraping is complete
  - sitemap_scraping_status: Boolean indicating if sitemap scraping is complete
  - articles_scraping_status: Boolean indicating if article scraping is complete
  - current_step: Integer indicating current step in the process
  - last_checked: Timestamp of last check
  - new_articles_discovered: Number of new articles discovered
  - new_articles_added: Number of new articles added
  - last_article_added: Timestamp of last article added
  - last_check_status: String indicating status of last check
  - checkpoint_data: JSON containing checkpoint information

## 5. Technical Requirements

### 5.1 Core Technologies
* Programming Language: Python (3.9+)
* Web Scraping: Crawl4AI
* Database: PostgreSQL
* LLM: OpenAI API (or similar)
* Vector Database: Pinecone or Weaviate
* API: FastAPI or Flask
* Frontend: Next.js
* Automation: n8n
* Asynchronous tasks: Celery or asyncio
* Caching: Redis

### 5.2 Data Compression
* Implement gzip compression for article content
* Optimize storage of large text content
* Maintain quick access to compressed content

## 6. Future Considerations

### 6.1 Planned Enhancements
* Sentiment analysis of news articles
* Topic modelling and trend analysis
* Integration with social media platforms
* Image and video scraping
* Advanced research capabilities through LLM integration
* Automated research report generation

### 6.2 Research Focus
* Enhanced LLM query capabilities
* Advanced data analysis tools
* Custom research report generation
* Trend analysis and visualization