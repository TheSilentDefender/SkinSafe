/** @type {import('next').NextConfig} */
const nextConfig = {
  swcMinify: true,
  reactStrictMode: true,
  images: {
    domains: [
      'media.ulta.com'
    ]
  },
}

module.exports = nextConfig;
