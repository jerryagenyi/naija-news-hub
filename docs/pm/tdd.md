# Technical Design Document (TDD) - NaijaNewsHub (Crawl4AI)

**1. Introduction**

* Document Purpose: To outline the technical architecture, design decisions, and implementation details for the NaijaNewsHub project.
* Audience: Developers, system administrators, and technical stakeholders.
* Project Purpose: The system is designed to aggregate news content for LLM training and research purposes, not as a public-facing news browsing platform. The scraped articles will be vectorized and used to train an LLM for a chat interface.

**2. System Architecture**

* **Modular Design:** The system is designed with a modular architecture to facilitate maintainability and scalability
* **Components:**
  * **API Endpoints (`src/api_endpoints/`):** Handles all HTTP endpoints and request/response handling
  * **Database Management (`src/database_management/`):** Manages data persistence and database operations
  * **Service Layer (`src/service_layer/`):** Implements business logic and coordinates between components
  * **Web Scraper (`src/web_scraper/`):** Handles web scraping and content extraction
  * **Utility Modules (`src/utility_modules/`):** Provides shared utilities and helper functions
  * **Test Suite (`src/test_suite/`):** Contains all test files and testing utilities
  * **Configuration (`src/configuration/`):** Manages application configuration
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

**3. Crawl4AI Integration Module**

* **URL Discovery:**
  * Utilize Crawl4AI's asynchronous capabilities for efficient URL discovery.
  * Configure Crawl4AI for sitemap parsing and dynamic URL generation.
  * Utilize Crawl4Ai's ability to handle javascript rendered pages.
  * Implement intelligent retry mechanisms with exponential backoff.
  * Configure proxy rotation and rate limiting.
* **Article Extraction:**
  * Implement Crawl4AI's CSS and LLM-based extraction strategies.
  * Configure Crawl4AI for optimal data extraction and normalization.
  * Utilize Crawl4AI's schema generation.
  * Configure Crawl4AI's proxy and anti scraping avoidance features.
  * Implement checkpointing for long-running extraction tasks.
* **Data Processing:**
  * Utilize Crawl4AI's markdown generation.
  * Data cleaning and normalization using regular expressions and string manipulation.
  * Data compression using gzip.
  * Implement a process that checks the last published date of the most recent article, and compares that to the current date, to discover new articles.
  * Implement data validation and sanitization.

**4. Data Storage Module**

* **Database Schema (PostgreSQL):**
  * **websites table**: id (SERIAL PRIMARY KEY), website_name (VARCHAR NOT NULL), website_url (VARCHAR NOT NULL UNIQUE), sitemap_index_url (VARCHAR), first_archive_url (VARCHAR), last_archive_url (VARCHAR), created_at (TIMESTAMP DEFAULT NOW()), updated_at (TIMESTAMP)
  * **sitemaps table**: id (SERIAL PRIMARY KEY), website_id (INTEGER REFERENCES websites), article_url (VARCHAR NOT NULL UNIQUE), last_mod (TIMESTAMP), created_at (TIMESTAMP DEFAULT NOW()), is_valid (BOOLEAN), last_checked (TIMESTAMP), status_code (INTEGER), retry_count (INTEGER DEFAULT 0), last_error (TEXT)
  * **categories table**: id (SERIAL PRIMARY KEY), website_id (INTEGER REFERENCES websites), category_name (VARCHAR NOT NULL), category_url (VARCHAR NOT NULL), created_at (TIMESTAMP DEFAULT NOW()), is_valid (BOOLEAN), last_checked (TIMESTAMP), UNIQUE(website_id, category_name)
  * **articles_data table**: id (SERIAL PRIMARY KEY), website_id (INTEGER REFERENCES websites), article_id (VARCHAR NOT NULL UNIQUE), article_title (TEXT NOT NULL), article_category (INTEGER REFERENCES categories), author (TEXT), article_url (TEXT NOT NULL), pub_date (TIMESTAMP), created_at (TIMESTAMP DEFAULT NOW()), article_content (TEXT), scraping_status (VARCHAR DEFAULT 'pending'), retry_count (INTEGER DEFAULT 0), last_error (TEXT)
  * **error_logs table**: id (SERIAL PRIMARY KEY), website_id (INTEGER REFERENCES websites), error_message (TEXT NOT NULL), error_type (VARCHAR NOT NULL), created_at (TIMESTAMP DEFAULT NOW()), resolved_at (TIMESTAMP), resolution_notes (TEXT), retry_count (INTEGER DEFAULT 0)
  * **progress_tracking table**: id (SERIAL PRIMARY KEY), website_id (INTEGER REFERENCES websites UNIQUE), category_scraping_status (BOOLEAN DEFAULT FALSE), sitemap_scraping_status (BOOLEAN DEFAULT FALSE), articles_scraping_status (BOOLEAN DEFAULT FALSE), current_step (INTEGER DEFAULT 0), last_checked (TIMESTAMP), new_articles_discovered (INTEGER DEFAULT 0), new_articles_added (INTEGER DEFAULT 0), last_article_added (TIMESTAMP), last_check_status (VARCHAR), checkpoint_data (JSONB)
  * **See full schema details in [Database Schema Documentation](../dev/database-schema.md)**
* **Vector Database (Pinecone/Weaviate):**
  * Storage of article embeddings for LLM retrieval.
  * Indexing strategy for efficient research queries.
  * Metadata storage for enhanced search capabilities.

**5. LLM Integration Module**

* **LLM API Interaction:**
  * Communication with the LLM API for natural language queries.
  * Vector search in the vector database.
  * Research-focused query processing.
  * Automated report generation.
* **Data Vectorization:**
  * Embedding generation for article content.
  * Metadata embedding for enhanced search.
  * Batch processing for efficiency.

**6. API Module**

* **API Endpoints:**
  * Endpoints for accessing scraped articles.
  * Endpoints for LLM queries.
  * Endpoints for dashboard data.
  * Research-specific endpoints.
* **Authentication and Authorization:**
  * API key-based authentication.
  * Role-based access control.

**7. Frontend Module**

* **UI Components:**
  * Multi-step form for URL input and configuration.
  * Dashboard for monitoring scraping progress and errors.
  * LLM interaction interface.
  * Progress bars for scraping stages.
  * Implement real-time updates for the dashboard, displaying the progress of each website's setup and scraping processes.
  * Create a dedicated live status page for each website, accessible via a link from the dashboard, displaying enhanced live status metrics.
  * Implement a quick preview of key live status metrics within the main dashboard view.
  * Research-focused interface components.
* **Technology:**
  * Next.js for server-side rendering and performance.
  * Real-time updates using WebSocket.

**8. Automation Module**

* **n8n Workflows:**
  * Automated URL discovery and content updates.
  * Error detection and resolution.
  * Scheduled tasks for monitoring and maintenance.
  * Implement a scheduled task to check for new articles, update the database and dashboard accordingly, and log the results of each check.
  * Automated error resolution workflows.
  * Health check monitoring.
* **Monitoring and Logging:**
  * Real-time monitoring of scraping processes.
  * Comprehensive error logging and reporting.
  * Performance metrics collection.

**9. Data Flow**

* User input via the frontend triggers URL discovery and scraping using Crawl4AI.
* Scraped data is processed and stored in the database and vector database.
* User queries via the frontend are sent to the LLM API.
* LLM responses are displayed in the frontend.
* Research queries are processed through the vector database.
* Automated workflows maintain data freshness and resolve errors.

**10. Testing**

* Unit tests for individual modules.
* Integration tests for system components.
* End-to-end tests for user workflows.
* Performance testing to ensure scalability.
* Testing for anti scraping avoidance.
* Error handling and recovery testing.
* Checkpoint and resume testing.

**11. Deployment**

* Cloud-based deployment (AWS, Google Cloud, or Azure).
* Containerization using Docker.
* Orchestration using Kubernetes.
* Automated deployment pipelines.
* Monitoring and alerting setup.

**12. Security**

* Secure API endpoints.
* Data encryption at rest and in transit.
* Regular security audits.
* Rate limiting and DDoS protection.
* Secure storage of API keys and credentials.

**13. Maintenance**

* Automated monitoring and alerting.
* Regular backups and disaster recovery.
* Version control using Git.
* Automated health checks.
* Performance optimization routines.