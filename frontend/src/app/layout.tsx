'use client';

import { useState } from 'react';
import { ThemeProvider } from 'next-themes';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import Footer from '@/components/layout/Footer';
import '@/styles/globals.css';
import { ApiProvider } from '../contexts/ApiContext';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ApiProvider isMock={process.env.NEXT_PUBLIC_USE_MOCK_API === 'true'}>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col">
              <Header onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
              <div className="flex flex-1 pt-16">
                <Sidebar isOpen={isSidebarOpen} />
                <main
                  className={`flex-1 transition-all duration-300 ${
                    isSidebarOpen ? 'md:ml-64' : ''
                  }`}
                >
                  <div className="container mx-auto px-4 py-8">{children}</div>
                </main>
              </div>
              <div className={`transition-all duration-300 ${
                isSidebarOpen ? 'md:ml-64' : ''
              }`}>
                <Footer />
              </div>
            </div>
          </ThemeProvider>
        </ApiProvider>
      </body>
    </html>
  );
}
