/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Replicad's WASM bundle is loaded client-side only in Phase 1.
  // No webpack customization needed yet.
};

module.exports = nextConfig;
