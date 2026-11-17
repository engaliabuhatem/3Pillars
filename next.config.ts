import type { NextConfig } from 'next';

// Uploaded media is served by the CMS host. The allow-list is derived from the
// same env var the data client uses, so the two can never disagree.
const cms = process.env.CMS_API_URL ? new URL(process.env.CMS_API_URL) : null;
const publicCms = process.env.NEXT_PUBLIC_CMS_API_URL ? new URL(process.env.NEXT_PUBLIC_CMS_API_URL) : cms;
const isDev = process.env.NODE_ENV === 'development';

/*
 * Content Security Policy. Scripts: self + inline (Next's bootstrap and the
 * pre-paint intro script) + the optional Turnstile/analytics hosts. Images and
 * media: self + the CMS host. Forms post to the CMS API.
 */
const cmsOrigin = publicCms ? publicCms.origin : '';
const csp = [
  "default-src 'self'",
  `script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ''} https://challenges.cloudflare.com https://plausible.io https://www.googletagmanager.com`,
  "style-src 'self' 'unsafe-inline'",
  `img-src 'self' data: blob: ${cmsOrigin} https://www.google-analytics.com`,
  `media-src 'self' ${cmsOrigin}`,
  "font-src 'self'",
  `connect-src 'self' ${cmsOrigin} https://plausible.io https://*.google-analytics.com https://challenges.cloudflare.com${isDev ? ' ws:' : ''}`,
  'frame-src https://challenges.cloudflare.com',
  "frame-ancestors 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "object-src 'none'",
  ...(isDev ? [] : ['upgrade-insecure-requests']),
].join('; ');

const securityHeaders = [
  { key: 'Content-Security-Policy', value: csp },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
  ...(isDev ? [] : [{ key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains; preload' }]),
];

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  experimental: { globalNotFound: true },
  images: {
    formats: ['image/avif', 'image/webp'],
    qualities: [60, 75, 90],
    remotePatterns: cms
      ? [
          {
            protocol: cms.protocol === 'https:' ? 'https' : 'http',
            hostname: cms.hostname,
            port: cms.port,
            pathname: '/assets/**',
          },
        ]
      : [],
    // The CMS runs on 127.0.0.1 in development (and in a local production
    // build when IMAGES_ALLOW_LOCAL_IP=true). Never set that on a server.
    ...(isDev || process.env.IMAGES_ALLOW_LOCAL_IP === 'true' ? { dangerouslyAllowLocalIP: true } : {}),
  },
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  },
};

export default nextConfig;
