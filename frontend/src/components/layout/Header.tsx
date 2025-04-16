'use client';

import { useState, useEffect, memo } from 'react';
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

const SearchBar = memo(({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose]);

  return (
    <div
      className={`fixed inset-0 z-50 flex items-start justify-center pt-16 px-4 sm:px-6 ${
        isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
      } transition-opacity duration-200`}
    >
      <div className="w-full max-w-2xl">
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search articles, websites, or jobs..."
            className="w-full px-4 py-3 text-gray-900 bg-white dark:bg-gray-800 dark:text-white rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
          />
          <button
            onClick={onClose}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            aria-label="Close search"
          >
            <FiX className="w-5 h-5" />
          </button>
        </div>
      </div>
      <div
        className="fixed inset-0 bg-black/50 -z-10"
        onClick={onClose}
        aria-hidden="true"
      />
    </div>
  );
});

const UserMenu = memo(({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest('[data-user-menu]')) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('click', handleClickOutside);
      return () => document.removeEventListener('click', handleClickOutside);
    }
  }, [isOpen, onClose]);

  return (
    <div
      className={`absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 ${
        isOpen ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2 pointer-events-none'
      } transition-all duration-200`}
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="user-menu-button"
      data-user-menu
    >
      <Link
        href="/profile"
        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
        role="menuitem"
      >
        Your Profile
      </Link>
      <Link
        href="/settings"
        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
        role="menuitem"
      >
        Settings
      </Link>
      <button
        onClick={() => {/* Add sign out logic */}}
        className="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
        role="menuitem"
      >
        Sign out
      </button>
    </div>
  );
});

const Header = memo(({ onToggleSidebar }: HeaderProps) => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const { theme, setTheme } = useTheme();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-40 w-full transition-all duration-200 ${
        isScrolled
          ? 'header-gradient backdrop-blur-sm shadow-sm'
          : 'header-gradient'
      }`}
    >
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8" aria-label="Main navigation">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={onToggleSidebar}
              className="p-2 text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
              aria-label="Toggle sidebar"
            >
              <FiMenu className="w-5 h-5" />
            </button>
            <Link href="/" className="flex items-center space-x-2">
              <span className="sr-only">Naija News Hub</span>
              <FiGlobe className="h-8 w-8 text-blue-600" />
              <span className="hidden sm:block font-bold text-xl text-gray-900 dark:text-white">
                Naija News Hub
              </span>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <button
              onClick={() => setIsSearchOpen(true)}
              className="p-2 text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300"
              aria-label="Search"
            >
              <FiSearch className="w-5 h-5" />
            </button>

            <button
              onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
              className="flex items-center space-x-2 p-2 text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300"
              aria-expanded={isUserMenuOpen}
              aria-haspopup="true"
              id="user-menu-button"
            >
              <img
                src="/placeholder-avatar.jpg"
                alt=""
                className="h-8 w-8 rounded-full"
              />
              <span className="hidden sm:block">John Doe</span>
            </button>
          </div>
        </div>
      </nav>

      <SearchBar isOpen={isSearchOpen} onClose={() => setIsSearchOpen(false)} />
      <UserMenu isOpen={isUserMenuOpen} onClose={() => setIsUserMenuOpen(false)} />
    </header>
  );
});

export default Header;