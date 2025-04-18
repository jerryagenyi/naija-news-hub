'use client';

import React from 'react';
import { ApiProvider } from '@/contexts/ApiContext';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Use environment variable to determine whether to use mock API
  // This makes it easy to switch between mock and real API
  const useMockApi = process.env.NEXT_PUBLIC_USE_MOCK_API === 'true';
  
  return (
    <ApiProvider isMock={useMockApi}>
      {children}
    </ApiProvider>
  );
}
