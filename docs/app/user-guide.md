# Naija News Hub - User Guide

**Last Updated:** 2024-04-16

*This guide is being actively developed as the project progresses. Some sections are now complete while others are still in development.*

## Table of Contents

### 1. Getting Started
- [ ] System Requirements
  - Hardware requirements
  - Software dependencies
  - Network requirements
  - Browser compatibility

- [ ] Installation
  - Local installation
  - Docker installation
  - Cloud deployment
  - Environment setup

- [ ] Initial Configuration
  - Environment variables
  - Database setup
  - API configuration
  - Security settings

### 2. Core Features

#### 2.1 Website Management
- [x] Adding News Sources
  - Base URL configuration: Enter the main URL of the news website (e.g., https://punchng.com).
  - Website name: Provide a descriptive name for the news source.
  - Status control: Set the website as active or inactive.

  To add a new website:
  1. Navigate to the Websites page from the dashboard sidebar
  2. Click the "Add Website" button in the top-right corner
  3. Fill in the required information in the modal form
  4. Click "Add Website" to save

- [x] Managing Sources
  - Viewing active sources: The Websites page displays all configured news sources with their status.
  - Updating source settings: Edit website details by clicking the edit icon.
  - Activating/deactivating sources: Toggle the status of a website using the play/pause button.
  - Starting scraping: Initiate scraping for a specific website using the refresh icon.
  - Deleting sources: Remove a website from the system using the delete icon (use with caution).

#### 2.2 Jobs Management
- [x] Viewing Jobs
  - Jobs listing: The Jobs page displays all scraping jobs with their status, progress, and other details.
  - Filtering: Filter jobs by status (All, Running, Paused, Completed, Failed) using the filter buttons.
  - Progress tracking: Monitor the progress of each job with a visual progress bar.
  - Article statistics: View the number of articles found and processed for each job.

  To access the Jobs page:
  1. Navigate to the Jobs page from the dashboard sidebar
  2. View all jobs or filter by status
  3. Monitor progress and statistics

- [x] Controlling Jobs
  - Starting jobs: Start a new scraping job from the Websites page.
  - Pausing jobs: Pause a running job by clicking the pause button.
  - Resuming jobs: Resume a paused job by clicking the play button.
  - Stopping jobs: Stop a job completely by clicking the stop button.
  - Restarting jobs: Restart a completed or failed job by clicking the refresh button.

#### 2.3 Article Management
- [ ] Viewing Articles
  - Article listing
  - Search functionality
  - Filtering options
  - Sorting options

- [ ] Article Details
  - Full content view
  - Metadata display
  - Source information
  - Related articles

#### 2.3 API Usage
- [ ] Authentication
  - API key generation
  - Token management
  - Access control
  - Security best practices

- [ ] Endpoints
  - Article endpoints
  - Source endpoints
  - Search endpoints
  - Analytics endpoints

- [ ] Rate Limiting
  - Understanding limits
  - Monitoring usage
  - Best practices
  - Error handling

### 3. Advanced Features

#### 3.1 Research Tools
- [ ] LLM Integration
  - Setting up LLM access
  - Query formulation
  - Result interpretation
  - Best practices

- [ ] Vector Search
  - Understanding vector search
  - Query optimization
  - Result relevance
  - Performance tuning

#### 3.2 Analytics
- [x] Dashboard
  - Overview metrics: The dashboard provides key metrics including total articles, active websites, running jobs, and recent errors.
  - Source statistics: View statistics for each news source including article count and status.
  - Job monitoring: Monitor the progress of scraping jobs with real-time updates.
  - Error tracking: Track and manage errors that occur during scraping operations.

  The dashboard is organized into several key sections:

  1. **Stats Cards**: Shows high-level metrics with trend indicators
  2. **Active Jobs**: Displays currently running scraping jobs with progress bars
  3. **Recent Errors**: Shows the most recent errors with details
  4. **Websites Management**: Allows adding, editing, and controlling scraping for websites

  You can access the dashboard at `/dashboard` after logging in.

- [ ] Reports
  - Generating reports
  - Customizing reports
  - Exporting data
  - Scheduled reports

### 4. Administration

#### 4.1 System Management
- [ ] Configuration
  - System settings
  - Database configuration
  - Cache management
  - Logging settings

- [ ] Monitoring
  - System health
  - Performance metrics
  - Error tracking
  - Alert configuration

#### 4.2 Security
- [ ] Access Control
  - User management
  - Role configuration
  - Permission settings
  - Audit logging

- [ ] Data Protection
  - Backup procedures
  - Data encryption
  - Security policies
  - Compliance

### 5. Troubleshooting

#### 5.1 Common Issues
- [x] Installation Problems
  - Dependency issues: Ensure all required packages are installed using `npm install` for the frontend and `pip install -r requirements.txt` for the backend.
  - Configuration errors: Verify that your `.env` file contains all required environment variables as specified in `.env.example`.
  - Network problems: Check your network connection and firewall settings if you're having trouble connecting to the API.
  - Permission issues: Ensure you have the necessary permissions to write to the database and file system.

- [x] Operational Issues
  - Scraping errors: Common scraping errors include network timeouts, parsing failures, and rate limiting. Check the Jobs page for specific error messages.
  - API problems: If the API is not responding, check the server logs and ensure the API service is running.
  - Performance issues: If the dashboard is slow, try reducing the number of concurrent scraping jobs.
  - Data inconsistencies: If you notice missing or incorrect data, check the error logs and consider re-scraping the affected websites.

#### 5.2 Maintenance
- [ ] Regular Maintenance
  - Database maintenance
  - Cache clearing
  - Log rotation
  - System updates

- [ ] Emergency Procedures
  - System recovery
  - Data restoration
  - Incident response
  - Contact information

### 6. Best Practices

#### 6.1 Performance
- [ ] Optimization
  - Query optimization
  - Cache utilization
  - Resource management
  - Scaling strategies

#### 6.2 Security
- [ ] Security Guidelines
  - API security
  - Data protection
  - Access control
  - Compliance

#### 6.3 Data Management
- [ ] Data Handling
  - Data retention
  - Backup strategies
  - Data validation
  - Quality assurance

### 7. API Reference

#### 7.1 Authentication
- [ ] Authentication Methods
  - API key authentication
  - Token-based authentication
  - OAuth integration
  - Security headers

#### 7.2 Endpoints
- [ ] Article Endpoints
  - GET /articles
  - GET /articles/{id}
  - POST /articles/search
  - GET /articles/sources

- [ ] Source Endpoints
  - GET /sources
  - POST /sources
  - PUT /sources/{id}
  - DELETE /sources/{id}

- [ ] Analytics Endpoints
  - GET /analytics/overview
  - GET /analytics/sources
  - GET /analytics/articles
  - POST /analytics/reports

#### 7.3 Error Handling
- [ ] Error Codes
  - HTTP status codes
  - Error messages
  - Error responses
  - Troubleshooting

### 8. Glossary
- [ ] Terms and Definitions
  - Technical terms
  - Business terms
  - Acronyms
  - Concepts

## Version History

### 0.2.0 - April 2024
- Added dashboard documentation
- Added website management documentation
- Added jobs management documentation
- Updated troubleshooting section
- Added API documentation for dashboard endpoints

### 0.1.0 - March 2024
- Initial creation of user guide template
- Outline of required sections
- Based on PRD and TDD requirements