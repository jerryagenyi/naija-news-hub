# Naija News Hub - File Relationship Rules

This document defines the relationships between project files and establishes rules for maintaining integrity when files are updated. Following these rules will ensure consistency across documentation and code.

## Core Documentation Relationships

### Database Schema Documentation

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `docs/dev/database-schema.md` | `docs/pm/tdd.md` | When database schema is updated, ensure the schema section in TDD is updated to match. |
| `docs/dev/database-schema.md` | `config/config_template.py` | When database schema is updated, ensure Pydantic models in config template reflect the changes. |
| `docs/dev/database-schema.md` | `docs/dev/development-tasks.md` | When database schema is updated, ensure database-related tasks are updated accordingly. |
| `docs/dev/database-schema.md` | `docs/dev/testing-checklist.md` | When database schema is updated, ensure database testing sections are updated to cover new/changed features. |
| `docs/dev/database-schema.md` | `docs/dev/enhanced-testing-checklist.md` | When database schema is updated, ensure enhanced database testing sections are updated to cover new/changed features. |

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

### Configuration Files

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `config/config_template.py` | `.env.example` | When configuration template is updated, ensure .env.example includes all required environment variables. |
| `config/config_template.py` | `.env` | When configuration template is updated, ensure your local .env file is updated with new variables (not committed to Git). |
| `.env.example` | `docs/dev/database-schema.md` | When database-related environment variables are updated, ensure they align with the database schema documentation. |

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
| `scraper/article_scraper.py` | `tests/test_scraper.py` | When scraper code is updated, ensure tests are updated to cover the changes. |
| `scraper/article_scraper.py` | `docs/dev/testing-checklist.md` | When scraper features are added/changed, ensure testing checklist is updated. |
| `scraper/utils/exporters.py` | `tests/test_exporters.py` | When exporter code is updated, ensure tests are updated to cover the changes. |

### API Components

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `api/routes/` | `docs/api/api-documentation.md` | When API routes are updated, ensure API documentation is updated to match. |
| `api/routes/` | `tests/test_api.py` | When API routes are updated, ensure API tests are updated to cover the changes. |
| `api/schemas/` | `models/database.py` | When API schemas are updated, ensure they remain compatible with database models. |

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
   - Update ORM models in `models/database.py`
   - Update repository classes in `repositories/`
   - Update tests to cover the changes

4. **Testing Documentation**: When updating testing documentation:
   - Ensure both `testing-checklist.md` and `enhanced-testing-checklist.md` remain in sync
   - Update actual test files to implement the described tests
   - Update development tasks to reflect testing requirements

## File Modification Checklist

When modifying any file, ask yourself:

1. Does this change affect the database schema?
2. Does this change affect the API?
3. Does this change affect the scraper functionality?
4. Does this change affect configuration requirements?
5. Does this change require updates to tests?
6. Does this change require updates to documentation?

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
