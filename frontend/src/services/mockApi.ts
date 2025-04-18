import { mockArticles, mockCategories, mockSources } from '../data/mockData';

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const mockApi = {
  getArticles: async (params?: { category?: string; limit?: number; offset?: number }) => {
    await delay(500); // Simulate network delay
    let articles = [...mockArticles];
    let totalCount = articles.length;

    if (params?.category) {
      articles = articles.filter(article => article.category === params.category);
      totalCount = articles.length;
    }

    // Apply offset first, then limit
    if (params?.offset !== undefined) {
      articles = articles.slice(params.offset);
    }

    if (params?.limit !== undefined) {
      articles = articles.slice(0, params.limit);
    }

    return {
      data: articles,
      total: totalCount
    };
  },

  getArticle: async (id: number) => {
    await delay(300);
    const article = mockArticles.find(a => a.id === id);
    if (!article) {
      throw new Error('Article not found');
    }
    return { data: article };
  },

  getCategories: async () => {
    await delay(200);
    return { data: mockCategories };
  },

  getSources: async () => {
    await delay(200);
    return { data: mockSources };
  },

  searchArticles: async (query: string) => {
    await delay(600);
    const results = mockArticles.filter(article =>
      article.title.toLowerCase().includes(query.toLowerCase()) ||
      article.content.toLowerCase().includes(query.toLowerCase())
    );
    return { data: results };
  },
  getDashboardStats: async () => {
    await delay(400);
    return {
      data: {
        totalArticles: 1234,
        totalWebsites: 15,
        activeJobs: 3,
        errorCount: 2,
      }
    };
  }
};
