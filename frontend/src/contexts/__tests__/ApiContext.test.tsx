import React, { useEffect, useState } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { ApiProvider, useArticles, Article } from '../ApiContext';
import { mockArticles } from '../../data/mockData';

// Mock the API services
jest.mock('../../services/mockApi', () => ({
  mockApi: {
    getArticles: jest.fn().mockResolvedValue({ data: mockArticles }),
    getArticle: jest.fn().mockImplementation((id) => {
      const article = mockArticles.find(a => a.id === id);
      if (!article) {
        return Promise.reject(new Error('Article not found'));
      }
      return Promise.resolve({ data: article });
    }),
    getCategories: jest.fn().mockResolvedValue({ data: [] }),
    getSources: jest.fn().mockResolvedValue({ data: [] }),
    searchArticles: jest.fn().mockResolvedValue({ data: [] })
  }
}));

jest.mock('../../services/api', () => ({
  realApi: {
    getArticles: jest.fn().mockResolvedValue({ data: [] }),
    getArticle: jest.fn().mockResolvedValue({ data: {} }),
    getCategories: jest.fn().mockResolvedValue({ data: [] }),
    getSources: jest.fn().mockResolvedValue({ data: [] }),
    searchArticles: jest.fn().mockResolvedValue({ data: [] })
  }
}));

// Test component that uses the API context
const TestComponent = () => {
  const fetchArticles = useArticles();
  const [articles, setArticles] = useState<Article[]>([]);
  
  useEffect(() => {
    const loadArticles = async () => {
      try {
        const response = await fetchArticles();
        setArticles(response.data);
      } catch (error) {
        console.error('Error loading articles:', error);
      }
    };
    
    loadArticles();
  }, [fetchArticles]);
  
  return (
    <div>
      {articles.map(article => (
        <div key={article.id} data-testid="article-item">
          {article.title}
        </div>
      ))}
    </div>
  );
};

describe('ApiContext', () => {
  test('provides articles through context with mock API', async () => {
    render(
      <ApiProvider isMock={true}>
        <TestComponent />
      </ApiProvider>
    );
    
    await waitFor(() => {
      const articleItems = screen.getAllByTestId('article-item');
      expect(articleItems.length).toBe(mockArticles.length);
    });
  });

  test('uses the correct API based on isMock prop', async () => {
    const { rerender } = render(
      <ApiProvider isMock={true}>
        <TestComponent />
      </ApiProvider>
    );
    
    await waitFor(() => {
      expect(screen.getAllByTestId('article-item').length).toBe(mockArticles.length);
    });

    // Re-render with real API (which returns empty data in our mock)
    rerender(
      <ApiProvider isMock={false}>
        <TestComponent />
      </ApiProvider>
    );

    // Wait for re-render with real API (which should show no articles)
    await waitFor(() => {
      expect(screen.queryAllByTestId('article-item').length).toBe(0);
    });
  });
});
