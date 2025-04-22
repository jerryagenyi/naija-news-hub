# Naija News Hub - Efficient Scraping Architecture

This document outlines the architecture and strategies for implementing an efficient, cost-effective web scraping system for Naija News Hub. These principles are designed to minimize resource usage while maintaining scalability.

## Core Architecture Principles

### 1. Centralized Agent Architecture

We implement a centralized multi-agent system with task-specific roles to optimize resource usage:

| Component | Implementation | Related Files |
|-----------|----------------|---------------|
| Agent-1: URL Discovery | Single agent instance for all websites | `src/web_scraper/url_discovery_agent.py` |
| Agent-2: Content Extraction | Single agent instance for all articles | `src/web_scraper/content_extraction_agent.py` |
| Agent-3: Metadata Enhancement | Single agent instance for all articles | `src/web_scraper/metadata_enhancement_agent.py` |
| Database Coordination | Sitemaps table for agent workflow coordination | `src/database_management/models.py` |

#### Implementation Rules:
- Use a single agent instance per task type instead of per-website agents
- Implement database-coordinated workflow using the sitemaps table
- Process websites in batches to manage resource usage
- Implement domain-based rate limiting to avoid triggering anti-scraping measures
- Use efficient LLM models (GPT-4o-mini where possible, GPT-4o for complex extraction)

### 2. Scheduled Batch Processing

Instead of continuous scraping, we implement scheduled batch processing to optimize resource usage:

| Component | Implementation | Related Files |
|-----------|----------------|--------------|
| Scheduler | Cron-based job scheduler | `src/scheduler/job_scheduler.py` |
| Job Queue | Simple queue for managing scraping tasks | `src/scheduler/job_queue.py` |
| Worker | Process that executes scraping tasks | `src/scraper/worker.py` |

#### Implementation Rules:
- Schedule scraping during off-peak hours when possible
- Implement configurable frequency per news source
- Use a single worker process for multiple sources to minimize resource usage
- Log all job executions for monitoring and debugging

### 2. Intelligent Crawling

Only scrape content that has changed to minimize bandwidth and processing:

| Strategy | Implementation | Related Files |
|----------|----------------|--------------|
| ETag/Last-Modified | Check HTTP headers before downloading | `src/scraper/http_client.py` |
| Content Hashing | Generate and compare content hashes | `src/utils/hash_utils.py` |
| URL Fingerprinting | Track already processed URLs | `src/database/repositories/url_repository.py` |

#### Implementation Rules:
- Store and check ETag/Last-Modified headers for each URL
- Implement content hash comparison to detect actual changes
- Skip processing for unchanged content
- Maintain a URL history with last processed timestamp and status

### 3. Content Compression

Minimize storage requirements through efficient compression:

| Strategy | Implementation | Related Files |
|----------|----------------|--------------|
| Text Compression | Compress article text | `src/utils/compression.py` |
| Database Optimization | Use appropriate column types | `src/database/models.py` |
| Normalization | Proper database schema design | `docs/dev/database-schema.md` |

#### Implementation Rules:
- Store article content in compressed format when appropriate
- Use TEXT type with compression for PostgreSQL
- Normalize database schema to reduce redundancy
- Consider JSON compression for metadata storage

### 4. Data Retention Policies

Manage data growth through intelligent retention policies:

| Strategy | Implementation | Related Files |
|----------|----------------|--------------|
| Archiving | Move older content to archive tables | `src/services/archive_service.py` |
| Pruning | Remove unnecessary data | `src/services/maintenance_service.py` |
| Summarization | Generate and store content summaries | `src/services/content_service.py` |

#### Implementation Rules:
- Define clear retention periods for different data types
- Implement automated archiving for older content
- Maintain full-text search capability for archived content
- Create a maintenance schedule for database optimization

### 5. Compute/Storage Separation

Design the system to scale compute and storage independently:

| Component | Implementation | Related Files |
|-----------|----------------|--------------|
| Scraper Service | Stateless scraping logic | `src/scraper/` |
| Database | Centralized storage | `src/database/` |
| Configuration | Environment-based config | `config/config.py` |

#### Implementation Rules:
- Keep scraping logic stateless
- Use environment variables for configuration
- Implement connection pooling for database access
- Design for potential future distribution of scraping tasks

## Implementation in VPS Environment

For deployment on a standard VPS (Hostinger/Ionos) with Cloudflare:

### Resource Allocation for Text-Only Scraping with AI Agents

| Resource | Allocation | Monitoring | Optimization Strategy |
|----------|------------|------------|----------------------|
| CPU | Limit scraping processes to avoid overload | `src/utils/resource_monitor.py` | Schedule jobs during off-peak hours |
| Memory | Implement memory limits for scraping processes | `src/utils/resource_monitor.py` | Use streaming parsers for large pages |
| Storage | Monitor growth rate and implement compression | `src/services/maintenance_service.py` | Compress text content, implement retention policies |
| Bandwidth | Schedule scraping to distribute bandwidth usage | `src/scheduler/job_scheduler.py` | Use conditional GET requests (ETag/Last-Modified) |
| API Tokens | Monitor token usage for LLM API calls | `src/monitoring/token_monitor.py` | Use GPT-4o-mini where possible, batch similar requests |
| Agent Concurrency | Limit concurrent agent operations | `src/web_scraper/agent_manager.py` | Process websites in batches, implement adaptive concurrency |

### Cost-Efficient VPS Configuration

For text-only scraping of up to 5 sources with AI agents, a standard VPS with the following specifications is sufficient:

| Component | Recommended Specification | Purpose |
|-----------|---------------------------|--------|
| CPU | 2-4 vCPU cores | Handle concurrent scraping tasks |
| Memory | 4-8GB RAM | Process content and run agent coordination |
| Storage | 50-100GB SSD | Store articles, metadata, and agent state |
| Bandwidth | 2-4TB monthly | Handle scraping and serving content |
| Cost Range | $20-25/month | Hostinger or Ionos VPS plans |
| API Budget | $50-100/month | OpenAI API for GPT-4o and GPT-4o-mini |

### Deployment Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Cron        │───▶│ Scheduler   │───▶│ Job Queue   │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                                             ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Agent       │◀───│ Job Handler │◀───│ Agent       │
│ Manager     │    └─────────────┘    │ Coordinator │
└─────────────┘           │           └─────────────┘
      │                    │                  │
      ▼                    ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Agent-1:    │    │ Agent-2:    │    │ Agent-3:    │
│ URL Discovery│    │ Content Ext.│    │ Metadata Enh.│
└─────────────┘    └─────────────┘    └─────────────┘
      │                    │                  │
      │                    │                  │
      ▼                    ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ PostgreSQL  │◀───│ Maintenance │───▶│ Token       │
│ Database    │    │ Service     │    │ Monitor     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Cloudflare Integration

Leverage Cloudflare's free tier to enhance the VPS setup:

| Cloudflare Feature | Implementation | Benefit |
|--------------------|----------------|--------|
| CDN Caching | Cache static content | Reduce bandwidth usage |
| SSL Certificates | Enable HTTPS | Secure connections |
| DDoS Protection | Basic protection | Prevent service disruption |
| DNS Management | Configure DNS records | Simplified domain management |

## Monitoring and Optimization

| Component | Implementation | Related Files |
|-----------|----------------|--------------|
| Job Monitoring | Track job execution and performance | `src/monitoring/job_monitor.py` |
| Resource Usage | Monitor system resource usage | `src/monitoring/resource_monitor.py` |
| Error Tracking | Log and alert on scraping errors | `src/utils/error_handling.py` |
| Performance Metrics | Track scraping efficiency | `src/monitoring/metrics.py` |

### Key Metrics to Track:

1. Articles scraped per job
2. Processing time per article
3. Database growth rate
4. Error rate per source
5. Resource usage during scraping
6. Content change frequency per source

## Integration with Existing Components

### File Relationship Rules

When implementing the efficient scraping architecture, follow these relationship rules:

| Primary File | Related Files | Integrity Rule |
|--------------|---------------|----------------|
| `src/web_scraper/url_discovery_agent.py` | `src/database_management/models.py` | When URL Discovery Agent is updated, ensure it's compatible with the sitemaps table schema. |
| `src/web_scraper/content_extraction_agent.py` | `src/database_management/models.py` | When Content Extraction Agent is updated, ensure it's compatible with the articles table schema. |
| `src/web_scraper/metadata_enhancement_agent.py` | `src/database_management/models.py` | When Metadata Enhancement Agent is updated, ensure it's compatible with the article_metadata table schema. |
| `src/scheduler/job_scheduler.py` | `src/web_scraper/url_discovery_agent.py` | When scheduler is updated, ensure URL Discovery Agent is compatible with the scheduling approach. |
| `src/scheduler/job_scheduler.py` | `src/web_scraper/content_extraction_agent.py` | When scheduler is updated, ensure Content Extraction Agent is compatible with the scheduling approach. |
| `src/utils/compression.py` | `src/database_management/models.py` | When compression utilities are updated, ensure database models handle compressed content correctly. |
| `src/utils/hash_utils.py` | `src/web_scraper/url_discovery_agent.py` | When hash utilities are updated, ensure URL Discovery Agent uses the correct hashing methods. |
| `src/services/archive_service.py` | `src/database_management/models.py` | When archive service is updated, ensure database models support archiving functionality. |
| `src/services/maintenance_service.py` | `docs/dev/database-schema.md` | When maintenance service is updated, ensure database schema documentation reflects maintenance operations. |

## Implementation Checklist

When implementing the efficient scraping architecture:

### 1. Centralized Agent Architecture
- [ ] Implement Agent-1: URL Discovery with GPT-4o-mini
- [ ] Implement Agent-2: Content Extraction with GPT-4o
- [ ] Implement Agent-3: Metadata Enhancement with GPT-4o-mini
- [ ] Create sitemaps table for agent workflow coordination
- [ ] Implement batch processing for websites
- [ ] Add domain-based rate limiting
- [ ] Implement agent monitoring and error handling
- [ ] Optimize token usage for cost efficiency

### 2. Scheduled Batch Processing
- [ ] Create scheduler component with configurable job frequency per source
- [ ] Implement job queue for managing scraping tasks
- [ ] Configure cron jobs to run during off-peak hours
- [ ] Add job prioritization based on source update frequency
- [ ] Implement job status tracking and reporting

### 2. Intelligent Crawling
- [ ] Implement ETag/Last-Modified header checking
- [ ] Add content hashing to detect actual changes
- [ ] Create URL fingerprinting system to track processed URLs
- [ ] Implement robots.txt compliance
- [ ] Add rate limiting per domain to avoid overloading sources

### 3. Content Compression
- [ ] Implement text compression for article storage
- [ ] Configure PostgreSQL for compressed text columns
- [ ] Optimize database schema for text-only content
- [ ] Add compression metrics to track storage efficiency
- [ ] Implement efficient text indexing for search functionality

### 4. Data Retention Policies
- [ ] Define retention periods for different content types
- [ ] Create archiving system for older content
- [ ] Implement database partitioning for efficient archiving
- [ ] Add scheduled maintenance jobs for data cleanup
- [ ] Create data growth monitoring and alerting

### 5. Compute/Storage Separation
- [ ] Design stateless scraping components
- [ ] Implement connection pooling for database access
- [ ] Configure environment-based settings for deployment flexibility
- [ ] Create resource usage monitoring
- [ ] Implement graceful scaling for increased load

### 6. Monitoring and Maintenance
- [ ] Set up comprehensive logging for all operations
- [ ] Create performance metrics tracking
- [ ] Implement error detection and reporting
- [ ] Add system health monitoring
- [ ] Create automated database maintenance routines

## Conclusion

This efficient scraping architecture is designed to minimize resource usage while maintaining scalability for text-only news scraping. Our analysis shows that for scraping up to 5 news sources with text-only content, a standard VPS ($20-25/month) from providers like Hostinger or Ionos, combined with Cloudflare's free tier, offers the most cost-effective solution compared to cloud services like AWS or Google Cloud.

By implementing the six core principles:

1. **Centralized agent architecture** with task-specific AI agents
2. **Scheduled batch processing** instead of continuous scraping
3. **Intelligent crawling** to only process changed content
4. **Content compression** to minimize storage requirements
5. **Data retention policies** to manage growth over time
6. **Separation of compute and storage concerns** for flexibility

We can build a highly efficient scraping system that runs well within the resource constraints of a standard VPS while maintaining the ability to scale if requirements change in the future.

This approach provides several advantages over cloud services for our specific use case:
- Simpler architecture and deployment
- More predictable monthly costs
- Sufficient resources for text-only content
- Lower overall cost for the required functionality
- Easier maintenance and monitoring

Last Updated: 2024-05-16
