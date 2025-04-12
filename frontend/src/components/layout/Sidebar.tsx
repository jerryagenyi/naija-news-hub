'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  FiHome,
  FiNewspaper,
  FiGlobe,
  FiClock,
  FiAlertCircle,
  FiSettings,
  FiChevronDown,
  FiChevronRight,
} from 'react-icons/fi';

interface SidebarProps {
  isOpen: boolean;
}

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  items?: { name: string; href: string }[];
}

const navigation: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: FiHome },
  { name: 'Articles', href: '/dashboard/articles', icon: FiNewspaper },
  { name: 'Websites', href: '/dashboard/websites', icon: FiGlobe },
  { name: 'Jobs', href: '/dashboard/jobs', icon: FiClock },
  { name: 'Errors', href: '/dashboard/errors', icon: FiAlertCircle },
  { name: 'Settings', href: '/dashboard/settings', icon: FiSettings },
];

export default function Sidebar({ isOpen }: SidebarProps) {
  const pathname = usePathname();
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const toggleExpand = (name: string) => {
    setExpandedItems((prev) =>
      prev.includes(name)
        ? prev.filter((item) => item !== name)
        : [...prev, name]
    );
  };

  const isActive = (href: string) => pathname === href;

  return (
    <aside
      className={`fixed top-16 left-0 z-40 h-[calc(100vh-4rem)] w-64 transform transition-transform duration-300 ease-in-out bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      <div className="h-full px-3 py-4 overflow-y-auto">
        <nav className="space-y-1">
          {navigation.map((item) => {
            const isItemActive = isActive(item.href);
            const isExpanded = expandedItems.includes(item.name);

            return (
              <div key={item.name}>
                <Link
                  href={item.href}
                  className={`flex items-center justify-between px-3 py-2 rounded-lg transition-colors ${
                    isItemActive
                      ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  <div className="flex items-center">
                    <item.icon
                      className={`w-5 h-5 mr-3 ${
                        isItemActive
                          ? 'text-blue-600 dark:text-blue-400'
                          : 'text-gray-400 dark:text-gray-500'
                      }`}
                    />
                    <span className="text-sm font-medium">{item.name}</span>
                  </div>
                  {item.items && (
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        toggleExpand(item.name);
                      }}
                      className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
                    >
                      {isExpanded ? (
                        <FiChevronDown className="w-4 h-4" />
                      ) : (
                        <FiChevronRight className="w-4 h-4" />
                      )}
                    </button>
                  )}
                </Link>
                {item.items && isExpanded && (
                  <div className="mt-1 ml-8 space-y-1">
                    {item.items.map((subItem) => (
                      <Link
                        key={subItem.href}
                        href={subItem.href}
                        className={`block px-3 py-2 rounded-lg text-sm ${
                          isActive(subItem.href)
                            ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                        }`}
                      >
                        {subItem.name}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </div>
    </aside>
  );
} 