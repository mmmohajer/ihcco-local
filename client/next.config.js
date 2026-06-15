/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  webpack: (config, { dev, isServer }) => {
    if (dev && isServer) {
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300,
      };
    }
    return config;
  },

  env: {},

  publicRuntimeConfig: {},

  images: {
    domains: ["localhost"],
  },
};

module.exports = nextConfig;
