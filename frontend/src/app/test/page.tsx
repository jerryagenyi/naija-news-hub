'use client';

import { Suspense } from 'react';
import { TestApi } from '../../components/TestApi';
import { ErrorBoundary } from '../../components/ErrorBoundary';

const ErrorFallback = (error: Error) => {
  return (
    <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
      <h2 className="text-lg font-semibold text-red-600 dark:text-red-400 mb-2">
        Something went wrong:
      </h2>
      <pre className="text-sm text-red-500 dark:text-red-300 whitespace-pre-wrap">
        {error.message}
      </pre>
    </div>
  );
};

function LoadingFallback() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>
  );
}

export default function TestPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
        API Test Page
      </h1>
      
      <ErrorBoundary fallback={ErrorFallback}>
        <Suspense fallback={<LoadingFallback />}>
          <TestApi />
        </Suspense>
      </ErrorBoundary>
    </div>
  );
} 