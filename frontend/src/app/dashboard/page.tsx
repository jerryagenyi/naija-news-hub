'use client';

import { useState, useEffect } from 'react';
import {
  FiUsers,
  FiNewspaper,
  FiGlobe,
  FiClock,
} from 'react-icons/fi';
import StatsCard from '@/components/dashboard/StatsCard';
import JobStatus from '@/components/dashboard/JobStatus';
import ErrorSummary from '@/components/dashboard/ErrorSummary';

interface DashboardStats {
  totalArticles: number;
  totalWebsites: number;
  activeJobs: number;
  errorCount: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    totalArticles: 0,
    totalWebsites: 0,
    activeJobs: 0,
    errorCount: 0,
  });

  // TODO: Fetch real data from API
  useEffect(() => {
    // Simulated data for now
    setStats({
      totalArticles: 1234,
      totalWebsites: 15,
      activeJobs: 3,
      errorCount: 2,
    });
  }, []);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Overview of your news aggregation system
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Total Articles"
          value={stats.totalArticles.toLocaleString()}
          icon={FiNewspaper}
          trend={+12.5}
        />
        <StatsCard
          title="Active Websites"
          value={stats.totalWebsites.toString()}
          icon={FiGlobe}
          trend={0}
        />
        <StatsCard
          title="Active Jobs"
          value={stats.activeJobs.toString()}
          icon={FiClock}
          trend={-2}
        />
        <StatsCard
          title="Recent Errors"
          value={stats.errorCount.toString()}
          icon={FiUsers}
          trend={+50}
          trendColor="red"
        />
      </div>

      {/* Job status and error summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active jobs */}
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Active Jobs
          </h2>
          <div className="space-y-4">
            <JobStatus
              website="Punch News"
              progress={75}
              status="running"
              startTime={new Date(Date.now() - 1000 * 60 * 30)} // 30 minutes ago
            />
            <JobStatus
              website="Vanguard News"
              progress={45}
              status="running"
              startTime={new Date(Date.now() - 1000 * 60 * 15)} // 15 minutes ago
            />
            <JobStatus
              website="ThisDay"
              progress={90}
              status="running"
              startTime={new Date(Date.now() - 1000 * 60 * 45)} // 45 minutes ago
            />
          </div>
        </div>

        {/* Error summary */}
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Recent Errors
          </h2>
          <ErrorSummary
            errors={[
              {
                id: 1,
                website: 'Punch News',
                type: 'network',
                message: 'Connection timeout',
                timestamp: new Date(Date.now() - 1000 * 60 * 10), // 10 minutes ago
              },
              {
                id: 2,
                website: 'Vanguard News',
                type: 'parsing',
                message: 'Failed to extract article content',
                timestamp: new Date(Date.now() - 1000 * 60 * 25), // 25 minutes ago
              },
            ]}
          />
        </div>
      </div>
    </div>
  );
} 