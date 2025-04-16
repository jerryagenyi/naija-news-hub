'use client';

import { useState, useEffect } from 'react';
import { FiPlus, FiEdit2, FiTrash2, FiPlay, FiPause, FiRefreshCw } from 'react-icons/fi';

interface Website {
  id: number;
  name: string;
  url: string;
  status: 'active' | 'inactive';
  lastScraped: Date | null;
  articleCount: number;
}

export default function WebsitesPage() {
  const [websites, setWebsites] = useState<Website[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newWebsite, setNewWebsite] = useState({ name: '', url: '' });

  // Fetch websites (mock data for now)
  useEffect(() => {
    // This would be replaced with an API call
    setWebsites([
      {
        id: 1,
        name: 'Punch News',
        url: 'https://punchng.com',
        status: 'active',
        lastScraped: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
        articleCount: 245,
      },
      {
        id: 2,
        name: 'Vanguard News',
        url: 'https://vanguardngr.com',
        status: 'active',
        lastScraped: new Date(Date.now() - 1000 * 60 * 15), // 15 minutes ago
        articleCount: 189,
      },
      {
        id: 3,
        name: 'ThisDay',
        url: 'https://thisdaylive.com',
        status: 'inactive',
        lastScraped: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 day ago
        articleCount: 156,
      },
    ]);
  }, []);

  const handleAddWebsite = () => {
    // This would be an API call in a real app
    const newId = Math.max(0, ...websites.map((w) => w.id)) + 1;
    const website: Website = {
      id: newId,
      name: newWebsite.name,
      url: newWebsite.url,
      status: 'inactive',
      lastScraped: null,
      articleCount: 0,
    };
    
    setWebsites([...websites, website]);
    setNewWebsite({ name: '', url: '' });
    setShowAddModal(false);
  };

  const toggleWebsiteStatus = (id: number) => {
    setWebsites(
      websites.map((website) =>
        website.id === id
          ? {
              ...website,
              status: website.status === 'active' ? 'inactive' : 'active',
            }
          : website
      )
    );
  };

  const startScraping = (id: number) => {
    // This would trigger an API call to start scraping
    alert(`Starting scraping for website ID: ${id}`);
  };

  const deleteWebsite = (id: number) => {
    if (confirm('Are you sure you want to delete this website?')) {
      setWebsites(websites.filter((website) => website.id !== id));
    }
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Websites
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Manage websites for scraping
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2"
        >
          <FiPlus className="w-4 h-4" />
          Add Website
        </button>
      </div>

      {/* Websites table */}
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                URL
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Last Scraped
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Articles
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
            {websites.map((website) => (
              <tr key={website.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900 dark:text-white">
                    {website.name}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    {website.url}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      website.status === 'active'
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
                    }`}
                  >
                    {website.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    {website.lastScraped
                      ? website.lastScraped.toLocaleString()
                      : 'Never'}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {website.articleCount}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() => toggleWebsiteStatus(website.id)}
                      className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                      title={website.status === 'active' ? 'Deactivate' : 'Activate'}
                    >
                      {website.status === 'active' ? (
                        <FiPause className="w-5 h-5" />
                      ) : (
                        <FiPlay className="w-5 h-5" />
                      )}
                    </button>
                    <button
                      onClick={() => startScraping(website.id)}
                      className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                      title="Start Scraping"
                    >
                      <FiRefreshCw className="w-5 h-5" />
                    </button>
                    <button
                      className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300"
                      title="Edit"
                    >
                      <FiEdit2 className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => deleteWebsite(website.id)}
                      className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                      title="Delete"
                    >
                      <FiTrash2 className="w-5 h-5" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Add Website Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-900 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">
              Add New Website
            </h2>
            <div className="space-y-4">
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                  Website Name
                </label>
                <input
                  type="text"
                  id="name"
                  value={newWebsite.name}
                  onChange={(e) =>
                    setNewWebsite({ ...newWebsite, name: e.target.value })
                  }
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
                />
              </div>
              <div>
                <label
                  htmlFor="url"
                  className="block text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                  Website URL
                </label>
                <input
                  type="url"
                  id="url"
                  value={newWebsite.url}
                  onChange={(e) =>
                    setNewWebsite({ ...newWebsite, url: e.target.value })
                  }
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
                />
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <button
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-white"
                >
                  Cancel
                </button>
                <button
                  onClick={handleAddWebsite}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                  disabled={!newWebsite.name || !newWebsite.url}
                >
                  Add Website
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
