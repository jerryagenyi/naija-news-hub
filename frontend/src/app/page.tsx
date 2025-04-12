'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.push('/dashboard');
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Redirecting to dashboard...
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Please wait while we redirect you to the dashboard.
        </p>
      </div>
    </div>
  );
}
