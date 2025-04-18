'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  FiHome,
  FiFileText,
  FiGlobe,
  FiClock,
  FiAlertCircle,
  FiSettings,
  FiChevronDown,
  FiChevronRight,
  FiBarChart2,
  FiServer,
  FiHelpCircle,
} from 'react-icons/fi';

interface SidebarProps {
  isOpen: boolean;
}

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  items?: { name: string; href: string }[];
  badge?: {
    text: string;
    color: 'green' | 'blue' | 'red' | 'yellow' | 'purple';
  };
}

const navigation: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: FiHome },
  {
    name: 'Articles',
    href: '/dashboard/articles',
    icon: FiFileText,
    badge: { text: 'New', color: 'green' }
  },
  { name: 'Websites', href: '/dashboard/websites', icon: FiGlobe },
  { name: 'Jobs', href: '/dashboard/jobs', icon: FiClock },
  {
    name: 'Analytics',
    href: '/dashboard/analytics',
    icon: FiBarChart2,
    items: [
      { name: 'Overview', href: '/dashboard/analytics/overview' },
      { name: 'Traffic', href: '/dashboard/analytics/traffic' },
      { name: 'Content', href: '/dashboard/analytics/content' },
    ]
  },
  {
    name: 'System',
    href: '/dashboard/system',
    icon: FiServer,
    items: [
      { name: 'Status', href: '/dashboard/system/status' },
      { name: 'Logs', href: '/dashboard/system/logs' },
      { name: 'Database', href: '/dashboard/system/database' },
    ]
  },
  { name: 'Errors', href: '/dashboard/errors', icon: FiAlertCircle, badge: { text: '2', color: 'red' } },
  { name: 'Settings', href: '/dashboard/settings', icon: FiSettings },
  { name: 'Help', href: '/dashboard/help', icon: FiHelpCircle },
];

export default function Sidebar({ isOpen }: SidebarProps) {
  const pathname = usePathname();

  // Initialize expandedItems based on the current path
  const initialExpandedItems = navigation
    .filter(item => item.items && item.items.some(subItem => pathname?.startsWith(subItem.href)))
    .map(item => item.name);

  const [expandedItems, setExpandedItems] = useState<string[]>(initialExpandedItems);

  const toggleExpand = (name: string) => {
    setExpandedItems((prev) =>
      prev.includes(name)
        ? prev.filter((item) => item !== name)
        : [...prev, name]
    );
  };

  const isActive = (href: string) => pathname === href || pathname?.startsWith(href + '/');

  return (
    <aside
      className={`fixed top-16 left-0 z-40 h-[calc(100vh-4rem)] w-64 transform transition-transform duration-300 ease-in-out bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 shadow-md ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      <div className="h-full flex flex-col">
        {/* Sidebar header */}
        <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Main Navigation
            </h2>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex-1 px-3 py-2 overflow-y-auto">
          <nav className="space-y-1">
            {navigation.map((item) => {
              const isItemActive = isActive(item.href);
              const isExpanded = expandedItems.includes(item.name);

              return (
                <div key={item.name} className="mb-1">
                  <Link
                    href={item.href}
                    className={`flex items-center justify-between px-3 py-2.5 rounded-lg transition-colors ${
                      isItemActive
                        ? 'bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 text-blue-700 dark:text-blue-400 font-medium'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                    onClick={(e) => {
                      if (item.items && item.items.length > 0) {
                        e.preventDefault();
                        toggleExpand(item.name);
                      }
                    }}
                  >
                    <div className="flex items-center">
                      <div
                        className={`w-8 h-8 flex items-center justify-center rounded-md mr-3 ${
                          isItemActive
                            ? 'bg-gradient-to-r from-green-500 to-blue-500 text-white'
                            : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400'
                        }`}
                      >
                        <item.icon className="w-5 h-5" />
                      </div>
                      <span className="text-sm">{item.name}</span>
                    </div>
                    <div className="flex items-center">
                      {item.badge && (
                        <span
                          className={`px-2 py-0.5 text-xs rounded-full mr-2 ${
                            item.badge.color === 'green' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                            item.badge.color === 'red' ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' :
                            item.badge.color === 'blue' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' :
                            item.badge.color === 'yellow' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' :
                            'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400'
                          }`}
                        >
                          {item.badge.text}
                        </span>
                      )}
                      {item.items && (
                        <div className="p-1">
                          {isExpanded ? (
                            <FiChevronDown className="w-4 h-4" />
                          ) : (
                            <FiChevronRight className="w-4 h-4" />
                          )}
                        </div>
                      )}
                    </div>
                  </Link>
                  {item.items && isExpanded && (
                    <div className="mt-1 ml-11 space-y-1 border-l-2 border-gray-200 dark:border-gray-700 pl-2">
                      {item.items.map((subItem) => {
                        const isSubItemActive = isActive(subItem.href);
                        return (
                          <Link
                            key={subItem.href}
                            href={subItem.href}
                            className={`block px-3 py-2 rounded-lg text-sm ${
                              isSubItemActive
                                ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 font-medium'
                                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                            }`}
                          >
                            {subItem.name}
                          </Link>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </nav>
        </div>

        {/* Sidebar footer */}
        <div className="px-3 py-3 border-t border-gray-200 dark:border-gray-800">
          <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-3">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xs font-semibold text-gray-900 dark:text-white">System Status</h3>
              <span className="px-1.5 py-0.5 text-xs rounded-full bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                Online
              </span>
            </div>
            <div className="text-xs text-gray-600 dark:text-gray-400">
              <div className="flex justify-between mb-1">
                <span>CPU</span>
                <span>23%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5 dark:bg-gray-700 mb-2">
                <div className="bg-green-500 h-1.5 rounded-full" style={{ width: '23%' }}></div>
              </div>
              <div className="flex justify-between mb-1">
                <span>Memory</span>
                <span>45%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5 dark:bg-gray-700">
                <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '45%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}