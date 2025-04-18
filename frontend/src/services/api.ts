import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL
});

export const realApi = {
  getArticles: async (params?: { category?: string; limit?: number }) => {
    const response = await api.get('/articles', { params });
    return response.data;
  },

  getArticle: async (id: number) => {
    const response = await api.get(`/articles/${id}`);
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get('/categories');
    return response.data;
  },

  getSources: async () => {
    const response = await api.get('/sources');
    return response.data;
  },

  searchArticles: async (query: string) => {
    const response = await api.get('/articles/search', { params: { q: query } });
    return response.data;
  }
}; 