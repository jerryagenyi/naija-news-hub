# News Scraper - Product Requirements Document (PRD)

## 1. Introduction

### 1.1 Purpose
This document outlines the requirements for developing a flexible and robust Nigerian news scraper that can automatically extract articles from various news websites when provided with just a base URL. The system will handle the challenges of varying website structures, sitemap formats, and article layouts across Nigerian news websites.

### 1.2 Scope
The project will create a system capable of:
- Accepting a base URL through a user-friendly interface
- Automatically discovering article URLs through various methods (sitemap parsing, category page crawling)
- Extracting article content and metadata
- Storing the data in a structured format
- Providing mechanisms for monitoring, error handling, and maintenance

### 1.3 Definitions and Acronyms
- **Sitemap**: An XML file that lists URLs for a site along with metadata about each URL
- **Crawler**: A program that visits websites and reads their pages to create entries for a search engine index
- **Scraper**: A tool that extracts data from websites
- **CSS Selector**: A pattern used to select HTML elements for data extraction
- **LLM**: Large Language Model, an AI system capable of understanding and generating human-like text

## 2. Product Overview

### 2.1 Product Perspective
The news scraper will be a standalone system that can be integrated with other applications through its database or API. It will serve as a foundation for a larger ecosystem of news aggregation, analysis, and research tools.

### 2.2 User Classes and Characteristics
- **Researchers**: Individuals who need access to Nigerian news content for analysis and research
- **Data Analysts**: Users who will process and analyze the scraped data
- **System Administrators**: Technical users who will maintain and monitor the system

### 2.3 Operating Environment
- Python-based backend
- Database system for storing article data and metadata
- Web-based frontend for user interaction
- Automated scheduling system for regular updates

### 2.4 Design and Implementation Constraints
- Must respect website terms of service and ethical scraping practices
- Must handle varying website structures across 28+ Nigerian news sites
- Must be resilient to website changes and errors
- Must minimize server load on target websites

### 2.5 Assumptions and Dependencies
- Target websites will remain accessible
- Basic structure of news articles will remain consistent enough for extraction
- System will have sufficient resources for processing and storage

## 3. System Features and Requirements

### 3.1 Functional Requirements

#### 3.1.1 URL Discovery and Sitemap Generation
- **Multi-step Form Interface**:
  - Accept a base URL input
  - Validate the URL and check accessibility
  - Guide users through the setup process with clear steps
  - Provide feedback on progress and success/failure

- **Sitemap-based URL Discovery**:
  - Automatically detect and parse sitemap index files
  - Extract article URLs from sitemaps
  - Validate extracted URLs (check for 200 status code)
  - Store valid URLs in the database
  - Track the first and last archive URL for future updates

- **Category-based URL Discovery**:
  - For websites without accessible sitemaps, detect category pages
  - Extract category URLs and validate them
  - Navigate pagination to discover article URLs
  - Store discovered URLs in the database
  - Track pagination patterns for future updates

#### 3.1.2 Article Extraction
- **Content Extraction**:
  - Extract article title, author, publication date, categories, and content
  - Support manual input of CSS selectors for extraction
  - Optionally use LLM to automatically detect appropriate selectors
  - Handle various HTML structures and formats
  - Clean and normalize extracted content

- **Data Storage**:
  - Store extracted articles in a structured database
  - Maintain relationships between articles, categories, and websites
  - Track extraction status and errors

#### 3.1.3 Maintenance and Updates
- **Automated Updates**:
  - Regularly check for new articles based on last publication date
  - Update the database with new content
  - Track update status and progress

- **Error Handling and Recovery**:
  - Log errors during URL discovery and article extraction
  - Provide mechanisms for resolving errors
  - Support resuming operations after interruptions

#### 3.1.4 Monitoring and Reporting
- **Dashboard Interface**:
  - Display scraping progress and status for each website
  - Show error counts and resolution status
  - Provide metrics on article counts and categories
  - Display live status updates during scraping operations

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance
- The system should handle scraping of 28+ websites efficiently
- URL discovery should process at least 1000 URLs per minute
- Article extraction should process at least 10 articles per minute

#### 3.2.2 Reliability
- The system should be able to resume operations after interruptions
- Data integrity should be maintained even during errors
- Regular backups of the database should be performed

#### 3.2.3 Security
- The system should not store or transmit sensitive information
- Access to the system should be restricted to authorized users
- API endpoints should be secured appropriately

#### 3.2.4 Scalability
- The system should be able to accommodate additional websites
- The database should be designed to handle millions of articles
- Processing should be distributable across multiple servers if needed

## 4. External Interface Requirements

### 4.1 User Interfaces
- **Multi-step Form**:
  - Clean, intuitive interface for entering base URLs
  - Clear progress indicators for multi-step processes
  - Feedback on success/failure of operations

- **Dashboard**:
  - Overview of all websites and their scraping status
  - Detailed view of scraping progress for each website
  - Error logs and resolution status
  - Metrics and statistics on scraped content

### 4.2 Software Interfaces
- **Database**:
  - Store website information, URLs, categories, and articles
  - Support efficient querying and updates
  - Maintain data integrity and relationships

- **Web Scraping Libraries**:
  - Interface with HTTP clients for fetching content
  - Parse HTML and extract data using selectors
  - Handle various content formats and structures

- **Scheduling System**:
  - Automate regular checks for new content
  - Manage periodic maintenance tasks

## 5. Other Requirements

### 5.1 Database Schema
- **websites table**:
  - id: Primary key
  - website_name: Name of the website
  - website_url: Base URL of the website
  - sitemap_index_url: URL of the sitemap index (if available)
  - first_archive_url: URL of the first archive page
  - last_archive_url: URL of the last archive page
  - sitemap_status: Status of sitemap generation (completed, pending, failed)
  - article_status: Status of article extraction (completed, pending, failed)
  - created_at: Timestamp of creation
  - updated_at: Timestamp of last update

- **sitemaps table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - article_url: URL of the article
  - last_mod: Last modification date from sitemap
  - is_valid: Boolean indicating if URL is valid (returns 200)
  - status_code: HTTP status code of the URL
  - last_checked: Timestamp of last validation
  - created_at: Timestamp of creation

- **categories table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - category_name: Name of the category
  - category_url: URL of the category page
  - created_at: Timestamp of creation

- **articles table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - article_url: URL of the article
  - title: Article title
  - author: Article author
  - publication_date: Date of publication
  - content: Article content
  - categories: Array of category IDs
  - extraction_status: Status of extraction (completed, pending, failed)
  - created_at: Timestamp of creation
  - updated_at: Timestamp of last update

- **error_logs table**:
  - id: Primary key
  - website_id: Foreign key to websites table
  - error_message: Description of the error
  - error_type: Type of error (URL discovery, article extraction, etc.)
  - resolved: Boolean indicating if error is resolved
  - created_at: Timestamp of creation
  - resolved_at: Timestamp of resolution

### 5.2 Future Considerations
1. **LLM Integration**:
   - Vectorize article content for LLM consumption
   - Develop an interface for querying the LLM about article content
   - Enable natural language research and analysis

2. **Advanced Analytics**:
   - Implement sentiment analysis on article content
   - Track trends and topics across news sources
   - Generate reports and visualizations

3. **API Access**:
   - Provide API endpoints for accessing scraped content
   - Enable integration with other systems and applications

## 6. Appendices

### 6.1 Development Phases
1. **Phase 1: URL Discovery and Sitemap Generation**
   - Implement base URL input and validation
   - Develop sitemap parsing functionality
   - Create category-based URL discovery as fallback
   - Set up database schema and storage

2. **Phase 2: Article Extraction**
   - Implement CSS selector-based extraction
   - Develop content cleaning and normalization
   - Create storage and tracking mechanisms
   - Implement error handling and logging

3. **Phase 3: Maintenance and Monitoring**
   - Develop dashboard for monitoring progress
   - Implement automated updates and checks
   - Create error resolution workflows
   - Set up regular maintenance tasks

4. **Phase 4: LLM Integration (Future)**
   - Implement content vectorization
   - Integrate with LLM API
   - Develop query interface
   - Create research and analysis tools
