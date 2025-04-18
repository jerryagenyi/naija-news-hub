/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // Required for Firebase Studio static hosting
  images: {
    unoptimized: true, // Required for static export
  },
  // Enable static export
  distDir: 'out',
  poweredByHeader: false,
  reactStrictMode: true,
};

module.exports = nextConfig;
