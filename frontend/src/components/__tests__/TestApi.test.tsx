import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { TestApi } from '../TestApi';
import { ApiProvider } from '../../contexts/ApiContext';

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

describe('TestApi Component', () => {
  test('renders loading state initially', () => {
    render(
      <ApiProvider isMock={true}>
        <TestApi />
      </ApiProvider>
    );

    expect(screen.getByText(/API Test Component/)).toBeInTheDocument();
    expect(screen.getByText(/Mock/)).toBeInTheDocument();
  });

  test('renders articles after loading', async () => {
    render(
      <ApiProvider isMock={true}>
        <TestApi />
      </ApiProvider>
    );

    // Wait for articles to load
    await waitFor(() => {
      // Check if the first article title is rendered
      expect(screen.getByText(testMockArticles[0].title)).toBeInTheDocument();
    });

    // Check if all articles are rendered
    testMockArticles.forEach(article => {
      expect(screen.getByText(article.title)).toBeInTheDocument();
    });
  });

  test('renders article tags', async () => {
    render(
      <ApiProvider isMock={true}>
        <TestApi />
      </ApiProvider>
    );

    // Wait for articles to load
    await waitFor(() => {
      // Check if at least one tag from the first article is rendered
      const firstTag = testMockArticles[0].tags[0];
      expect(screen.getAllByText(firstTag).length).toBeGreaterThan(0);
    });
  });
});
