'use client';

import React, { useEffect, useState } from 'react';
import { useArticles, Article } from '@/contexts/ApiContext';
import { FiEye, FiShare2, FiClock, FiCalendar, FiBarChart2 } from 'react-icons/fi';

// Mock engagement data for articles
interface ArticleEngagement {
  views: number;
  shares: number;
  avgReadTime: number; // in seconds
}

// Generate mock engagement data for an article
const generateMockEngagement = (articleId: number): ArticleEngagement => {
  // Use the article ID as a seed for consistent random values
  const seed = articleId * 1000;
  return {
    views: Math.floor((seed % 1000) + 500), // 500-1500 views
    shares: Math.floor((seed % 100) + 20),  // 20-120 shares
    avgReadTime: Math.floor((seed % 180) + 60) // 60-240 seconds
  };
};

// Format time in seconds to minutes and seconds
const formatReadTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}m ${remainingSeconds}s`;
};

export default function ContentAnalyticsPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [articleEngagement, setArticleEngagement] = useState<Record<number, ArticleEngagement>>({});
  const [sortBy, setSortBy] = useState<'views' | 'shares' | 'readTime'>('views');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Get the API hooks
  const fetchArticles = useArticles({ limit: 15 }); // Get all articles for analytics

  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  // Load articles and generate engagement data
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        
        // Load articles
        const articlesResponse = await fetchArticles();
        setArticles(articlesResponse.data);
        
        // Generate mock engagement data for each article
        const engagementData: Record<number, ArticleEngagement> = {};
        articlesResponse.data.forEach(article => {
          engagementData[article.id] = generateMockEngagement(article.id);
        });
        
        setArticleEngagement(engagementData);
        setError(null);
      } catch (err) {
        setError('Failed to fetch content analytics data');
        console.error('Error fetching content analytics data:', err);
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [fetchArticles]);

  // Sort articles based on engagement metrics
  const sortedArticles = [...articles].sort((a, b) => {
    const engagementA = articleEngagement[a.id] || { views: 0, shares: 0, avgReadTime: 0 };
    const engagementB = articleEngagement[b.id] || { views: 0, shares: 0, avgReadTime: 0 };
    
    let comparison = 0;
    if (sortBy === 'views') {
      comparison = engagementA.views - engagementB.views;
    } else if (sortBy === 'shares') {
      comparison = engagementA.shares - engagementB.shares;
    } else if (sortBy === 'readTime') {
      comparison = engagementA.avgReadTime - engagementB.avgReadTime;
    }
    
    return sortOrder === 'asc' ? comparison : -comparison;
  });

  // Handle sort change
  const handleSortChange = (metric: 'views' | 'shares' | 'readTime') => {
    if (sortBy === metric) {
      // Toggle sort order if clicking the same metric
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      // Set new metric and default to descending order
      setSortBy(metric);
      setSortOrder('desc');
    }
  };

  // Calculate total engagement
  const totalEngagement = Object.values(articleEngagement).reduce(
    (acc, curr) => ({
      views: acc.views + curr.views,
      shares: acc.shares + curr.shares,
      avgReadTime: acc.avgReadTime + curr.avgReadTime / Object.keys(articleEngagement).length
    }),
    { views: 0, shares: 0, avgReadTime: 0 }
  );

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Content Analytics
      </h1>

      {loading ? (
        <div className="flex justify-center items-center p-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      ) : error ? (
        <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-md mb-4">
          {error}
        </div>
      ) : (
        <>
          {/* Engagement summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
              <div className="flex items-center mb-2">
                <FiEye className="w-5 h-5 text-blue-500 dark:text-blue-400 mr-2" />
                <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Total Views</h3>
              </div>
              <div className="text-3xl font-bold text-gray-900 dark:text-white">
                {totalEngagement.views.toLocaleString()}
              </div>
            </div>
            
            <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
              <div className="flex items-center mb-2">
                <FiShare2 className="w-5 h-5 text-green-500 dark:text-green-400 mr-2" />
                <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Total Shares</h3>
              </div>
              <div className="text-3xl font-bold text-gray-900 dark:text-white">
                {totalEngagement.shares.toLocaleString()}
              </div>
            </div>
            
            <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
              <div className="flex items-center mb-2">
                <FiClock className="w-5 h-5 text-purple-500 dark:text-purple-400 mr-2" />
                <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Avg. Read Time</h3>
              </div>
              <div className="text-3xl font-bold text-gray-900 dark:text-white">
                {formatReadTime(Math.round(totalEngagement.avgReadTime))}
              </div>
            </div>
          </div>

          {/* Content performance chart placeholder */}
          <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4">
              Content Performance Over Time
            </h3>
            <div className="flex items-center justify-center h-64 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <FiBarChart2 className="w-12 h-12 text-blue-500 dark:text-blue-400" />
              <span className="ml-2 text-gray-500 dark:text-gray-400">Performance chart will appear here</span>
            </div>
          </div>

          {/* Article performance table */}
          <div className="bg-white dark:bg-gray-900 rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">
                Article Performance
              </h3>
            </div>
            
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Article
                    </th>
                    <th 
                      scope="col" 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer"
                      onClick={() => handleSortChange('views')}
                    >
                      <div className="flex items-center">
                        <FiEye className="mr-1" />
                        Views
                        {sortBy === 'views' && (
                          <span className="ml-1">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                        )}
                      </div>
                    </th>
                    <th 
                      scope="col" 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer"
                      onClick={() => handleSortChange('shares')}
                    >
                      <div className="flex items-center">
                        <FiShare2 className="mr-1" />
                        Shares
                        {sortBy === 'shares' && (
                          <span className="ml-1">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                        )}
                      </div>
                    </th>
                    <th 
                      scope="col" 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer"
                      onClick={() => handleSortChange('readTime')}
                    >
                      <div className="flex items-center">
                        <FiClock className="mr-1" />
                        Avg. Read Time
                        {sortBy === 'readTime' && (
                          <span className="ml-1">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                        )}
                      </div>
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      <div className="flex items-center">
                        <FiCalendar className="mr-1" />
                        Published
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                  {sortedArticles.map((article) => {
                    const engagement = articleEngagement[article.id] || { views: 0, shares: 0, avgReadTime: 0 };
                    return (
                      <tr key={article.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                        <td className="px-6 py-4">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {article.title}
                          </div>
                          <div className="text-sm text-gray-500 dark:text-gray-400">
                            {article.category}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {engagement.views.toLocaleString()}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {engagement.shares.toLocaleString()}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {formatReadTime(engagement.avgReadTime)}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {formatDate(article.publishedAt)}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
