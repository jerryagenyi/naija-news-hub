/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  images: {
    domains: ['api.dicebear.com'],
  },
};

module.exports = nextConfig;
