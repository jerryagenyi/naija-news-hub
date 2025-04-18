'use client';

import React, { useEffect, useState } from 'react';
import { useArticles, Article } from '@/contexts/ApiContext';

export default function LatestArticles() {
  const [page, setPage] = useState(1);
  const [totalArticles, setTotalArticles] = useState(0);
  const articlesPerPage = 5;

  const fetchArticles = useArticles({
    limit: articlesPerPage,
    offset: (page - 1) * articlesPerPage
  });

  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadArticles = async () => {
      try {
        setLoading(true);
        const response = await fetchArticles();
        setArticles(response.data);
        setTotalArticles(response.total || 0);
        setError(null);
      } catch (err) {
        setError('Failed to fetch articles');
        console.error('Error fetching articles:', err);
      } finally {
        setLoading(false);
      }
    };

    loadArticles();
  }, [fetchArticles, page]);

  return (
    <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Latest Articles
      </h2>

      {loading && (
        <div className="flex items-center justify-center p-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-md mb-4">
          {error}
        </div>
      )}

      {!loading && !error && articles.length === 0 && (
        <div className="text-center py-4 text-gray-500 dark:text-gray-400">
          No articles found
        </div>
      )}

      {!loading && !error && articles.length > 0 && (
        <>
          <div className="space-y-4">
            {articles.map((article) => (
              <div
                key={article.id}
                className="border dark:border-gray-700 p-4 rounded-lg hover:shadow-lg transition-shadow duration-200"
              >
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {article.title}
                </h3>
                <div className="flex items-center space-x-4 text-sm">
                  <span className="text-blue-600 dark:text-blue-400">
                    {article.source}
                  </span>
                  <span className="text-gray-500 dark:text-gray-400">
                    {article.category}
                  </span>
                </div>
                <div className="mt-2 flex flex-wrap gap-2">
                  {article.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-xs rounded-full"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Pagination Controls */}
          <div className="flex justify-between items-center mt-6">
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Showing {(page - 1) * articlesPerPage + 1} to {Math.min(page * articlesPerPage, totalArticles)} of {totalArticles} articles
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className={`px-3 py-1 rounded ${page === 1 ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-600 cursor-not-allowed' : 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/30'}`}
              >
                Previous
              </button>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={page * articlesPerPage >= totalArticles}
                className={`px-3 py-1 rounded ${page * articlesPerPage >= totalArticles ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-600 cursor-not-allowed' : 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/30'}`}
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
