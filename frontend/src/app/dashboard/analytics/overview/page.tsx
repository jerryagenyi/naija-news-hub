'use client';

import React from 'react';
import { FiBarChart2, FiPieChart, FiCalendar, FiTrendingUp, FiTrendingDown } from 'react-icons/fi';

// Simple component for stat cards
const StatCard = ({ title, value, icon: Icon, trend, trendValue }: {
  title: string;
  value: string | number;
  icon: React.ElementType;
  trend: 'up' | 'down' | 'neutral';
  trendValue: string;
}) => (
  <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
    <div className="flex items-center justify-between mb-4">
      <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">{title}</h3>
      <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
        <Icon className="w-5 h-5 text-blue-500 dark:text-blue-400" />
      </div>
    </div>
    <div className="text-3xl font-bold text-gray-900 dark:text-white mb-2">{value}</div>
    <div className={`flex items-center text-sm ${
      trend === 'up' ? 'text-green-600 dark:text-green-400' :
      trend === 'down' ? 'text-red-600 dark:text-red-400' :
      'text-gray-500 dark:text-gray-400'
    }`}>
      {trend === 'up' ? <FiTrendingUp className="mr-1" /> :
       trend === 'down' ? <FiTrendingDown className="mr-1" /> :
       null}
      {trendValue}
    </div>
  </div>
);

// Mock chart component
const MockChart = ({ title, type }: { title: string; type: 'bar' | 'pie' | 'line' }) => (
  <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
    <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4">{title}</h3>
    <div className="flex items-center justify-center h-64 bg-gray-50 dark:bg-gray-800 rounded-lg">
      {type === 'bar' && <FiBarChart2 className="w-12 h-12 text-blue-500 dark:text-blue-400" />}
      {type === 'pie' && <FiPieChart className="w-12 h-12 text-blue-500 dark:text-blue-400" />}
      {type === 'line' && <FiTrendingUp className="w-12 h-12 text-blue-500 dark:text-blue-400" />}
      <span className="ml-2 text-gray-500 dark:text-gray-400">Chart visualization will appear here</span>
    </div>
  </div>
);

// Hardcoded category distribution data
const categoryDistribution = [
  { name: 'Politics', count: 45, percentage: 30 },
  { name: 'Technology', count: 30, percentage: 20 },
  { name: 'Sports', count: 25, percentage: 17 },
  { name: 'Entertainment', count: 20, percentage: 13 },
  { name: 'Health', count: 15, percentage: 10 },
  { name: 'Business', count: 15, percentage: 10 },
];

export default function AnalyticsOverviewPage() {
  // Hardcoded stats
  const stats = {
    totalArticles: 150,
    articlesThisWeek: 28,
    topCategory: 'Politics',
    averageArticlesPerDay: 4.2
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Analytics Overview
      </h1>

      {/* Stats cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Total Articles"
          value={stats.totalArticles}
          icon={FiBarChart2}
          trend="up"
          trendValue="15% increase"
        />
        <StatCard
          title="Articles This Week"
          value={stats.articlesThisWeek}
          icon={FiCalendar}
          trend="up"
          trendValue="5 more than last week"
        />
        <StatCard
          title="Top Category"
          value={stats.topCategory}
          icon={FiPieChart}
          trend="neutral"
          trendValue="No change"
        />
        <StatCard
          title="Avg. Articles/Day"
          value={stats.averageArticlesPerDay}
          icon={FiTrendingUp}
          trend="up"
          trendValue="0.8 more than last week"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <MockChart title="Articles by Category" type="pie" />
        <MockChart title="Articles Published Over Time" type="line" />
      </div>

      {/* Category distribution */}
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4">
          Category Distribution
        </h3>
        <div className="space-y-4">
          {categoryDistribution.map(category => (
            <div key={category.name}>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {category.name}
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {category.count} articles ({category.percentage}%)
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                <div
                  className="bg-blue-600 h-2.5 rounded-full"
                  style={{ width: `${category.percentage}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
