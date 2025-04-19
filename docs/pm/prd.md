# Naija News Hub - Product Requirements Document (PRD)

## 1. Introduction

### 1.1 Project Overview
* Project Name: NaijaNewsHub (Crawl4AI)
* Simple Descriptor: Nigerian News Aggregation & Analysis Platform (Crawl4AI Integration)
* Purpose: To build a robust, adaptable, and scalable system for aggregating news content from a diverse range of Nigerian online news sources, leveraging Crawl4AI for efficient web scraping, enabling data-driven research and analysis. The primary purpose of this platform is to collect news articles that will be vectorized and used to train an LLM for a chat interface, not for direct browsing by end users.
* Target Audience: Researchers, analysts, journalists, and users seeking access to a consolidated source of Nigerian news for research and analysis purposes.

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
* Automate the discovery and extraction of article URLs from 28+ news websites, accommodating diverse website structures using Crawl4AI
* Develop a robust scraping mechanism for extracting key article metadata using Crawl4AI
* Implement efficient data storage and retrieval optimized for LLM integration
* Create an LLM-powered interface for natural language querying
* Automate maintenance, monitoring, and error resolution processes
* Minimize resource consumption and avoid triggering anti-scraping measures
* Provide real-time progress tracking and a comprehensive dashboard

## 3. Functional Requirements

### 3.1 AI Agent Integration Module
- Implement a multi-agent system with specialized roles for different scraping tasks
- Configure agents using OpenAI Agents SDK with GPT-4o and GPT-4o-mini models
- Integrate agents with Crawl4AI for web scraping capabilities
- Implement agent communication and workflow orchestration
- Provide agent monitoring and error handling

### 3.2 Crawl4AI Integration Module
- Implement Crawl4AI for URL discovery, article extraction, and dynamic content handling
- Configure Crawl4AI for optimal performance and anti-scraping measures
- Utilize Crawl4AI's LLM schema generation for extraction

### 3.3 Sitemap Generator Module
- User-friendly interface for inputting base URLs
- Automated sitemap index detection and parsing using Crawl4AI
- Extraction of article URLs from sitemap files using Crawl4AI
- URL validation and status code checking
- Storage of URLs in the sitemaps table with relevant metadata
- Logging of errors and resolution status
- Functionality to check for new articles based on last published date
- Progress bar to indicate sitemap scraping progress

### 3.4 Dynamic URL Discovery Module
- Category URL extraction and validation using Crawl4AI
- Pagination pattern identification and URL generation using Crawl4AI
- Storage of dynamically generated URLs in the sitemaps table
- Way to save progress, so if script breaks it can restart from where it stopped
- Progress bar to indicate category scraping progress

### 3.5 Article Scraper Module
- User interface for inputting CSS selectors or LLM generated selectors using Crawl4AI
- Extraction of article metadata (title, author, publication date, categories, content) using Crawl4AI
- Storage of scraped articles in the articles_data table
- Progress tracking and status updates
- Error logging and recovery
- Progress bar to indicate article scraping progress

### 3.6 LLM Integration Module
- Integration with a suitable LLM for natural language querying
- Vectorisation of article content for efficient retrieval
- User-friendly interface for interacting with the LLM

### 3.7 Automation and Monitoring Module
- Automated URL discovery and content updates
- Error detection and resolution
- Performance monitoring and reporting
- Use of n8n for workflow orchestration

### 3.8 Dashboard Module
- Display base URLs and the status of each scraping stage (category, sitemap, article)
- Display the number of articles scraped per URL
- Display the number of errors and their resolution status
- Provide visualizations of scraping progress
- A way to track the steps
- Display live status updates for each website's article scraping process, including metrics such as:
  - Total number of articles scraped
  - Percentage completion
  - Estimated time remaining
  - Enhanced metrics in maintenance mode:
    - Number of new articles discovered
    - Number of new articles added
    - Percentage completion of new article scraping
    - Last date new articles were added
    - Last date checked for new articles
    - Status of last check
    - Estimated time remaining for new article scraping
- Display the overall progress of each website's setup process
- Provide a detailed breakdown of each setup step's status
- Provide a detailed live status page for each website

### 3.9 Data Compression
- Implement data compression for article content storage

### 3.10 Database Schema
- websites table: id, website_name, website_url
- sitemaps table: id, website_id, article_url, last_mod, created_at, is_valid, last_checked, status_code
- categories table: id, website_id, category_name, category_url, created_at
- articles_data table: id, website_id, article_id, article_title, article_category, author, article_url, pub_date, created_at, article_content
- error_logs: id, website_id, error_message, created_at, resolved_at

## 4. Non-Functional Requirements
- Performance: The system should be able to process a large volume of data efficiently, with minimal resource consumption
- Scalability: The system should be able to scale to accommodate new news sources and increasing data volumes
- Reliability: The system should be reliable and fault-tolerant, with robust error handling
- Security: The system should be secure and protect sensitive data
- Maintainability: The system should be designed for easy maintenance and updates
- Anti-Scraping Compliance: The system should avoid triggering anti-scraping measures through rate limiting, proxy usage, and adherence to robots.txt

## 5. Technical Requirements
- Programming Language: Python
- AI Agents: OpenAI Agents SDK with GPT-4o and GPT-4o-mini models
- Web Scraping: Crawl4AI
- Database: PostgreSQL or similar
- LLM: OpenAI API, or other suitable LLM
- Vector Database: Pinecone, Weaviate, etc.
- Automation Tool: n8n
- Frontend: Next.js or similar

## 6. User Interface (UI) Requirements
- Intuitive and user-friendly interface
- Multi-step form for URL input and configuration
- Clear progress indicators and status updates
- LLM interaction interface
- Comprehensive dashboard for monitoring scraping progress and errors
- Display clear progress indicators for the multi-step form, showing the number of completed steps and the total number of steps (e.g., 'Step 2 of 5')

## 7. Future Considerations
- Sentiment analysis of news articles
- Topic modelling and trend analysis
- Integration with social media platforms
- Image and video scraping

## 8. Technical Design Document (Separate Document)
A separate technical design document will be created to detail the following:
- Detailed architecture and system design
- Specific technologies and libraries to be used
- Database schema and data storage strategies
- API design and integration details
- Testing strategy and test cases
- Deployment and infrastructure considerations
- Detailed information about rate limiting, and anti scraping avoidance
- Detailed information about data compression