'use client';

import React from 'react';
import { FiBarChart2, FiPieChart, FiCalendar, FiTrendingUp } from 'react-icons/fi';

export default function AnalyticsOverviewPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Analytics Overview
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Total Articles</h3>
            <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <FiBarChart2 className="w-5 h-5 text-blue-500 dark:text-blue-400" />
            </div>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white mb-2">15</div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Articles This Week</h3>
            <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <FiCalendar className="w-5 h-5 text-blue-500 dark:text-blue-400" />
            </div>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white mb-2">8</div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Top Category</h3>
            <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <FiPieChart className="w-5 h-5 text-blue-500 dark:text-blue-400" />
            </div>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Technology</div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Avg. Articles/Day</h3>
            <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <FiTrendingUp className="w-5 h-5 text-blue-500 dark:text-blue-400" />
            </div>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white mb-2">1.2</div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4">
          Category Distribution
        </h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Technology</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">5 articles (33%)</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '33%' }}></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Politics</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">4 articles (27%)</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '27%' }}></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Sports</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">3 articles (20%)</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '20%' }}></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Entertainment</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">3 articles (20%)</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '20%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
