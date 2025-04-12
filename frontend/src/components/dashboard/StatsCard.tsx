'use client';

import { FiArrowUp, FiArrowDown } from 'react-icons/fi';

interface StatsCardProps {
  title: string;
  value: string;
  icon: React.ElementType;
  trend: number;
  trendColor?: 'green' | 'red';
}

export default function StatsCard({
  title,
  value,
  icon: Icon,
  trend,
  trendColor = trend >= 0 ? 'green' : 'red',
}: StatsCardProps) {
  return (
    <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
            {title}
          </p>
          <p className="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">
            {value}
          </p>
        </div>
        <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <Icon className="w-6 h-6 text-gray-600 dark:text-gray-400" />
        </div>
      </div>
      {trend !== 0 && (
        <div className="mt-4 flex items-center">
          {trend > 0 ? (
            <FiArrowUp
              className={`w-4 h-4 ${
                trendColor === 'green'
                  ? 'text-green-500'
                  : 'text-red-500'
              }`}
            />
          ) : (
            <FiArrowDown
              className={`w-4 h-4 ${
                trendColor === 'green'
                  ? 'text-green-500'
                  : 'text-red-500'
              }`}
            />
          )}
          <span
            className={`ml-2 text-sm font-medium ${
              trendColor === 'green'
                ? 'text-green-500'
                : 'text-red-500'
            }`}
          >
            {Math.abs(trend)}%
          </span>
          <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">
            from last period
          </span>
        </div>
      )}
    </div>
  );
} 