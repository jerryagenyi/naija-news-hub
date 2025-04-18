'use client';

import { createContext, useContext, ReactNode, useCallback } from 'react';
import { mockApi } from '../services/mockApi';
import { realApi } from '../services/api';

// Define types for our API responses
export interface Article {
  id: number;
  title: string;
  content: string;
  source: string;
  category: string;
  publishedAt: string;
  author: string;
  url: string;
  imageUrl: string;
  tags: string[];
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface Source {
  id: number;
  name: string;
  url: string;
}

export interface ApiResponse<T> {
  data: T;
  total?: number;
}

export interface DashboardStats {
  totalArticles: number;
  totalWebsites: number;
  activeJobs: number;
  errorCount: number;
}

// Define the API interface
export interface Api {
  getArticles: (params?: { category?: string; limit?: number; offset?: number }) => Promise<ApiResponse<Article[]>>;
  getArticle: (id: number) => Promise<ApiResponse<Article>>;
  getCategories: () => Promise<ApiResponse<Category[]>>;
  getSources: () => Promise<ApiResponse<Source[]>>;
  searchArticles: (query: string) => Promise<ApiResponse<Article[]>>;
  getDashboardStats: () => Promise<ApiResponse<DashboardStats>>;
}

interface ApiContextType {
  isMock: boolean;
  api: Api;
  isLoading: boolean;
  error: Error | null;
}

const ApiContext = createContext<ApiContextType | undefined>(undefined);

interface ApiProviderProps {
  children: ReactNode;
  isMock?: boolean;
}

export const ApiProvider = ({ children, isMock = true }: ApiProviderProps) => {
  const api = isMock ? mockApi : realApi;

  return (
    <ApiContext.Provider
      value={{
        isMock,
        api,
        isLoading: false,
        error: null
      }}
    >
      {children}
    </ApiContext.Provider>
  );
};

export const useApi = () => {
  const context = useContext(ApiContext);
  if (context === undefined) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
};

// Custom hooks for specific API operations
export const useArticles = (params?: { category?: string; limit?: number; offset?: number }) => {
  const { api } = useApi();
  const fetchArticles = useCallback(async () => {
    try {
      return await api.getArticles(params);
    } catch (error) {
      console.error('Error fetching articles:', error);
      throw error;
    }
  }, [api, params]);

  return fetchArticles;
};

export const useArticle = (id: number) => {
  const { api } = useApi();
  const fetchArticle = useCallback(async () => {
    try {
      return await api.getArticle(id);
    } catch (error) {
      console.error(`Error fetching article ${id}:`, error);
      throw error;
    }
  }, [api, id]);

  return fetchArticle;
};

export const useCategories = () => {
  const { api } = useApi();
  const fetchCategories = useCallback(async () => {
    try {
      return await api.getCategories();
    } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
    }
  }, [api]);

  return fetchCategories;
};

export const useSources = () => {
  const { api } = useApi();
  const fetchSources = useCallback(async () => {
    try {
      return await api.getSources();
    } catch (error) {
      console.error('Error fetching sources:', error);
      throw error;
    }
  }, [api]);

  return fetchSources;
};
