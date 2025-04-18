'use client';

import React, { useState, useEffect } from 'react';
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

// Types for system status
type ServiceStatus = 'operational' | 'degraded' | 'outage';

interface SystemService {
  id: string;
  name: string;
  status: ServiceStatus;
  uptime: number; // in seconds
  lastIncident?: string; // ISO date string
}

interface SystemResource {
  id: string;
  name: string;
  usage: number; // percentage
  total: string;
  used: string;
}

// Mock data for system services
const mockServices: SystemService[] = [
  {
    id: 'api',
    name: 'API Server',
    status: 'operational',
    uptime: 1209600, // 14 days
  },
  {
    id: 'scraper',
    name: 'Web Scraper',
    status: 'operational',
    uptime: 864000, // 10 days
  },
  {
    id: 'database',
    name: 'Database',
    status: 'operational',
    uptime: 2592000, // 30 days
  },
  {
    id: 'search',
    name: 'Search Engine',
    status: 'degraded',
    uptime: 432000, // 5 days
    lastIncident: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
  },
  {
    id: 'storage',
    name: 'Storage Service',
    status: 'operational',
    uptime: 1728000, // 20 days
  },
  {
    id: 'scheduler',
    name: 'Task Scheduler',
    status: 'outage',
    uptime: 0,
    lastIncident: new Date().toISOString(),
  },
];

// Mock data for system resources
const mockResources: SystemResource[] = [
  {
    id: 'cpu',
    name: 'CPU',
    usage: 23,
    total: '8 cores',
    used: '1.84 cores',
  },
  {
    id: 'memory',
    name: 'Memory',
    usage: 45,
    total: '16 GB',
    used: '7.2 GB',
  },
  {
    id: 'disk',
    name: 'Disk',
    usage: 68,
    total: '500 GB',
    used: '340 GB',
  },
  {
    id: 'network',
    name: 'Network',
    usage: 12,
    total: '1 Gbps',
    used: '120 Mbps',
  },
];

// Format uptime in seconds to a human-readable string
const formatUptime = (seconds: number): string => {
  if (seconds === 0) return 'Down';
  
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  if (days > 0) {
    return `${days}d ${hours}h`;
  } else if (hours > 0) {
    return `${hours}h ${minutes}m`;
  } else {
    return `${minutes}m`;
  }
};

// Get status color and icon
const getStatusInfo = (status: ServiceStatus) => {
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

export default function SystemStatusPage() {
  const [services, setServices] = useState<SystemService[]>(mockServices);
  const [resources, setResources] = useState<SystemResource[]>(mockResources);
  const [loading, setLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

  // Simulate refreshing the data
  const refreshData = () => {
    setLoading(true);
    
    // Simulate API call delay
    setTimeout(() => {
      // Update with slightly different values to simulate real-time changes
      const updatedResources = resources.map(resource => ({
        ...resource,
        usage: Math.min(100, Math.max(0, resource.usage + (Math.random() * 10 - 5))),
        used: `${(resource.usage / 100 * parseFloat(resource.total.split(' ')[0])).toFixed(1)} ${resource.total.split(' ')[1]}`
      }));
      
      setResources(updatedResources);
      setLastUpdated(new Date());
      setLoading(false);
    }, 1000);
  };

  // Format date for display
  const formatDate = (date: Date) => {
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="p-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 md:mb-0">
          System Status
        </h1>
        <div className="flex items-center">
          <span className="text-sm text-gray-500 dark:text-gray-400 mr-4">
            Last updated: {formatDate(lastUpdated)}
          </span>
          <button 
            onClick={refreshData}
            disabled={loading}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:bg-blue-400 disabled:cursor-not-allowed"
          >
            <FiRefreshCw className={`mr-2 ${loading ? 'animate-spin' : ''}`} />
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
                {services.filter(s => s.status === 'operational').length} of {services.length} operational
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
                {resources.find(r => r.id === 'cpu')?.usage.toFixed(1)}% usage
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
                {resources.find(r => r.id === 'memory')?.usage.toFixed(1)}% usage
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
                {resources.find(r => r.id === 'disk')?.usage.toFixed(1)}% usage
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
                        Uptime: {formatUptime(service.uptime)}
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
                    Last incident: {new Date(service.lastIncident).toLocaleString()}
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
