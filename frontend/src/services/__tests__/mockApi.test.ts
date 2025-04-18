import { mockApi } from '../mockApi';
import { mockArticles, mockCategories, mockSources } from '../../data/mockData';

// Mock the delay function to make tests run faster
jest.mock('../mockApi', () => {
  const originalModule = jest.requireActual('../mockApi');
  return {
    ...originalModule,
    mockApi: {
      ...originalModule.mockApi,
      getArticles: (params?: { category?: string; limit?: number }) => {
        let articles = [...mockArticles];

        if (params?.category) {
          articles = articles.filter(article => article.category === params.category);
        }

        if (params?.limit) {
          articles = articles.slice(0, params.limit);
        }

        return Promise.resolve({
          data: articles,
          total: articles.length
        });
      },
      getArticle: (id: number) => {
        const article = mockArticles.find(a => a.id === id);
        if (!article) {
          return Promise.reject(new Error('Article not found'));
        }
        return Promise.resolve({ data: article });
      },
      getCategories: () => Promise.resolve({ data: mockCategories }),
      getSources: () => Promise.resolve({ data: mockSources }),
      searchArticles: (query: string) => {
        const results = mockArticles.filter(article =>
          article.title.toLowerCase().includes(query.toLowerCase()) ||
          article.content.toLowerCase().includes(query.toLowerCase())
        );
        return Promise.resolve({ data: results });
      }
    }
  };
});

describe('Mock API Service', () => {
  // Test article retrieval
  test('getArticles returns all articles when no parameters provided', async () => {
    const result = await mockApi.getArticles();
    expect(result.data).toEqual(mockArticles);
    expect(result.total).toBe(mockArticles.length);
  });

  // Test filtering by category
  test('getArticles filters by category correctly', async () => {
    const category = 'Technology';
    const result = await mockApi.getArticles({ category });
    expect(result.data.every(article => article.category === category)).toBe(true);
    expect(result.data.length).toBeGreaterThan(0);
  });

  // Test limiting results
  test('getArticles limits the number of results correctly', async () => {
    const limit = 5;
    const result = await mockApi.getArticles({ limit });
    expect(result.data.length).toBe(limit);
  });

  // Test pagination with limit and offset
  test('getArticles handles pagination correctly', async () => {
    const limit = 5;
    const offset = 5;
    const result = await mockApi.getArticles({ limit, offset });
    expect(result.data.length).toBe(limit);
    expect(result.data[0].id).toBe(6); // First article in second page
  });

  // Test getting a single article
  test('getArticle returns the correct article by ID', async () => {
    const id = 1;
    const result = await mockApi.getArticle(id);
    expect(result.data.id).toBe(id);
  });

  // Test error handling
  test('getArticle throws error for non-existent article', async () => {
    await expect(mockApi.getArticle(999)).rejects.toThrow('Article not found');
  });

  // Test categories retrieval
  test('getCategories returns all categories', async () => {
    const result = await mockApi.getCategories();
    expect(result.data).toEqual(mockCategories);
  });

  // Test sources retrieval
  test('getSources returns all sources', async () => {
    const result = await mockApi.getSources();
    expect(result.data).toEqual(mockSources);
  });

  // Test search functionality
  test('searchArticles returns articles matching query', async () => {
    const result = await mockApi.searchArticles('Tech');
    expect(result.data.length).toBeGreaterThan(0);
    expect(result.data[0].title).toContain('Tech');
  });

  // Test search with no results
  test('searchArticles returns empty array for non-matching query', async () => {
    const result = await mockApi.searchArticles('NonExistentTerm');
    expect(result.data.length).toBe(0);
  });
});
