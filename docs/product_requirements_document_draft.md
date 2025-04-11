# Product Requirements Document (PRD) \- NaijaNewsHub (Crawl4AI)

**1\. Introduction**

* Project Name: NaijaNewsHub (Crawl4AI)  
* Simple Descriptor: Nigerian News Aggregation & Analysis Platform (Crawl4AI Integration)  
* Purpose: To build a robust, adaptable, and scalable system for aggregating news content from a diverse range of Nigerian online news sources, leveraging Crawl4AI for efficient web scraping, enabling data-driven research and analysis.  
* Target Audience: Researchers, analysts, journalists, and users seeking access to a consolidated source of Nigerian news.

**2\. Goals and Objectives**

* Primary Goal: To create a reliable, scalable, and efficient platform for collecting, processing, and analyzing Nigerian news content, utilizing Crawl4AI for robust web scraping.  
* Specific Objectives:  
  * Automate the discovery and extraction of article URLs from 28+ news websites, accommodating diverse website structures using Crawl4AI.  
  * Develop a robust scraping mechanism for extracting key article metadata using Crawl4AI.  
  * Implement efficient data storage and retrieval optimized for LLM integration.  
  * Create an LLM-powered interface for natural language querying.  
  * Automate maintenance, monitoring, and error resolution processes.  
  * Minimize resource consumption and avoid triggering anti-scraping measures.  
  * Provide real-time progress tracking and a comprehensive dashboard.

**3\. Functional Requirements**

* **Crawl4AI Integration Module:**  
  * Implement Crawl4AI for URL discovery, article extraction, and dynamic content handling.  
  * Configure Crawl4AI for optimal performance and anti-scraping measures.  
  * Utilize Crawl4AI’s LLM schema generation for extraction.  
* **Sitemap Generator Module:**  
  * User-friendly interface for inputting base URLs.  
  * Automated sitemap index detection and parsing using Crawl4AI.  
  * Extraction of article URLs from sitemap files using Crawl4AI.  
  * URL validation and status code checking.  
  * Storage of URLs in the sitemaps table with relevant metadata.  
  * Logging of errors and resolution status.  
  * Functionality to check for new articles based on last published date.  
  * Progress bar to indicate sitemap scraping progress.  
* **Dynamic URL Discovery Module:**  
  * Category URL extraction and validation using Crawl4AI.  
  * Pagination pattern identification and URL generation using Crawl4AI.  
  * Storage of dynamically generated URLs in the sitemaps table.  
  * Way to save progress, so if script breaks it can restart from where it stopped.  
  * Progress bar to indicate category scraping progress.  
* **Article Scraper Module:**  
  * User interface for inputting CSS selectors or LLM generated selectors using Crawl4AI.  
  * Extraction of article metadata (title, author, publication date, categories, content) using Crawl4AI.  
  * Storage of scraped articles in the articles\_data table.  
  * Progress tracking and status updates.  
  * Error logging and recovery.  
  * Progress bar to indicate article scraping progress.  
* **LLM Integration Module:**  
  * Integration with a suitable LLM for natural language querying.  
  * Vectorisation of article content for efficient retrieval.  
  * User-friendly interface for interacting with the LLM.  
* **Automation and Monitoring Module:**  
  * Automated URL discovery and content updates.  
  * Error detection and resolution.  
  * Performance monitoring and reporting.  
  * Use of n8n for workflow orchestration.  
* **Dashboard Module:**  
  * Display base URLs and the status of each scraping stage (category, sitemap, article).  
  * Display the number of articles scraped per URL.  
  * Display the number of errors and their resolution status.  
  * Provide visualizations of scraping progress.  
  * A way to track the steps.  
  * Display live status updates for each website's article scraping process, including metrics such as the total number of articles scraped, percentage completion, and estimated time remaining. When in maintenance mode, display enhanced metrics such as the number of new articles discovered, number of new articles added, percentage completion of new article scraping, last date new articles were added, last date checked for new articles, status of last check, and estimated time remaining for new article scraping.  
  * Display the overall progress of each website's setup process, showing the number of completed steps out of the total steps (e.g., '2 of 5 steps completed').  
  * Provide a detailed breakdown of each setup step's status for each website, with columns indicating 'completed' or 'pending' for each step (e.g., 'Category Scraping: completed', 'Sitemap Scraping: pending', etc.).  
  * Provide a detailed live status page for each website, accessible via a link from the dashboard, displaying all enhanced live status metrics. Allow for a quick preview of key metrics within the main dashboard view.  
* **Data Compression:**  
  * Implement data compression for article content storage.  
* **Database Schema:**  
  * websites table: id, website\_name, website\_url.  
  * sitemaps table: id, website\_id, article\_url, last\_mod, created\_at, is\_valid, last\_checked, status\_code.  
  * categories table: id, website\_id, category\_name, category\_url, created\_at.  
  * articles\_data table: id, website\_id, article\_id, article\_title, article\_category, author, article\_url, pub\_date, created\_at, article\_content.  
  * error\_logs: id, website\_id, error\_message, created\_at, resolved\_at.

**4\. Non-Functional Requirements**

* **Performance:** The system should be able to process a large volume of data efficiently, with minimal resource consumption.  
* **Scalability:** The system should be able to scale to accommodate new news sources and increasing data volumes.  
* **Reliability:** The system should be reliable and fault-tolerant, with robust error handling.  
* **Security:** The system should be secure and protect sensitive data.  
* **Maintainability:** The system should be designed for easy maintenance and updates.  
* **Anti-Scraping Compliance:** The system should avoid triggering anti-scraping measures through rate limiting, proxy usage, and adherence to robots.txt.

**5\. Technical Requirements**

* Programming Language: Python.  
* Web Scraping: Crawl4AI  
* Database: PostgreSQL or similar.  
* LLM: OpenAI API, or other suitable LLM.  
* Vector Database: Pinecone, Weaviate, etc.  
* Automation Tool: n8n.  
* Frontend: Next.js or similar.

**6\. User Interface (UI) Requirements**

* Intuitive and user-friendly interface.  
* Multi-step form for URL input and configuration.  
* Clear progress indicators and status updates.  
* LLM interaction interface.  
* Comprehensive dashboard for monitoring scraping progress and errors.  
* Display clear progress indicators for the multi-step form, showing the number of completed steps and the total number of steps (e.g., 'Step 2 of 5').

**7\. Future Considerations**

* Sentiment analysis of news articles.  
* Topic modelling and trend analysis.  
* Integration with social media platforms.  
* Image and video scraping.

**8\. Technical Design Document (Separate Document)**

* A separate technical design document will be created to detail the following:  
  * Detailed architecture and system design.  
  * Specific technologies and libraries to be used.  
  * Database schema and data storage strategies.  
  * API design and integration details.  
  * Testing strategy and test cases.  
  * Deployment and infrastructure considerations.  
  * Detailed information about rate limiting, and anti scraping avoidance.  
  * Detailed information about data compression.