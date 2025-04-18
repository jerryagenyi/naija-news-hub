'use client';

import React from 'react';
import { FiEye, FiShare2, FiClock, FiCalendar, FiBarChart2 } from 'react-icons/fi';

// Format time in seconds to minutes and seconds
const formatReadTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}m ${remainingSeconds}s`;
};

export default function ContentAnalyticsPage() {
  // Sample article data
  const sampleArticles = [
    { id: 1, title: 'The Future of AI in Nigeria', category: 'Technology', publishedAt: '2024-04-15T10:00:00Z', views: 1250, shares: 85, readTime: 180 },
    { id: 2, title: 'Economic Outlook for 2025', category: 'Economy', publishedAt: '2024-04-14T14:30:00Z', views: 980, shares: 62, readTime: 210 },
    { id: 3, title: 'Latest Political Developments', category: 'Politics', publishedAt: '2024-04-13T09:15:00Z', views: 1500, shares: 120, readTime: 150 },
    { id: 4, title: 'Sports Highlights of the Week', category: 'Sports', publishedAt: '2024-04-12T16:45:00Z', views: 850, shares: 45, readTime: 120 },
    { id: 5, title: 'Health Tips for the Rainy Season', category: 'Health', publishedAt: '2024-04-11T11:20:00Z', views: 720, shares: 38, readTime: 165 },
  ];

  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  // Calculate total engagement
  const totalViews = sampleArticles.reduce((sum, article) => sum + article.views, 0);
  const totalShares = sampleArticles.reduce((sum, article) => sum + article.shares, 0);
  const avgReadTime = Math.round(sampleArticles.reduce((sum, article) => sum + article.readTime, 0) / sampleArticles.length);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Content Analytics
      </h1>

      {/* Engagement summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center mb-2">
            <FiEye className="w-5 h-5 text-blue-500 dark:text-blue-400 mr-2" />
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Total Views</h3>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white">
            {totalViews.toLocaleString()}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center mb-2">
            <FiShare2 className="w-5 h-5 text-green-500 dark:text-green-400 mr-2" />
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Total Shares</h3>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white">
            {totalShares.toLocaleString()}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center mb-2">
            <FiClock className="w-5 h-5 text-purple-500 dark:text-purple-400 mr-2" />
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Avg. Read Time</h3>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white">
            {formatReadTime(avgReadTime)}
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
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  <div className="flex items-center">
                    <FiEye className="mr-1" />
                    Views
                  </div>
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  <div className="flex items-center">
                    <FiShare2 className="mr-1" />
                    Shares
                  </div>
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  <div className="flex items-center">
                    <FiClock className="mr-1" />
                    Avg. Read Time
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
              {sampleArticles.map((article) => (
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
                      {article.views.toLocaleString()}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {article.shares.toLocaleString()}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {formatReadTime(article.readTime)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {formatDate(article.publishedAt)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
