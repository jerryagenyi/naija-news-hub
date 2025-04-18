import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { TestApi } from '../TestApi';
import { ApiProvider } from '../../contexts/ApiContext';
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
      expect(screen.getByText(mockArticles[0].title)).toBeInTheDocument();
    });
    
    // Check if all articles are rendered
    mockArticles.forEach(article => {
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
      // Check if tags from the first article are rendered
      mockArticles[0].tags.forEach(tag => {
        expect(screen.getByText(tag)).toBeInTheDocument();
      });
    });
  });
});
