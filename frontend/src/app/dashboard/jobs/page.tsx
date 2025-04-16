'use client';

import { useState, useEffect } from 'react';
import { FiPlay, FiPause, FiStopCircle, FiRefreshCw, FiEye } from 'react-icons/fi';

interface Job {
  id: number;
  websiteName: string;
  websiteId: number;
  status: 'running' | 'paused' | 'completed' | 'failed';
  progress: number;
  startTime: Date;
  endTime: Date | null;
  articlesFound: number;
  articlesProcessed: number;
  errors: number;
}

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filter, setFilter] = useState<'all' | 'running' | 'paused' | 'completed' | 'failed'>('all');

  // Fetch jobs (mock data for now)
  useEffect(() => {
    // This would be replaced with an API call
    setJobs([
      {
        id: 1,
        websiteName: 'Punch News',
        websiteId: 1,
        status: 'running',
        progress: 75,
        startTime: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
        endTime: null,
        articlesFound: 120,
        articlesProcessed: 90,
        errors: 0,
      },
      {
        id: 2,
        websiteName: 'Vanguard News',
        websiteId: 2,
        status: 'running',
        progress: 45,
        startTime: new Date(Date.now() - 1000 * 60 * 15), // 15 minutes ago
        endTime: null,
        articlesFound: 85,
        articlesProcessed: 38,
        errors: 2,
      },
      {
        id: 3,
        websiteName: 'ThisDay',
        websiteId: 3,
        status: 'paused',
        progress: 30,
        startTime: new Date(Date.now() - 1000 * 60 * 60), // 1 hour ago
        endTime: new Date(Date.now() - 1000 * 60 * 45), // 45 minutes ago
        articlesFound: 50,
        articlesProcessed: 15,
        errors: 1,
      },
      {
        id: 4,
        websiteName: 'The Nation',
        websiteId: 4,
        status: 'completed',
        progress: 100,
        startTime: new Date(Date.now() - 1000 * 60 * 120), // 2 hours ago
        endTime: new Date(Date.now() - 1000 * 60 * 90), // 1.5 hours ago
        articlesFound: 75,
        articlesProcessed: 75,
        errors: 0,
      },
      {
        id: 5,
        websiteName: 'Daily Trust',
        websiteId: 5,
        status: 'failed',
        progress: 10,
        startTime: new Date(Date.now() - 1000 * 60 * 180), // 3 hours ago
        endTime: new Date(Date.now() - 1000 * 60 * 175), // 2.9 hours ago
        articlesFound: 20,
        articlesProcessed: 2,
        errors: 5,
      },
    ]);
  }, []);

  const filteredJobs = filter === 'all' ? jobs : jobs.filter(job => job.status === filter);

  const handleJobAction = (id: number, action: 'start' | 'pause' | 'stop' | 'restart') => {
    // This would trigger an API call to control the job
    alert(`${action} job ${id}`);
    
    // Update local state for demo purposes
    if (action === 'start') {
      setJobs(jobs.map(job => job.id === id ? {...job, status: 'running'} : job));
    } else if (action === 'pause') {
      setJobs(jobs.map(job => job.id === id ? {...job, status: 'paused'} : job));
    } else if (action === 'stop') {
      setJobs(jobs.map(job => job.id === id ? {...job, status: 'completed', progress: 100, endTime: new Date()} : job));
    } else if (action === 'restart') {
      setJobs(jobs.map(job => job.id === id ? {...job, status: 'running', progress: 0, startTime: new Date(), endTime: null} : job));
    }
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Scraping Jobs
        </h1>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Monitor and control scraping jobs
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-3 py-1 rounded-full text-sm ${
            filter === 'all'
              ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
              : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('running')}
          className={`px-3 py-1 rounded-full text-sm ${
            filter === 'running'
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
              : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
          }`}
        >
          Running
        </button>
        <button
          onClick={() => setFilter('paused')}
          className={`px-3 py-1 rounded-full text-sm ${
            filter === 'paused'
              ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
              : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
          }`}
        >
          Paused
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-3 py-1 rounded-full text-sm ${
            filter === 'completed'
              ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300'
              : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
          }`}
        >
          Completed
        </button>
        <button
          onClick={() => setFilter('failed')}
          className={`px-3 py-1 rounded-full text-sm ${
            filter === 'failed'
              ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
              : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
          }`}
        >
          Failed
        </button>
      </div>

      {/* Jobs list */}
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Website
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Progress
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Started
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Articles
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Errors
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
            {filteredJobs.map((job) => (
              <tr key={job.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900 dark:text-white">
                    {job.websiteName}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      job.status === 'running'
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                        : job.status === 'paused'
                        ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
                        : job.status === 'completed'
                        ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
                        : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                    }`}
                  >
                    {job.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                    <div
                      className={`h-2.5 rounded-full ${
                        job.status === 'failed'
                          ? 'bg-red-600'
                          : 'bg-blue-600'
                      }`}
                      style={{ width: `${job.progress}%` }}
                    ></div>
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {job.progress}%
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    {job.startTime.toLocaleString()}
                  </div>
                  {job.endTime && (
                    <div className="text-xs text-gray-400 dark:text-gray-500">
                      Ended: {job.endTime.toLocaleString()}
                    </div>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900 dark:text-white">
                    {job.articlesProcessed} / {job.articlesFound}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {Math.round((job.articlesProcessed / job.articlesFound) * 100) || 0}% processed
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  <span className={job.errors > 0 ? 'text-red-600 dark:text-red-400' : ''}>
                    {job.errors}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end gap-2">
                    {job.status === 'running' && (
                      <>
                        <button
                          onClick={() => handleJobAction(job.id, 'pause')}
                          className="text-yellow-600 hover:text-yellow-900 dark:text-yellow-400 dark:hover:text-yellow-300"
                          title="Pause"
                        >
                          <FiPause className="w-5 h-5" />
                        </button>
                        <button
                          onClick={() => handleJobAction(job.id, 'stop')}
                          className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                          title="Stop"
                        >
                          <FiStopCircle className="w-5 h-5" />
                        </button>
                      </>
                    )}
                    {job.status === 'paused' && (
                      <button
                        onClick={() => handleJobAction(job.id, 'start')}
                        className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                        title="Resume"
                      >
                        <FiPlay className="w-5 h-5" />
                      </button>
                    )}
                    {(job.status === 'completed' || job.status === 'failed') && (
                      <button
                        onClick={() => handleJobAction(job.id, 'restart')}
                        className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                        title="Restart"
                      >
                        <FiRefreshCw className="w-5 h-5" />
                      </button>
                    )}
                    <button
                      className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300"
                      title="View Details"
                    >
                      <FiEye className="w-5 h-5" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
