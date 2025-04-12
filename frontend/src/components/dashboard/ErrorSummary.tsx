'use client';

import { FiAlertCircle } from 'react-icons/fi';

interface Error {
  id: number;
  website: string;
  type: string;
  message: string;
  timestamp: Date;
}

interface ErrorSummaryProps {
  errors: Error[];
}

export default function ErrorSummary({ errors }: ErrorSummaryProps) {
  const getErrorTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'network':
        return 'text-red-500';
      case 'parsing':
        return 'text-yellow-500';
      case 'validation':
        return 'text-orange-500';
      default:
        return 'text-gray-500';
    }
  };

  const getRelativeTime = (timestamp: Date) => {
    const now = new Date();
    const elapsed = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(elapsed / 1000 / 60);

    if (minutes < 1) {
      return 'just now';
    } else if (minutes === 1) {
      return '1 minute ago';
    } else if (minutes < 60) {
      return `${minutes} minutes ago`;
    } else {
      const hours = Math.floor(minutes / 60);
      if (hours === 1) {
        return '1 hour ago';
      } else {
        return `${hours} hours ago`;
      }
    }
  };

  return (
    <div className="space-y-4">
      {errors.length === 0 ? (
        <div className="text-center py-6">
          <FiAlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">No recent errors</p>
        </div>
      ) : (
        errors.map((error) => (
          <div
            key={error.id}
            className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4"
          >
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white">
                  {error.website}
                </h3>
                <p
                  className={`text-sm mt-1 ${getErrorTypeColor(error.type)}`}
                >
                  {error.type.charAt(0).toUpperCase() + error.type.slice(1)} Error
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  {error.message}
                </p>
              </div>
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {getRelativeTime(error.timestamp)}
              </span>
            </div>
          </div>
        ))
      )}
    </div>
  );
} 