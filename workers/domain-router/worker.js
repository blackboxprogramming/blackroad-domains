/**
 * BlackRoad Domain Router - Cloudflare Worker
 *
 * Routes incoming requests to the correct Cloudflare Pages project
 * based on the hostname. Handles health checks, security headers,
 * and domain-to-project mapping for all 19 BlackRoad domains.
 *
 * Copyright 2024-2026 BlackRoad OS, Inc. All Rights Reserved.
 * Proprietary and Confidential.
 */

const DOMAIN_MAP = {
  // BlackRoad Core
  'blackroad.io': 'blackroad-io',
  'www.blackroad.io': 'blackroad-io',
  'blackroad.me': 'blackroad-me',
  'www.blackroad.me': 'blackroad-me',
  'blackroad.network': 'blackroad-network',
  'www.blackroad.network': 'blackroad-network',
  'blackroad.systems': 'blackroad-systems',
  'www.blackroad.systems': 'blackroad-systems',
  'blackroad.company': 'blackroad-io',
  'www.blackroad.company': 'blackroad-io',

  // AI & Quantum
  'blackroadai.com': 'blackroadai-com',
  'www.blackroadai.com': 'blackroadai-com',
  'blackroadqi.com': 'blackroadqi-com',
  'www.blackroadqi.com': 'blackroadqi-com',
  'blackroadquantum.com': 'blackroadquantum-com',
  'www.blackroadquantum.com': 'blackroadquantum-com',
  'blackroadquantum.info': 'blackroadquantum-info',
  'www.blackroadquantum.info': 'blackroadquantum-info',
  'blackroadquantum.net': 'blackroadquantum-net',
  'www.blackroadquantum.net': 'blackroadquantum-net',
  'blackroadquantum.shop': 'blackroadquantum-shop',
  'www.blackroadquantum.shop': 'blackroadquantum-shop',
  'blackroadquantum.store': 'blackroadquantum-store',
  'www.blackroadquantum.store': 'blackroadquantum-store',

  // Lucidia
  'lucidia.earth': 'lucidia-earth',
  'www.lucidia.earth': 'lucidia-earth',
  'lucidia.studio': 'lucidia-studio',
  'www.lucidia.studio': 'lucidia-studio',
  'lucidiaqi.com': 'lucidiaqi-com',
  'www.lucidiaqi.com': 'lucidiaqi-com',

  // Other
  'blackroadinc.us': 'blackroadinc-us',
  'www.blackroadinc.us': 'blackroadinc-us',
  'blackboxprogramming.io': 'blackroad-io',
  'www.blackboxprogramming.io': 'blackroad-io',

  // Blockchain
  'roadchain.io': 'blackroad-io',
  'www.roadchain.io': 'blackroad-io',
  'roadcoin.io': 'blackroad-io',
  'www.roadcoin.io': 'blackroad-io',
};

const SECURITY_HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'SAMEORIGIN',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
};

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const hostname = url.hostname;

    // Health check endpoint
    if (url.pathname === '/api/health') {
      return new Response(
        JSON.stringify({
          status: 'healthy',
          service: 'blackroad-domain-router',
          hostname: hostname,
          timestamp: new Date().toISOString(),
          version: '1.0.0',
        }),
        {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            ...SECURITY_HEADERS,
          },
        }
      );
    }

    // Look up the Cloudflare Pages project for this domain
    const project = DOMAIN_MAP[hostname];

    if (!project) {
      return new Response(
        JSON.stringify({
          error: 'Domain not configured',
          hostname: hostname,
          message: 'Contact blackroad.systems@gmail.com for support.',
        }),
        {
          status: 404,
          headers: {
            'Content-Type': 'application/json',
            ...SECURITY_HEADERS,
          },
        }
      );
    }

    // Proxy to the Cloudflare Pages project
    const pagesUrl = `https://${project}.pages.dev${url.pathname}${url.search}`;
    const response = await fetch(pagesUrl, {
      method: request.method,
      headers: request.headers,
      body: request.method !== 'GET' && request.method !== 'HEAD' ? request.body : undefined,
    });

    // Clone response and add security headers
    const newResponse = new Response(response.body, response);
    for (const [key, value] of Object.entries(SECURITY_HEADERS)) {
      newResponse.headers.set(key, value);
    }

    return newResponse;
  },
};
