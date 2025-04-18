'use client';

import React from 'react';
import {
  FiServer,
  FiDatabase,
  FiCpu,
  FiHardDrive,
  FiActivity,
  FiCheckCircle,
  FiAlertTriangle,
  FiXCircle,
  FiRefreshCw
} from 'react-icons/fi';

export default function SystemStatusPage() {
  // Sample services data
  const services = [
    { id: 'api', name: 'API Server', status: 'operational', uptime: '14d 5h' },
    { id: 'scraper', name: 'Web Scraper', status: 'operational', uptime: '10d 12h' },
    { id: 'database', name: 'Database', status: 'operational', uptime: '30d 0h' },
    { id: 'search', name: 'Search Engine', status: 'degraded', uptime: '5d 8h', lastIncident: 'Apr 17, 2025, 10:30 AM' },
    { id: 'storage', name: 'Storage Service', status: 'operational', uptime: '20d 3h' },
    { id: 'scheduler', name: 'Task Scheduler', status: 'outage', uptime: 'Down', lastIncident: 'Apr 18, 2025, 2:15 PM' },
  ];

  // Sample resources data
  const resources = [
    { id: 'cpu', name: 'CPU', usage: 23, total: '8 cores', used: '1.84 cores' },
    { id: 'memory', name: 'Memory', usage: 45, total: '16 GB', used: '7.2 GB' },
    { id: 'disk', name: 'Disk', usage: 68, total: '500 GB', used: '340 GB' },
    { id: 'network', name: 'Network', usage: 12, total: '1 Gbps', used: '120 Mbps' },
  ];

  // Get status color and class
  const getStatusInfo = (status: string) => {
    switch (status) {
      case 'operational':
        return {
          color: 'text-green-500 dark:text-green-400',
          bgColor: 'bg-green-100 dark:bg-green-900/20',
          icon: FiCheckCircle
        };
      case 'degraded':
        return {
          color: 'text-yellow-500 dark:text-yellow-400',
          bgColor: 'bg-yellow-100 dark:bg-yellow-900/20',
          icon: FiAlertTriangle
        };
      case 'outage':
        return {
          color: 'text-red-500 dark:text-red-400',
          bgColor: 'bg-red-100 dark:bg-red-900/20',
          icon: FiXCircle
        };
      default:
        return {
          color: 'text-gray-500 dark:text-gray-400',
          bgColor: 'bg-gray-100 dark:bg-gray-900/20',
          icon: FiActivity
        };
    }
  };

  // Get resource usage color
  const getResourceUsageColor = (usage: number) => {
    if (usage < 50) {
      return 'bg-green-500';
    } else if (usage < 80) {
      return 'bg-yellow-500';
    } else {
      return 'bg-red-500';
    }
  };

  return (
    <div className="p-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 md:mb-0">
          System Status
        </h1>
        <div className="flex items-center">
          <span className="text-sm text-gray-500 dark:text-gray-400 mr-4">
            Last updated: Apr 18, 2025, 3:45 PM
          </span>
          <button
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          >
            <FiRefreshCw className="mr-2" />
            Refresh
          </button>
        </div>
      </div>

      {/* System overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <div className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-lg mr-4">
              <FiServer className="w-6 h-6 text-blue-500 dark:text-blue-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Services</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                4 of 6 operational
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <div className="p-3 bg-green-100 dark:bg-green-900/20 rounded-lg mr-4">
              <FiCpu className="w-6 h-6 text-green-500 dark:text-green-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">CPU</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                23.0% usage
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <div className="p-3 bg-purple-100 dark:bg-purple-900/20 rounded-lg mr-4">
              <FiDatabase className="w-6 h-6 text-purple-500 dark:text-purple-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Memory</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                45.0% usage
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <div className="p-3 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg mr-4">
              <FiHardDrive className="w-6 h-6 text-yellow-500 dark:text-yellow-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Disk</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                68.0% usage
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Services status */}
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow overflow-hidden mb-6">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Services Status</h2>
        </div>
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {services.map((service) => {
            const { color, bgColor, icon: StatusIcon } = getStatusInfo(service.status);
            return (
              <div key={service.id} className="px-6 py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className={`p-2 ${bgColor} rounded-lg mr-4`}>
                      <FiActivity className={`w-5 h-5 ${color}`} />
                    </div>
                    <div>
                      <h3 className="text-md font-medium text-gray-900 dark:text-white">{service.name}</h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        Uptime: {service.uptime}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <StatusIcon className={`w-5 h-5 ${color} mr-2`} />
                    <span className={`text-sm font-medium ${color}`}>
                      {service.status.charAt(0).toUpperCase() + service.status.slice(1)}
                    </span>
                  </div>
                </div>
                {service.lastIncident && (
                  <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                    Last incident: {service.lastIncident}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Resource usage */}
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Resource Usage</h2>
        </div>
        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          {resources.map((resource) => {
            const usageColor = getResourceUsageColor(resource.usage);
            return (
              <div key={resource.id} className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                <div className="flex justify-between mb-2">
                  <h3 className="text-md font-medium text-gray-900 dark:text-white">{resource.name}</h3>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {resource.usage.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700 mb-2">
                  <div
                    className={`${usageColor} h-2.5 rounded-full`}
                    style={{ width: `${resource.usage}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
                  <span>Used: {resource.used}</span>
                  <span>Total: {resource.total}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
