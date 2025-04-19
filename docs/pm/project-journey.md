# The Naija News Hub Journey: From Concept to Structure

**Last Updated:** May 16, 2025

> **Note:** This document is updated regularly as the project evolves. The date above indicates when this document was last updated. Always check this date to determine if you need to review recent commits for additional developments.

## Introduction

In early 2025, I embarked on an ambitious project to solve a significant challenge in Nigerian news aggregation: the inconsistent and often inaccessible nature of news website structures. This blog post chronicles the journey of Naija News Hub from its initial concept to its current structured state.

## The Genesis: Identifying the Problem

The project began with a clear observation: Nigerian news websites, while rich in content, present unique technical challenges:

- Varying URL structures and formats
- Inconsistent sitemap implementations
- Dynamic article listings instead of traditional pagination
- Diverse website architectures
- Limited API access

These challenges made it difficult to create a reliable news aggregation system that could consistently and efficiently gather content from multiple sources.

## The Vision: Naija News Hub

The solution emerged as Naija News Hub - a sophisticated web scraping and news aggregation system designed to:

1. Automatically discover and validate article URLs
2. Handle diverse website structures
3. Extract and normalize article content
4. Provide a robust API for data access
5. Offer advanced features like LLM integration for research

It's important to note that Naija News Hub is not a public-facing news browsing platform. Rather, it's a data collection and analysis tool designed to aggregate news content that will be vectorized and used to train an LLM for a chat interface. The dashboard is for managing scraping, logging, and errors - not for browsing articles.

## The Development Journey

### Phase 1: Documentation and Planning (February 2025)

The project started with comprehensive documentation:

1. **Product Requirements Document (PRD)**
   - Detailed system requirements
   - Feature specifications
   - Technical requirements
   - Future considerations

2. **Technical Design Document (TDD)**
   - System architecture
   - Component design
   - Database schema
   - API specifications

3. **Testing Checklist**
   - Unit testing requirements
   - Integration testing needs
   - Performance benchmarks
   - Security considerations

### Phase 2: Project Structure (March 2025)

With the documentation in place, we established a robust project structure:

1. **Development Standards**
   - Python and TypeScript coding standards
   - Git workflow
   - Testing procedures
   - Documentation requirements

2. **Project Management Framework**
   - Task organization (Epics, Stories, Tasks)
   - Milestone planning
   - Progress tracking
   - Regular review processes

3. **Technical Infrastructure**
   - Directory structure
   - Configuration management
   - Environment setup
   - Deployment pipeline

## Key Decisions and Innovations

1. **Crawl4AI Integration**
   - Leveraging AsyncWebCrawler for efficient web scraping
   - Implementing intelligent URL discovery with pattern matching
   - Handling dynamic content and JavaScript-rendered pages
   - Extracting article content with HTML cleaning and markdown conversion
   - Implementing error handling and fallback mechanisms
   - Using rate limiting and proxy rotation to avoid blocking

2. **Modular Architecture**
   - Separating concerns into distinct components
   - Creating reusable utilities
   - Ensuring scalability

3. **Comprehensive Testing**
   - Unit testing for all components
   - Integration testing for workflows
   - Performance testing for scalability

4. **Documentation-First Approach**
   - Clear documentation standards
   - Regular updates
   - Version control for documentation

## Current Status and Next Steps

As of April 2025, Naija News Hub has:

1. **Completed**
   - Comprehensive project documentation
   - Development standards
   - Project structure
   - Testing framework
   - Initial setup implementation
   - Development environment configuration
   - Basic infrastructure setup
   - Database models and connection
   - Core scraper components with Crawl4AI integration
   - URL discovery and article extraction
   - Database integration with repository pattern
   - Article storage and retrieval
   - Command-line interface for database operations
   - API structure and routes
   - Unit tests for core components
   - Error handling and recovery mechanisms

2. **In Progress**
   - Content extraction refinement
   - API refinement and security
   - Article update mechanism
   - Content versioning implementation
   - Article deduplication

3. **Next Steps**
   - Frontend development
   - Dashboard for monitoring
   - LLM integration
   - Vector database implementation
   - Advanced feature integration
   - Automated URL discovery and content updates
   - Error notification system

## Development Timeline

### April 11-12, 2025

- Initial project setup with basic scraper functionality
- Created comprehensive Product Requirements Document (PRD)
- Renamed documentation files to use more descriptive names
- Refined original concept document for better readability
- Cleaned up duplicate documentation files
- Added comprehensive PRD, TDD, and testing checklist
- Removed old scraper implementation files
- Added project structure and development guide
- Reorganized documentation structure and added project journey
- Added user guide template with comprehensive section outline
- Added GitHub Issues tracking guide
- Set up MkDocs with initial guide structure
- Set up GitHub Pages deployment
- Updated GitHub Pages workflow for static deployment
- Created GitHub Actions workflow for documentation
- Updated MkDocs configuration and workflow
- Added development tasks tracker with detailed checklists
- Added comprehensive enhanced testing checklist with redundancy
- Created comprehensive database schema documentation
- Added file relationship rules document for maintaining project integrity
- Implemented MCP time handling for consistent date references
- Updated file relationship rules to include MCP time relationships
- Reorganized MCP time implementation into utils/mcp directory
- Created example script for demonstrating time utility usage
- Configured MCP to use the official time server

### April 12, 2025 (Afternoon)

- Implemented project structure based on TDD and PRD requirements
- Created core directory structure for src/ with appropriate subdirectories
- Implemented database models in src/database/models.py
- Created database connection module in src/database/connection.py
- Implemented basic scraper components in src/scraper/
- Created API structure with FastAPI in src/api/
- Implemented API routes for websites, articles, and scraping
- Created Pydantic schemas for API requests and responses
- Added unit tests for scraper, API, and database components
- Created main.py entry point with command-line interface
- Updated requirements.txt with all necessary dependencies
- Created comprehensive API documentation
- Updated README.md with installation and usage instructions
- Ensured documentation consistency according to file relationship rules

### April 13, 2025

- Implemented Crawl4AI integration for web scraping
- Set up PostgreSQL database and configured the connection
- Fixed database connection issues and metadata attribute conflicts
- Implemented URL discovery using Crawl4AI's AsyncWebCrawler
- Implemented article extraction with content cleaning and markdown conversion
- Added error handling and fallback mechanisms for scraping
- Created test command for scraper testing
- Updated documentation to reflect Crawl4AI integration
- Tested URL discovery and article extraction with real websites
- Committed changes to the repository

### April 14, 2025 (Afternoon)

- **Frontend Dependencies Optimization**
  - Removed `@types/axios` package in favor of built-in TypeScript types from axios
  - Improved type compatibility and reduced package dependencies
  - Streamlined frontend development setup
- **Documentation Updates**
  - Updated file relationship rules to reflect current project structure
  - Ensured consistency across all documentation files
  - Updated development tasks to reflect completed work
  - Maintained documentation integrity according to established rules

### April 17, 2025

- **Frontend UI Improvements**
  - Fixed Tailwind CSS configuration issues with Next.js 15.3.0
  - Implemented collapsible sidebar with toggle button in header
  - Updated footer to dark color scheme for better visibility
  - Resolved module import errors in ES modules
  - Optimized CSS for better performance and maintainability
  - Ensured compatibility between Tailwind CSS 3.4.1 and Next.js 15.3.0
- **Documentation Updates**
  - Updated development tasks to reflect completed frontend improvements
  - Updated project journey with latest milestones
  - Maintained documentation integrity according to established rules

### April 18, 2025

- **Frontend Development**
  - Implemented mock API service for frontend development
    - Created mockApi.ts with simulated endpoints
    - Added mock data for articles, categories, and sources
    - Implemented realistic API behavior with delays
    - Added support for filtering and pagination
  - Cleaned up redundant configuration files
    - Removed duplicate Next.js, Tailwind CSS, and PostCSS config files
    - Maintained consistent JavaScript configuration files
    - Improved project maintainability
  - Updated documentation to reflect changes
    - Updated development tasks
    - Updated project structure documentation
    - Maintained documentation integrity according to established rules

### April 19, 2025

- **Frontend Testing and Integration**
  - Enhanced mock API implementation
    - Expanded mock data with more diverse test scenarios
    - Added comprehensive unit tests for mock API service
    - Created tests for API context and components
  - Set up Jest testing infrastructure
    - Configured Jest with TypeScript support
    - Added test setup files and mocks
    - Implemented React Testing Library for component testing
  - Integrated mock API with dashboard
    - Created ApiProvider context for dashboard layout
    - Implemented LatestArticles component using mock API
    - Added environment variable configuration for API switching
  - Updated documentation
    - Updated development tasks with completed testing work
    - Updated project journey with latest milestones
    - Maintained documentation integrity according to established rules

### April 20, 2025

- **Mock API Enhancement and Pagination**
  - Expanded mock data for comprehensive testing
    - Increased mock articles from 5 to 15 with diverse content
    - Added additional categories and sources to match expanded articles
    - Created more realistic test scenarios with varied content types
  - Implemented pagination support
    - Added offset parameter to API interfaces
    - Updated mock API service to handle pagination correctly
    - Ensured consistent behavior between mock and real APIs
  - Enhanced LatestArticles component
    - Added pagination controls with Previous/Next buttons
    - Implemented page tracking and article count display
    - Improved user experience with loading states and error handling
  - Updated tests for new functionality
    - Added pagination tests for mock API
    - Ensured all components work with paginated data
    - Maintained test coverage for new features

### May 15, 2025

- **Backend Scraping Improvements**
  - Fixed datetime handling issues
    - Implemented proper timezone handling for article dates
    - Created utility functions for date parsing and conversion
    - Ensured consistent datetime formats across the application
  - Implemented rate limiting and anti-ban measures
    - Created rate limiter module with domain-specific limits
    - Added exponential backoff for retries
    - Implemented user agent rotation and header randomization
  - Enhanced URL discovery
    - Added support for RSS feed discovery
    - Improved sitemap parsing with better error handling
    - Implemented category page discovery
    - Combined multiple discovery methods for better coverage
  - Improved article extraction reliability
    - Enhanced error handling with fallback mechanisms
    - Implemented content validation
    - Added support for different article formats
    - Improved image URL extraction
  - Created test scripts for enhanced functionality
    - Added tests for URL discovery
    - Added tests for article extraction
    - Created implementation script for easy deployment

## Project Milestones

### May 2025

#### May 16, 2025 - Comprehensive Scraping Workflow Documentation
- Created detailed scraping workflow architecture documentation:
  - Mapped the entire scraping process from URL discovery to data storage
  - Documented the technical implementation of each component
  - Identified challenges and implemented solutions
  - Prepared data for vectorization and LLM training
  - Created comprehensive workflow diagrams
- Fixed category handling in the scraping process:
  - Ensured categories are properly extracted and stored
  - Implemented website-specific category handling
  - Created utility scripts for fixing data inconsistencies
  - Updated service layer to properly handle categories
- Updated project documentation to clarify project purpose:
  - Explicitly stated that the platform is for LLM training, not browsing
  - Added LLM integration tasks to development roadmap
  - Updated development rules with project purpose
  - Ensured consistency across all documentation files

#### May 15, 2025 - Backend Scraping Architecture Improvements
- Implemented comprehensive scraping reliability improvements:
  - Fixed datetime handling issues with proper timezone support
  - Created rate limiting module with domain-specific limits and exponential backoff
  - Implemented anti-ban measures with user agent rotation and header randomization
  - Enhanced URL discovery with multiple methods (sitemap, RSS, category pages)
  - Improved article extraction reliability with better error handling and fallback mechanisms
- Created utility modules for reusable functionality:
  - rate_limiter.py for controlling request frequency
  - anti_ban.py for avoiding detection and blocking
  - enhanced_url_discovery.py for better URL discovery
  - enhanced_article_extractor.py for more reliable content extraction
- Updated project documentation to reflect new capabilities
- Created test scripts for validating improvements

### April 2025

#### April 13, 2025 - Major Project Restructuring and Crawl4AI Migration
- Reorganized project directory structure to follow Python naming conventions (snake_case)
- Updated all directory names for better consistency:
  - `api-endpoints` → `api_endpoints`
  - `database-management` → `database_management`
  - `service-layer` → `service_layer`
  - `test-suite` → `test_suite`
  - `utility-modules` → `utility_modules`
  - `web-scraper` → `web_scraper`
- Updated import statements across the codebase
- Enhanced error handling system with comprehensive test suite
- Implemented Crawl4AI v0.5.0 migration changes
- Updated documentation to reflect new directory structure

## Directory Structure Standardization (2024-04-12)
- Standardized directory naming conventions:
  - Converted directory names to kebab-case for better readability
  - Maintained Python files in snake_case for module compatibility
  - Renamed key directories:
    - `database` → `database-management`
    - `services` → `service-layer`
    - `utils` → `utility-modules`
    - `api` → `api-endpoints`
    - `scraper` → `web-scraper`
    - `config` → `configuration`
    - `tests` → `test-suite`
- Updated import statements across the codebase to reflect new directory names
- Ensured all Python files maintain snake_case naming for module compatibility
- Documented naming conventions in project guidelines

## Best Practices Adopted

### Documentation Best Practices

1. **Foundational Documentation Files**
   - **Product Requirements Document (PRD)**: Comprehensive system requirements and feature specifications
   - **Technical Design Document (TDD)**: System architecture and component design
   - **File Relationship Rules**: Ensures documentation and code consistency
   - **Development Standards**:
     - `frontend_rules.mdc`: Frontend development standards and conventions
     - `python_rules.mdc`: Python development standards and conventions
   - **Integration Documentation**:
     - `crawl4ai_integration.md`: Crawl4AI integration details and best practices
     - `database_integration.md`: Database integration patterns and practices
   - **Testing Documentation**:
     - `testing_checklist.md`: Core testing requirements
     - `enhanced_testing_checklist.md`: Advanced testing scenarios
   - **Project Management**:
     - `project_journey.md`: Project evolution and decisions
     - `development_tasks.md`: Task tracking and progress
   - **API Documentation**:
     - `api_documentation.md`: API specifications and usage
   - **User Documentation**:
     - `user_guide.md`: End-user documentation
     - `issue_tracking_guide.md`: Issue management process

2. **Documentation Structure**
   - Using MkDocs for documentation generation
   - Organized documentation in logical directories:
     - `docs/api/`: API documentation
     - `docs/dev/`: Development standards and guides
     - `docs/pm/`: Project management documentation
     - `docs/guide/`: User guides and tutorials
     - `docs/frontend/`: Frontend-specific documentation
     - `docs/notes/`: Project notes and ideas

3. **Documentation Standards**
   - Using consistent Markdown formatting
   - Including "Last Updated" timestamps
   - Maintaining cross-references between documents
   - Following the file relationship rules
   - Using MCP time handling for consistent date references

### Development Best Practices

1. **Database Management**
   - Creating comprehensive schema documentation with ERD
   - Documenting SQL creation scripts
   - Planning for database migrations and maintenance
   - Implementing proper indexing and performance considerations

2. **Task Management**
   - Breaking down tasks into manageable chunks
   - Using hierarchical task organization
   - Tracking progress with checklists
   - Organizing tasks by project phase

3. **Code Organization**
   - Following a modular architecture
   - Separating concerns into distinct components
   - Creating reusable utilities
   - Implementing proper error handling

## Lessons Learned

1. **Documentation is Crucial**
   - Clear documentation saves time in the long run
   - Standards ensure consistency
   - Version control for documentation is essential
   - Maintaining relationships between documents preserves integrity

2. **Planning Pays Off**
   - Detailed planning prevents rework
   - Clear structure enables parallel development
   - Well-defined milestones guide progress
   - Breaking down tasks makes complex projects manageable

3. **Flexibility is Key**
   - Adapting to changing requirements
   - Incorporating new technologies
   - Maintaining scalability
   - Evolving documentation as the project grows

## Looking Forward

The journey of Naija News Hub is just beginning. With a solid foundation in place, we're ready to:

1. Implement the core scraping functionality
2. Develop the API infrastructure
3. Create the user interface
4. Integrate advanced features

This project represents not just a technical solution, but a commitment to making Nigerian news more accessible and researchable. The structured approach we've taken ensures that Naija News Hub will be a robust, scalable, and maintainable system that can grow with the needs of its users.

Stay tuned for more updates as we continue this exciting journey!

## Foundational Documentation Files

This project has established several key documentation files that serve as templates and best practices for future projects:

### Core Documentation
1. **Product Requirements Document (PRD)**
   - Location: `docs/pm/prd.md`
   - Purpose: Defines product vision, goals, and requirements
   - Best Practice: Use as a template for future project requirements documentation

2. **Technical Design Document (TDD)**
   - Location: `docs/pm/tdd.md`
   - Purpose: Outlines technical architecture, components, and implementation details
   - Best Practice: Follow the established structure for technical documentation

3. **File Relationship Rules**
   - Location: `docs/dev/file-relationship-rules.md`
   - Purpose: Defines relationships between files and ensures documentation integrity
   - Best Practice: Implement similar rules for maintaining documentation consistency

4. **MkDocs Documentation**
   - Location: `docs/`
   - Purpose: Comprehensive project documentation using MkDocs
   - Best Practice: Use MkDocs for all future project documentation

### Integration Documentation
1. **Crawl4AI Integration**
   - Location: `docs/dev/crawl4ai-integration.md`
   - Purpose: Documents web scraping integration and best practices
   - Best Practice: Use as a template for third-party service integrations

2. **Database Integration**
   - Location: `docs/dev/database-integration.md`
   - Purpose: Documents database architecture and integration patterns
   - Best Practice: Follow established database integration patterns

### Testing Documentation
1. **Testing Checklist**
   - Location: `docs/dev/testing-checklist.md`
   - Purpose: Standardizes testing procedures and coverage
   - Best Practice: Use as a template for test planning

2. **Enhanced Testing Checklist**
   - Location: `docs/dev/enhanced-testing-checklist.md`
   - Purpose: Advanced testing scenarios and edge cases
   - Best Practice: Implement comprehensive testing strategies

### Project Management
1. **Development Tasks**
   - Location: `docs/dev/development-tasks.md`
   - Purpose: Tracks development progress and priorities
   - Best Practice: Maintain clear task tracking and progress updates

2. **Project Journey**
   - Location: `docs/pm/project-journey.md`
   - Purpose: Documents project evolution and key decisions
   - Best Practice: Keep detailed project history and decision logs

### API Documentation
1. **API Documentation**
   - Location: `docs/api/api-documentation.md`
   - Purpose: Comprehensive API reference and usage guidelines
   - Best Practice: Maintain up-to-date API documentation

### User Documentation
1. **User Guide**
   - Location: `docs/app/user-guide.md`
   - Purpose: End-user documentation and tutorials
   - Best Practice: Create clear and comprehensive user guides

### Frontend Documentation
1. **Frontend Project Structure**
   - Location: `docs/frontend/project-structure.md`
   - Purpose: Documents frontend architecture and components
   - Best Practice: Follow established frontend documentation patterns

2. **Frontend Development Tasks**
   - Location: `docs/frontend/development-tasks.md`
   - Purpose: Tracks frontend development progress
   - Best Practice: Maintain separate frontend task tracking

### Documentation Standards
1. **File Naming Convention**
   - Use hyphens (-) for Markdown documentation files
   - Use underscores (_) for Python files
   - Follow consistent casing (lowercase for all files)

2. **Directory Structure**
   - Organize documentation in logical directories
   - Maintain clear separation of concerns
   - Follow established directory naming conventions

3. **Documentation Format**
   - Use consistent Markdown formatting
   - Include "Last Updated" timestamps
   - Maintain cross-references between documents
   - Follow file relationship rules