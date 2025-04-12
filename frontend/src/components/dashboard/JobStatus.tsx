'use client';

import { FiClock, FiPlay, FiPause, FiX } from 'react-icons/fi';

interface JobStatusProps {
  website: string;
  progress: number;
  status: 'running' | 'paused' | 'failed';
  startTime: Date;
}

export default function JobStatus({
  website,
  progress,
  status,
  startTime,
}: JobStatusProps) {
  const getStatusColor = () => {
    switch (status) {
      case 'running':
        return 'text-green-500';
      case 'paused':
        return 'text-yellow-500';
      case 'failed':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'running':
        return <FiPlay className={`w-4 h-4 ${getStatusColor()}`} />;
      case 'paused':
        return <FiPause className={`w-4 h-4 ${getStatusColor()}`} />;
      case 'failed':
        return <FiX className={`w-4 h-4 ${getStatusColor()}`} />;
      default:
        return null;
    }
  };

  const getElapsedTime = () => {
    const now = new Date();
    const elapsed = now.getTime() - startTime.getTime();
    const minutes = Math.floor(elapsed / 1000 / 60);
    return `${minutes} min${minutes !== 1 ? 's' : ''}`;
  };

  return (
    <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {getStatusIcon()}
          <span className="font-medium text-gray-900 dark:text-white">
            {website}
          </span>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
          <FiClock className="w-4 h-4" />
          <span>{getElapsedTime()}</span>
        </div>
      </div>
      <div className="relative pt-1">
        <div className="flex mb-2 items-center justify-between">
          <div>
            <span className="text-xs font-semibold inline-block text-gray-600 dark:text-gray-400">
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </span>
          </div>
          <div className="text-right">
            <span className="text-xs font-semibold inline-block text-gray-600 dark:text-gray-400">
              {progress}%
            </span>
          </div>
        </div>
        <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200 dark:bg-gray-700">
          <div
            style={{ width: `${progress}%` }}
            className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${
              status === 'failed'
                ? 'bg-red-500'
                : status === 'paused'
                ? 'bg-yellow-500'
                : 'bg-green-500'
            }`}
          ></div>
        </div>
      </div>
    </div>
  );
} 