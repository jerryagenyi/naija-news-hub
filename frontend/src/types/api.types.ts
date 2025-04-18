export interface Article {
  id: number;
  title: string;
  content: string;
  source: string;
  category: string;
  publishedAt: string;
  author: string;
  url: string;
  imageUrl: string;
  tags: string[];
  status: 'published' | 'draft' | 'error';
  readTime: number;
  summary: string;
}

export interface Website {
  id: number;
  name: string;
  url: string;
  status: 'active' | 'inactive' | 'error';
  lastScraped: string;
  articleCount: number;
  errorCount: number;
  scrapingInterval: number;
}

export interface Job {
  id: number;
  type: 'scraping' | 'analysis' | 'cleanup';
  status: 'running' | 'completed' | 'failed' | 'queued';
  progress: number;
  startedAt: string;
  completedAt?: string;
  error?: string;
  websiteId?: number;
  metadata: Record<string, any>;
}

export interface SystemStatus {
  cpuUsage: number;
  memoryUsage: number;
  diskUsage: number;
  activeJobs: number;
  queuedJobs: number;
  lastBackup: string;
  uptime: number;
}

export interface AnalyticsData {
  period: 'day' | 'week' | 'month';
  metrics: {
    articlesScraped: number;
    successRate: number;
    averageProcessingTime: number;
    totalErrors: number;
  };
  timeline: Array<{
    timestamp: string;
    value: number;
    type: string;
  }>;
}

export interface ApiResponse<T> {
  data: T;
  total?: number;
  page?: number;
  pageSize?: number;
  hasMore?: boolean;
  metadata?: Record<string, any>;
} 