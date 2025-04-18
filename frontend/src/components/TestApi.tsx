'use client';

import { useEffect, useState } from 'react';
import { useApi, useArticles, Article } from '../contexts/ApiContext';

export const TestApi = () => {
  const { isMock } = useApi();
  const fetchArticles = useArticles();
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadArticles = async () => {
      try {
        setLoading(true);
        const response = await fetchArticles();
        setArticles(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch articles');
        console.error('Error fetching articles:', err);
      } finally {
        setLoading(false);
      }
    };

    loadArticles();
  }, [fetchArticles]);

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">
        API Test Component ({isMock ? 'Mock' : 'Real'} API)
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
      
      {!loading && !error && (
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
      )}
    </div>
  );
}; 