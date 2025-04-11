# Technical Design Document (TDD) \- NaijaNewsHub (Crawl4AI)

**1\. Introduction**

* Document Purpose: To outline the technical architecture, design decisions, and implementation details for the NaijaNewsHub project.  
* Audience: Developers, system administrators, and technical stakeholders.

**2\. System Architecture**

* **Modular Design:** The system will be designed with a modular architecture to facilitate maintainability and scalability  
* **Components:**  
  * **Crawl4AI Module:** Handles all web scraping functionalities.  
  * **Data Processing Module:** Handles data cleaning, normalization, and compression.  
  * **Data Storage Module:** Manages data storage and retrieval.  
  * **LLM Integration Module:** Handles communication with the LLM and vector database.  
  * **API Module:** Provides an API for accessing scraped data and LLM functionality.  
  * **Frontend Module:** Implements the user interface.  
  * **Automation Module:** Handles the automation of the scraping process  
* **Technology Stack:**  
  * **Programming Language:** Python (3.9+)  
  * **Web Scraping:** Crawl4AI  
  * **Database:** PostgreSQL  
  * **LLM:** OpenAI API (or similar)  
  * **Vector Database:** Pinecone or Weaviate  
  * **API:** FastAPI or Flask  
  * **Frontend:** Next.js  
  * **Automation:** n8n  
  * **Asynchronous tasks:** Celery, or asyncio.  
  * **Caching:** Redis.

**3\. Crawl4AI Integration Module**

* **URL Discovery:**  
  * Utilize Crawl4AI's asynchronous capabilities for efficient URL discovery.  
  * Configure Crawl4AI for sitemap parsing and dynamic URL generation.  
  * Utilize Crawl4Ai's ability to handle javascript rendered pages.  
* **Article Extraction:**  
  * Implement Crawl4AI's CSS and LLM-based extraction strategies.  
  * Configure Crawl4AI for optimal data extraction and normalization.  
  * Utilize Crawl4AI’s schema generation.  
  * Configure Crawl4AI’s proxy and anti scraping avoidance features.  
* **Data Processing:**  
  * Utilize Crawl4AI’s markdown generation.  
  * Data cleaning and normalization using regular expressions and string manipulation.  
  * Data compression using gzip.  
  * Implement a process that checks the last published date of the most recent article, and compares that to the current date, to discover new articles.

**4\. Data Storage Module**

* **Database Schema (PostgreSQL):**  
  * websites table: id, website\_name, website\_url  
  * sitemaps table: id, website\_id, article\_url, last\_mod, created\_at, is\_valid, last\_checked, status\_code  
  * categories table: id, website\_id, category\_name, category\_url, created\_at  
  * articles\_data table: id, website\_id, article\_id, article\_title, article\_category, author, article\_url, pub\_date, created\_at, article\_content  
  * error\_logs: id, website\_id, error\_message, created\_at, resolved\_at  
  * progress\_tracking: id, website\_id, category\_scraping\_status (Boolean), sitemap\_scraping\_status (Boolean), articles\_scraping\_status (Boolean), current\_step (Integer), last\_checked (Timestamp), new\_articles\_discovered (Integer), new\_articles\_added (Integer), last\_article\_added (Timestamp), last\_check\_status (String).  
* **Vector Database (Pinecone/Weaviate):**  
  * Storage of article embeddings for LLM retrieval.

**5\. LLM Integration Module**

* **LLM API Interaction:**  
  * Communication with the LLM API for natural language queries.  
  * Vector search in the vector database.  
* **Data Vectorization:**  
  * Embedding generation for article content.

**6\. API Module**

* **API Endpoints:**  
  * Endpoints for accessing scraped articles.  
  * Endpoints for LLM queries.  
  * Endpoints for dashboard data.  
* **Authentication and Authorization:**  
  * API key-based authentication.

**7\. Frontend Module**

* **UI Components:**  
  * Multi-step form for URL input and configuration.  
  * Dashboard for monitoring scraping progress and errors.  
  * LLM interaction interface.  
  * Progress bars for scraping stages.  
  * Implement real-time updates for the dashboard, displaying the progress of each website's setup and scraping processes.  
  * Create a dedicated live status page for each website, accessible via a link from the dashboard, displaying enhanced live status metrics.  
  * Implement a quick preview of key live status metrics within the main dashboard view.  
* **Technology:**  
  * Next.js for server-side rendering and performance.

**8\. Automation Module**

* **n8n Workflows:**  
  * Automated URL discovery and content updates.  
  * Error detection and resolution.  
  * Scheduled tasks for monitoring and maintenance.  
  * Implement a scheduled task to check for new articles, update the database and dashboard accordingly, and log the results of each check.  
* **Monitoring and Logging:**  
  * Real-time monitoring of scraping processes.  
  * Comprehensive error logging and reporting.

**9\. Data Flow**

* User input via the frontend triggers URL discovery and scraping using Crawl4AI.  
* Scraped data is processed and stored in the database and vector database.  
* User queries via the frontend are sent to the LLM API.  
* LLM responses are displayed in the frontend.

**10\. Testing**

* Unit tests for individual modules.  
* Integration tests for system components.  
* End-to-end tests for user workflows.  
* Performance testing to ensure scalability.  
* Testing for anti scraping avoidance.

**11\. Deployment**

* Cloud-based deployment (AWS, Google Cloud, or Azure).  
* Containerization using Docker.  
* Orchestration using Kubernetes.

**12\. Security**

* Secure API endpoints.  
* Data encryption at rest and in transit.  
* Regular security audits.

**13\. Maintenance**

* Automated monitoring and alerting.  
* Regular backups and disaster recovery.  
* Version control using Git.

