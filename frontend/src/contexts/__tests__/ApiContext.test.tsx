import React, { useEffect, useState } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { ApiProvider, useArticles, Article } from '../ApiContext';

// Create mock articles for testing
const testMockArticles = [
  {
    id: 1,
    title: "Test Article 1",
    content: "Test content 1",
    source: "Test Source",
    category: "Test Category",
    publishedAt: "2024-04-17T10:00:00Z",
    author: "Test Author",
    url: "https://example.com/test1",
    imageUrl: "https://example.com/test1.jpg",
    tags: ["test", "mock"]
  },
  {
    id: 2,
    title: "Test Article 2",
    content: "Test content 2",
    source: "Test Source",
    category: "Test Category",
    publishedAt: "2024-04-16T15:30:00Z",
    author: "Test Author",
    url: "https://example.com/test2",
    imageUrl: "https://example.com/test2.jpg",
    tags: ["test", "mock"]
  }
];

// Mock the API services
jest.mock('../../services/mockApi', () => ({
  mockApi: {
    getArticles: jest.fn().mockResolvedValue({ data: testMockArticles }),
    getArticle: jest.fn().mockImplementation((id) => {
      const article = testMockArticles.find(a => a.id === id);
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
      expect(articleItems.length).toBe(testMockArticles.length);
    });
  });

  test('uses the correct API based on isMock prop', async () => {
    const { rerender } = render(
      <ApiProvider isMock={true}>
        <TestComponent />
      </ApiProvider>
    );

    await waitFor(() => {
      expect(screen.getAllByTestId('article-item').length).toBe(testMockArticles.length);
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
