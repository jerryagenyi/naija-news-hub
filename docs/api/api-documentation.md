# Naija News Hub - API Documentation

**Last Updated:** 2024-04-16

This document provides comprehensive documentation for the Naija News Hub API, including endpoints, request/response formats, authentication, and usage examples.

## API Overview

The Naija News Hub API provides programmatic access to Nigerian news articles and related data. It allows you to:

- Retrieve articles from various Nigerian news sources
- Search for articles by keyword, date, source, or category
- Manage news sources and scraping operations
- Access article metadata and content

## Base URL

```
https://api.naijanewshub.com/api
```

For local development:

```
http://localhost:8000/api
```

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints, you need to include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Getting a Token

```http
POST /auth/token
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## API Endpoints

### Health Check

#### Get API Status

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Websites

#### List All Websites

```http
GET /websites
```

Query Parameters:
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100)
- `active_only` (boolean, optional): Only return active websites (default: false)

Response:

```json
[
  {
    "id": 1,
    "name": "Punch Nigeria",
    "base_url": "https://punchng.com",
    "description": "Nigerian daily newspaper",
    "logo_url": "https://punchng.com/logo.png",
    "sitemap_url": "https://punchng.com/sitemap.xml",
    "active": true,
    "created_at": "2025-03-15T10:30:00Z",
    "updated_at": "2025-04-01T14:20:00Z"
  },
  {
    "id": 2,
    "name": "Vanguard Nigeria",
    "base_url": "https://vanguardngr.com",
    "description": "Nigerian news and media website",
    "logo_url": "https://vanguardngr.com/logo.png",
    "sitemap_url": "https://vanguardngr.com/sitemap.xml",
    "active": true,
    "created_at": "2025-03-15T11:45:00Z",
    "updated_at": "2025-04-02T09:15:00Z"
  }
]
```

#### Get Website by ID

```http
GET /websites/{website_id}
```

Response:

```json
{
  "id": 1,
  "name": "Punch Nigeria",
  "base_url": "https://punchng.com",
  "description": "Nigerian daily newspaper",
  "logo_url": "https://punchng.com/logo.png",
  "sitemap_url": "https://punchng.com/sitemap.xml",
  "active": true,
  "created_at": "2025-03-15T10:30:00Z",
  "updated_at": "2025-04-01T14:20:00Z"
}
```

#### Create Website

```http
POST /websites
Content-Type: application/json

{
  "name": "The Guardian Nigeria",
  "base_url": "https://guardian.ng",
  "description": "Nigerian news website",
  "logo_url": "https://guardian.ng/logo.png",
  "sitemap_url": "https://guardian.ng/sitemap.xml",
  "active": true
}
```

Response:

```json
{
  "id": 3,
  "name": "The Guardian Nigeria",
  "base_url": "https://guardian.ng",
  "description": "Nigerian news website",
  "logo_url": "https://guardian.ng/logo.png",
  "sitemap_url": "https://guardian.ng/sitemap.xml",
  "active": true,
  "created_at": "2025-04-12T15:30:00Z",
  "updated_at": "2025-04-12T15:30:00Z"
}
```

#### Update Website

```http
PUT /websites/{website_id}
Content-Type: application/json

{
  "name": "The Guardian Nigeria (Updated)",
  "description": "Updated description",
  "active": false
}
```

Response:

```json
{
  "id": 3,
  "name": "The Guardian Nigeria (Updated)",
  "base_url": "https://guardian.ng",
  "description": "Updated description",
  "logo_url": "https://guardian.ng/logo.png",
  "sitemap_url": "https://guardian.ng/sitemap.xml",
  "active": false,
  "created_at": "2025-04-12T15:30:00Z",
  "updated_at": "2025-04-12T16:45:00Z"
}
```

#### Delete Website

```http
DELETE /websites/{website_id}
```

Response:

```json
{
  "message": "Website deleted successfully"
}
```

### Articles

#### List Articles

```http
GET /articles
```

Query Parameters:
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100)
- `website_id` (integer, optional): Filter by website ID
- `search` (string, optional): Search term for article title or content

Response:

```json
[
  {
    "id": 1,
    "title": "Nigeria Celebrates Independence Day",
    "url": "https://punchng.com/nigeria-celebrates-independence-day",
    "content": "Nigeria celebrated its independence day with...",
    "content_markdown": "# Nigeria Celebrates Independence Day\n\nNigeria celebrated its independence day with...",
    "content_html": "<h1>Nigeria Celebrates Independence Day</h1><p>Nigeria celebrated its independence day with...</p>",
    "author": "John Doe",
    "published_at": "2025-10-01T08:00:00Z",
    "image_url": "https://punchng.com/images/independence.jpg",
    "website_id": 1,
    "metadata": {
      "word_count": 450,
      "reading_time": 3
    },
    "active": true,
    "created_at": "2025-10-01T10:30:00Z",
    "updated_at": "2025-10-01T10:30:00Z"
  },
  {
    "id": 2,
    "title": "Economic Growth in Nigeria",
    "url": "https://vanguardngr.com/economic-growth-in-nigeria",
    "content": "Nigeria's economy has shown signs of growth...",
    "content_markdown": "# Economic Growth in Nigeria\n\nNigeria's economy has shown signs of growth...",
    "content_html": "<h1>Economic Growth in Nigeria</h1><p>Nigeria's economy has shown signs of growth...</p>",
    "author": "Jane Smith",
    "published_at": "2025-09-28T14:15:00Z",
    "image_url": "https://vanguardngr.com/images/economy.jpg",
    "website_id": 2,
    "metadata": {
      "word_count": 620,
      "reading_time": 4
    },
    "active": true,
    "created_at": "2025-09-28T15:45:00Z",
    "updated_at": "2025-09-28T15:45:00Z"
  }
]
```

#### Get Article by ID

```http
GET /articles/{article_id}
```

Response:

```json
{
  "id": 1,
  "title": "Nigeria Celebrates Independence Day",
  "url": "https://punchng.com/nigeria-celebrates-independence-day",
  "content": "Nigeria celebrated its independence day with...",
  "content_markdown": "# Nigeria Celebrates Independence Day\n\nNigeria celebrated its independence day with...",
  "content_html": "<h1>Nigeria Celebrates Independence Day</h1><p>Nigeria celebrated its independence day with...</p>",
  "author": "John Doe",
  "published_at": "2025-10-01T08:00:00Z",
  "image_url": "https://punchng.com/images/independence.jpg",
  "website_id": 1,
  "metadata": {
    "word_count": 450,
    "reading_time": 3
  },
  "active": true,
  "created_at": "2025-10-01T10:30:00Z",
  "updated_at": "2025-10-01T10:30:00Z"
}
```

#### Get Article by URL

```http
GET /articles/url/{url}
```

Response: Same as Get Article by ID

### Scraping

#### Start Website Scraping

```http
POST /scraping/website/{website_id}
Content-Type: application/json

{
  "config": {
    "max_depth": 3,
    "rate_limit": 2,
    "proxy_rotation": true
  }
}
```

Response:

```json
{
  "id": 0,
  "website_id": 1,
  "status": "pending",
  "articles_found": 0,
  "articles_scraped": 0,
  "config": {
    "max_depth": 3,
    "rate_limit": 2,
    "proxy_rotation": true
  }
}
```

#### Start All Websites Scraping

```http
POST /scraping/all
Content-Type: application/json

{
  "config": {
    "max_depth": 2,
    "rate_limit": 1,
    "proxy_rotation": true
  }
}
```

Response:

```json
[
  {
    "id": 0,
    "website_id": 1,
    "status": "pending",
    "articles_found": 0,
    "articles_scraped": 0,
    "config": {
      "max_depth": 2,
      "rate_limit": 1,
      "proxy_rotation": true
    }
  },
  {
    "id": 0,
    "website_id": 2,
    "status": "pending",
    "articles_found": 0,
    "articles_scraped": 0,
    "config": {
      "max_depth": 2,
      "rate_limit": 1,
      "proxy_rotation": true
    }
  }
]
```

#### Get Scraping Jobs

```http
GET /scraping/jobs
```

Query Parameters:
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100)
- `website_id` (integer, optional): Filter by website ID
- `status` (string, optional): Filter by job status (pending, running, completed, failed)

Response:

```json
[
  {
    "id": 1,
    "website_id": 1,
    "website_name": "Punch Nigeria",
    "status": "running",
    "progress": 75,
    "articles_found": 120,
    "articles_processed": 90,
    "errors": 0,
    "start_time": "2024-04-16T06:45:02Z",
    "end_time": null,
    "config": {
      "max_depth": 3,
      "rate_limit": 2,
      "proxy_rotation": true
    }
  },
  {
    "id": 2,
    "website_id": 2,
    "website_name": "Vanguard Nigeria",
    "status": "running",
    "progress": 45,
    "articles_found": 85,
    "articles_processed": 38,
    "errors": 2,
    "start_time": "2024-04-16T07:00:02Z",
    "end_time": null,
    "config": {
      "max_depth": 3,
      "rate_limit": 2,
      "proxy_rotation": true
    }
  }
]
```

#### Control Scraping Job

```http
POST /scraping/jobs/{job_id}/control
Content-Type: application/json

{
  "action": "pause|resume|stop|restart"
}
```

Response:

```json
{
  "id": 1,
  "website_id": 1,
  "website_name": "Punch Nigeria",
  "status": "paused",
  "progress": 75,
  "articles_found": 120,
  "articles_processed": 90,
  "errors": 0,
  "start_time": "2024-04-16T06:45:02Z",
  "end_time": "2024-04-16T07:15:02Z",
  "config": {
    "max_depth": 3,
    "rate_limit": 2,
    "proxy_rotation": true
  }
}
```

```json
[
  {
    "id": 1,
    "website_id": 1,
    "status": "completed",
    "start_time": "2025-04-12T10:00:00Z",
    "end_time": "2025-04-12T10:15:00Z",
    "articles_found": 150,
    "articles_scraped": 145,
    "error_message": null,
    "config": {
      "max_depth": 3,
      "rate_limit": 2,
      "proxy_rotation": true
    },
    "created_at": "2025-04-12T10:00:00Z",
    "updated_at": "2025-04-12T10:15:00Z"
  },
  {
    "id": 2,
    "website_id": 2,
    "status": "running",
    "start_time": "2025-04-12T10:30:00Z",
    "end_time": null,
    "articles_found": 120,
    "articles_scraped": 80,
    "error_message": null,
    "config": {
      "max_depth": 2,
      "rate_limit": 1,
      "proxy_rotation": true
    },
    "created_at": "2025-04-12T10:30:00Z",
    "updated_at": "2025-04-12T10:45:00Z"
  }
]
```

#### Get Scraping Job by ID

```http
GET /scraping/jobs/{job_id}
```

Response:

```json
{
  "id": 1,
  "website_id": 1,
  "status": "completed",
  "start_time": "2025-04-12T10:00:00Z",
  "end_time": "2025-04-12T10:15:00Z",
  "articles_found": 150,
  "articles_scraped": 145,
  "error_message": null,
  "config": {
    "max_depth": 3,
    "rate_limit": 2,
    "proxy_rotation": true
  },
  "created_at": "2025-04-12T10:00:00Z",
  "updated_at": "2025-04-12T10:15:00Z"
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request:

- 200 OK: The request was successful
- 400 Bad Request: The request was invalid
- 401 Unauthorized: Authentication failed
- 403 Forbidden: The authenticated user doesn't have permission
- 404 Not Found: The requested resource was not found
- 500 Internal Server Error: An error occurred on the server

Error responses include a JSON object with an error message:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Dashboard API

#### Get Dashboard Stats

```http
GET /dashboard/stats
```

Response:

```json
{
  "total_articles": 1234,
  "total_websites": 15,
  "active_jobs": 3,
  "error_count": 2,
  "trends": {
    "articles": {
      "value": 1234,
      "change": 12.5,
      "period": "24h"
    },
    "websites": {
      "value": 15,
      "change": 0,
      "period": "24h"
    },
    "jobs": {
      "value": 3,
      "change": -2,
      "period": "24h"
    },
    "errors": {
      "value": 2,
      "change": 50,
      "period": "24h"
    }
  }
}
```

#### Get Recent Errors

```http
GET /dashboard/errors
```

Query Parameters:
- `limit` (integer, optional): Maximum number of records to return (default: 10)

Response:

```json
[
  {
    "id": 1,
    "website_id": 1,
    "website_name": "Punch Nigeria",
    "type": "network",
    "message": "Connection timeout",
    "timestamp": "2024-04-16T07:05:02Z",
    "url": "https://punchng.com/some-article",
    "resolved": false
  },
  {
    "id": 2,
    "website_id": 2,
    "website_name": "Vanguard Nigeria",
    "type": "parsing",
    "message": "Failed to extract article content",
    "timestamp": "2024-04-16T06:50:02Z",
    "url": "https://vanguardngr.com/some-article",
    "resolved": false
  }
]
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Rate limits are applied per API key or IP address:

- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers are included in the response:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1617981600
```

## Pagination

List endpoints support pagination using `skip` and `limit` parameters:

```
GET /articles?skip=100&limit=50
```

Response headers include pagination information:

```
X-Total-Count: 1250
X-Page-Count: 25
X-Current-Page: 3
```

## Versioning

The API is versioned to ensure backward compatibility. The current version is v1:

```
https://api.naijanewshub.com/api/v1/articles
```

## SDKs and Client Libraries

- Python: [naijanewshub-python](https://github.com/naijanewshub/python-client)
- JavaScript: [naijanewshub-js](https://github.com/naijanewshub/js-client)

## Support

For API support, please contact:

- Email: api-support@naijanewshub.com
- Documentation: https://docs.naijanewshub.com
- GitHub Issues: https://github.com/naijanewshub/api/issues
