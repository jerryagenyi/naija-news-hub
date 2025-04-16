'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useTheme } from 'next-themes';
import {
  FiMenu,
  FiX,
  FiSun,
  FiMoon,
  FiSearch,
  FiUser,
  FiBell,
  FiGlobe,
  FiSettings,
  FiHelpCircle
} from 'react-icons/fi';

interface HeaderProps {
  onToggleSidebar: () => void;
}

export default function Header({ onToggleSidebar }: HeaderProps) {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const { theme, setTheme } = useTheme();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-green-600 to-blue-600 shadow-md">
      <div className="px-4 h-16 flex items-center justify-between">
        {/* Left section */}
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="p-2 text-white hover:bg-white/10 rounded-lg transition-colors"
            aria-label="Toggle sidebar"
          >
            <FiMenu className="w-6 h-6" />
          </button>
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="bg-white p-1 rounded-full">
              <FiGlobe className="w-6 h-6 text-green-600" />
            </div>
            <span className="text-xl font-bold text-white hidden sm:inline">
              Naija News Hub
            </span>
            <span className="text-xl font-bold text-white sm:hidden">
              NNH
            </span>
          </Link>
        </div>

        {/* Center section - Search */}
        <div className="hidden md:flex flex-1 max-w-2xl mx-4">
          <div className="relative w-full">
            <input
              type="text"
              placeholder="Search articles..."
              className="w-full px-4 py-2 pl-10 bg-white/10 border border-white/20 text-white placeholder-white/70 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/50 focus:bg-white/20 transition-all"
            />
            <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-white/70" />
          </div>
        </div>

        {/* Right section */}
        <div className="flex items-center gap-1 sm:gap-2">
          {/* Mobile search button */}
          <button
            onClick={() => setIsSearchOpen(!isSearchOpen)}
            className="md:hidden p-2 text-white hover:bg-white/10 rounded-lg transition-colors"
            aria-label="Search"
          >
            <FiSearch className="w-5 h-5" />
          </button>

          {/* Theme toggle */}
          <button
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            className="p-2 text-white hover:bg-white/10 rounded-lg transition-colors"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? (
              <FiSun className="w-5 h-5" />
            ) : (
              <FiMoon className="w-5 h-5" />
            )}
          </button>

          {/* Help */}
          <button
            className="p-2 text-white hover:bg-white/10 rounded-lg transition-colors hidden sm:block"
            aria-label="Help"
          >
            <FiHelpCircle className="w-5 h-5" />
          </button>

          {/* Notifications */}
          <button
            className="p-2 text-white hover:bg-white/10 rounded-lg transition-colors relative"
            aria-label="Notifications"
          >
            <FiBell className="w-5 h-5" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* User menu */}
          <div className="relative">
            <button
              onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
              className="p-2 text-white hover:bg-white/10 rounded-lg transition-colors flex items-center gap-2"
              aria-label="User menu"
            >
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                <FiUser className="w-5 h-5" />
              </div>
              <span className="hidden lg:inline text-sm font-medium">Admin</span>
            </button>

            {/* Dropdown menu */}
            {isUserMenuOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 z-10 border border-gray-200 dark:border-gray-700">
                <Link
                  href="/dashboard/profile"
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                  onClick={() => setIsUserMenuOpen(false)}
                >
                  Your Profile
                </Link>
                <Link
                  href="/dashboard/settings"
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                  onClick={() => setIsUserMenuOpen(false)}
                >
                  Settings
                </Link>
                <div className="border-t border-gray-200 dark:border-gray-700"></div>
                <button
                  className="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                  onClick={() => setIsUserMenuOpen(false)}
                >
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile search bar */}
      {isSearchOpen && (
        <div className="md:hidden px-4 pb-4">
          <div className="relative w-full">
            <input
              type="text"
              placeholder="Search articles..."
              className="w-full px-4 py-2 pl-10 bg-white/10 border border-white/20 text-white placeholder-white/70 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/50"
            />
            <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-white/70" />
          </div>
        </div>
      )}
    </header>
  );
}