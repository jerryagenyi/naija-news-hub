# Naija News Hub - File Relationship Rules

This document defines the relationships between project files and establishes rules for maintaining integrity when files are updated. Following these rules will ensure consistency across documentation and code.

## Core Documentation Relationships

### Database Documentation

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `docs/dev/database-schema.md` | `docs/pm/tdd.md` | When database schema is updated, ensure the schema section in TDD is updated to match. |
| `docs/dev/database-schema.md` | `config/config_template.py` | When database schema is updated, ensure Pydantic models in config template reflect the changes. |
| `docs/dev/database-schema.md` | `docs/dev/development-tasks.md` | When database schema is updated, ensure database-related tasks are updated accordingly. |
| `docs/dev/database-schema.md` | `docs/dev/testing-checklist.md` | When database schema is updated, ensure database testing sections are updated to cover new/changed features. |
| `docs/dev/database-schema.md` | `docs/dev/enhanced-testing-checklist.md` | When database schema is updated, ensure enhanced database testing sections are updated to cover new/changed features. |
| `docs/dev/database-integration.md` | `src/database/repositories/*.py` | When repository implementations are updated, ensure database integration documentation is updated to match. |
| `docs/dev/database-integration.md` | `src/services/article_service.py` | When article service is updated, ensure database integration documentation is updated to match. |
| `docs/dev/database-integration.md` | `docs/dev/development-tasks.md` | When database integration documentation is updated, ensure development tasks are updated accordingly. |
| `docs/dev/database-integration.md` | `docs/pm/project-journey.md` | When database integration is updated, ensure project journey document reflects the changes. |

### Testing Documentation

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `docs/dev/testing-checklist.md` | `docs/dev/enhanced-testing-checklist.md` | When testing checklist is updated, ensure enhanced testing checklist is updated to maintain consistency. |
| `docs/dev/testing-checklist.md` | `docs/dev/development-tasks.md` | When testing checklist is updated, ensure testing tasks in development tasks are updated accordingly. |
| `docs/dev/enhanced-testing-checklist.md` | `docs/dev/testing-checklist.md` | When enhanced testing checklist is updated, ensure regular testing checklist is updated with core items. |

### Development Tasks

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `docs/dev/development-tasks.md` | `docs/pm/tdd.md` | When development tasks are updated, ensure TDD reflects any architectural or design changes. |
| `docs/dev/development-tasks.md` | `docs/dev/testing-checklist.md` | When development tasks are updated, ensure testing checklist covers the new/changed features. |
| `docs/dev/development-tasks.md` | `README.md` | When major development tasks are completed, ensure README is updated to reflect current project status. |
| `docs/dev/development-tasks.md` | `docs/pm/project-journey.md` | When significant development tasks are completed, add an entry to the project journey document with the date. |

### Configuration Files

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `config/config_template.py` | `.env.example` | When configuration template is updated, ensure .env.example includes all required environment variables. |
| `config/config_template.py` | `.env` | When configuration template is updated, ensure your local .env file is updated with new variables (not committed to Git). |
| `.env.example` | `docs/dev/database-schema.md` | When database-related environment variables are updated, ensure they align with the database schema documentation. |
| `config/config_template.py` | `docs/dev/crawl4ai-integration.md` | When Crawl4AI configuration is updated, ensure the integration documentation is updated to match. |
| `config/config.py` | `docs/dev/crawl4ai-integration.md` | When Crawl4AI configuration implementation is updated, ensure the integration documentation is updated to match. |

### MCP Configuration

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `mcp.json` | `utils/mcp/time.py` | When MCP time configuration is updated, ensure the time utility implementation is compatible. |
| `utils/mcp/time.py` | `docs/pm/project-journey.md` | When MCP time module is updated, ensure project journey document uses the correct date format. |
| `utils/mcp/time.py` | Any documentation with timestamps | When MCP time module is updated, ensure all documentation with timestamps follows the same format. |

## Code Relationships

### Database Models

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `models/database.py` | `docs/dev/database-schema.md` | When database models are updated, ensure database schema documentation is updated to match. |
| `models/database.py` | `migrations/` | When database models are updated, ensure a new migration is created to update the database schema. |
| `models/database.py` | `repositories/` | When database models are updated, ensure repository classes are updated to handle the changes. |

### Scraper Components

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `src/scraper/url_discovery.py` | `docs/dev/crawl4ai-integration.md` | When URL discovery code is updated, ensure Crawl4AI integration documentation is updated. |
| `src/scraper/article_extractor.py` | `docs/dev/crawl4ai-integration.md` | When article extraction code is updated, ensure Crawl4AI integration documentation is updated. |
| `src/scraper/url_discovery.py` | `tests/test_scraper.py` | When URL discovery code is updated, ensure tests are updated to cover the changes. |
| `src/scraper/article_extractor.py` | `tests/test_scraper.py` | When article extraction code is updated, ensure tests are updated to cover the changes. |
| `src/scraper/url_discovery.py` | `docs/dev/testing-checklist.md` | When URL discovery features are added/changed, ensure testing checklist is updated. |
| `src/scraper/article_extractor.py` | `docs/dev/testing-checklist.md` | When article extraction features are added/changed, ensure testing checklist is updated. |

### API Components

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `api/routes/` | `docs/api/api-documentation.md` | When API routes are updated, ensure API documentation is updated to match. |
| `api/routes/` | `tests/test_api.py` | When API routes are updated, ensure API tests are updated to cover the changes. |
| `api/schemas/` | `models/database.py` | When API schemas are updated, ensure they remain compatible with database models. |
| `frontend/src/app/dashboard/websites/page.tsx` | `docs/app/user-guide.md` | When websites management page is updated, ensure user guide is updated to match. |
| `frontend/src/app/dashboard/jobs/page.tsx` | `docs/app/user-guide.md` | When jobs management page is updated, ensure user guide is updated to match. |
| `frontend/src/components/layout/Header.tsx` | `docs/frontend/project-structure.md` | When header component is updated, ensure frontend project structure documentation is updated if needed. |
| `frontend/src/components/layout/Footer.tsx` | `docs/frontend/project-structure.md` | When footer component is updated, ensure frontend project structure documentation is updated if needed. |
| `frontend/src/components/layout/Sidebar.tsx` | `docs/frontend/project-structure.md` | When sidebar component is updated, ensure frontend project structure documentation is updated if needed. |

### Project Journey

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|-----------------|
| `docs/pm/project-journey.md` | `docs/dev/development-tasks.md` | When the project journey is updated, ensure it reflects completed development tasks. |
| `docs/pm/project-journey.md` | `docs/pm/tdd.md` | When architectural decisions are documented in the project journey, ensure they are reflected in the TDD. |
| `docs/pm/project-journey.md` | `README.md` | When major milestones are documented in the project journey, update the README to reflect current project status. |

### Time Handling

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|-----------------|
| `utils/mcp/time.py` | All documentation files | When updating documentation with dates or timestamps, use the MCP time module to ensure consistency. |
| `utils/mcp/time.py` | `docs/pm/project-journey.md` | When adding entries to the project journey, include the current date from the MCP time module. |
| `utils/mcp/time.py` | Database timestamp fields | When storing timestamps in the database, use consistent formats from the MCP time module. |

## Documentation Consistency Rules

1. **Version Numbers**: When updating version numbers, ensure they are updated in:
   - `README.md`
   - `setup.py`
   - `scraper/__init__.py`
   - `docs/pm/changelog.md`

2. **Feature Descriptions**: When adding/changing features, ensure they are consistently described in:
   - `README.md`
   - `docs/pm/tdd.md`
   - `docs/dev/development-tasks.md`
   - Relevant API documentation

3. **Database Schema Changes**: When making database schema changes:
   - Update `docs/dev/database-schema.md` first
   - Create database migration scripts
   - Update Pydantic models in `config/config_template.py`
   - Update ORM models in `src/database/models.py`
   - Update repository classes in `src/database/repositories/`
   - Update tests to cover the changes
   - Update `docs/dev/database-integration.md` to reflect the changes

4. **Testing Documentation**: When updating testing documentation:
   - Ensure both `testing-checklist.md` and `enhanced-testing-checklist.md` remain in sync
   - Update actual test files to implement the described tests
   - Update development tasks to reflect testing requirements

5. **Crawl4AI Integration**: When updating Crawl4AI integration:
   - Update `docs/dev/crawl4ai-integration.md` to reflect implementation changes
   - Update `src/scraper/url_discovery.py` and `src/scraper/article_extractor.py` to maintain consistency
   - Update configuration in `config/config_template.py` if needed
   - Update tests to cover the changes
   - Update development tasks to reflect completed tasks

6. **Database Integration**: When updating database integration:
   - Update `docs/dev/database-integration.md` to reflect implementation changes
   - Update repository classes in `src/database/repositories/` to maintain consistency
   - Update service classes in `src/services/` to reflect the changes
   - Update CLI commands in `main.py` if needed
   - Update tests to cover the changes
   - Update development tasks to reflect completed tasks

7. **Time and Date References**: When adding time or date references:
   - Use the MCP time module (`utils/mcp/time.py`) to get the current date/time
   - Follow the format YYYY-MM-DD for dates
   - Update the "Last Updated" timestamp in documentation files
   - Ensure all documentation uses consistent date formats

## File Modification Checklist

When modifying any file, ask yourself:

1. Does this change affect the database schema?
2. Does this change affect the database integration?
3. Does this change affect the API?
4. Does this change affect the scraper functionality?
5. Does this change affect Crawl4AI integration?
6. Does this change affect configuration requirements?
7. Does this change require updates to tests?
8. Does this change require updates to documentation?

For each "yes" answer, identify the related files using this document and update them accordingly.

## Automated Integrity Checks

Consider implementing the following automated checks:

1. **Pre-commit hooks**: Set up Git pre-commit hooks to check for consistency between related files.
2. **Documentation linting**: Use tools to ensure documentation is consistent and up-to-date.
3. **Schema validation**: Validate that database schema documentation matches actual database models.
4. **Test coverage**: Ensure test coverage is maintained when code is updated.

## Maintaining This Document

This document itself should be updated whenever:

1. New files or components are added to the project
2. Existing files are renamed or moved
3. New relationships between files are identified
4. New integrity rules are established

By following these rules, we can ensure that our project remains consistent and well-documented as it evolves.

## Documentation Standards

1. **File Naming Conventions**
   - Use hyphens (-) for Markdown documentation files (e.g., `project-journey.md`, `api-documentation.md`)
   - Use underscores (_) for Python files to maintain module compatibility
   - Use descriptive, full names instead of abbreviations
   - Follow consistent casing (lowercase for all files)

2. **Directory Structure**
   - Organize documentation in logical directories:
     - `docs/api/`: API documentation
     - `docs/dev/`: Development standards and guides
     - `docs/pm/`: Project management documentation
     - `docs/guide/`: User guides and tutorials
     - `docs/frontend/`: Frontend-specific documentation
     - `docs/notes/`: Project notes and ideas

3. **Documentation Format**
   - Use consistent Markdown formatting
   - Include "Last Updated" timestamps
   - Maintain cross-references between documents
   - Follow the file relationship rules
   - Use MCP time handling for consistent date references
