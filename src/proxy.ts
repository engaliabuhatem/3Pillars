import { NextResponse, type NextRequest } from 'next/server';
import { DEFAULT_LOCALE, LOCALES, isLocale, type Locale } from '@/i18n/config';
import { withSlash } from '@/lib/utils';

/*
 * Runs before every page request, in this order:
 *   1. ?preview=<token> turns the private preview on (or off) for this browser.
 *   2. The other form of the site address (www / no www) → the preferred one.
 *   3. No locale in the path → redirect to the visitor's language.
 *   4. A CMS Redirect matches the path → permanent or temporary redirect to its target.
 *   5. The coming-soon switch is on and this is not a preview → coming-soon page.
 *
 * Trailing slashes are already settled before this runs (next.config
 * `trailingSlash`), so every path here ends in one.
 *
 * The switch and the redirect table are read from the CMS and cached in this
 * process for a few seconds, so an editor's change lands almost at once
 * without a CMS round-trip on every request. A CMS outage keeps the last
 * known values rather than blocking the site.
 */

const PREVIEW_PARAM = 'preview';
const PREVIEW_COOKIE = '3p-preview';
const SWITCH_TTL_MS = 10_000;
const REDIRECTS_TTL_MS = 60_000;

interface Cached<T> {
  value: T;
  at: number;
}

interface Switches {
  comingSoon: boolean;
  preferWww: boolean;
}

let switchCache: Cached<Switches> | null = null;
let redirectCache: Cached<Map<string, { to: string; permanent: boolean }>> | null = null;

const api = () => process.env.CMS_API_URL?.replace(/\/$/, '');

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${api()}/${path}`, { cache: 'no-store', signal: AbortSignal.timeout(2000) });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return (await response.json()) as T;
}

async function switches(): Promise<Switches> {
  const fallback = { comingSoon: process.env.COMING_SOON === 'true', preferWww: false };
  if (!api()) return fallback;
  if (switchCache && Date.now() - switchCache.at < SWITCH_TTL_MS) return switchCache.value;
  try {
    const settings = await fetchJson<{ comingSoon?: boolean; preferWww?: boolean }>('site-settings/');
    switchCache = { value: { comingSoon: settings.comingSoon === true, preferWww: settings.preferWww === true }, at: Date.now() };
  } catch (error) {
    console.error('[proxy] site switches unavailable:', error);
    switchCache = { value: switchCache?.value ?? fallback, at: Date.now() };
  }
  return switchCache.value;
}

/**
 * One preferred host: the www and bare forms of the site's own domain
 * redirect to whichever Site settings prefers. Other hosts (localhost, IPs,
 * preview domains) are left alone.
 */
function preferredHost(request: NextRequest, preferWww: boolean): URL | null {
  const site = process.env.SITE_URL ? new URL(process.env.SITE_URL).hostname.replace(/^www\./, '') : null;
  const host = request.nextUrl.hostname;
  if (!site || host.replace(/^www\./, '') !== site) return null;
  const isWww = host.startsWith('www.');
  if (isWww === preferWww) return null;
  const target = request.nextUrl.clone();
  target.hostname = preferWww ? `www.${site}` : site;
  target.protocol = 'https:';
  target.port = '';
  return target;
}

async function redirects() {
  if (!api()) return new Map();
  if (redirectCache && Date.now() - redirectCache.at < REDIRECTS_TTL_MS) return redirectCache.value;
  try {
    const rows = await fetchJson<Array<{ oldPath: string; newPath: string; permanent: boolean }>>('redirects/');
    redirectCache = {
      value: new Map(rows.map((r) => [r.oldPath.replace(/\/$/, '') || '/', { to: r.newPath, permanent: r.permanent }])),
      at: Date.now(),
    };
  } catch (error) {
    console.error('[proxy] redirects unavailable:', error);
    redirectCache = { value: redirectCache?.value ?? new Map(), at: Date.now() };
  }
  return redirectCache.value;
}

function preferredLocale(request: NextRequest): Locale {
  const saved = request.cookies.get('locale')?.value;
  if (isLocale(saved)) return saved;
  const ranked = (request.headers.get('accept-language') ?? '')
    .split(',')
    .map((part) => {
      const [tag = '', q] = part.trim().split(';q=');
      return { lang: tag.slice(0, 2).toLowerCase(), q: q ? Number(q) : 1 };
    })
    .sort((a, b) => b.q - a.q);
  const match = ranked.find((entry) => isLocale(entry.lang));
  return match && isLocale(match.lang) ? match.lang : DEFAULT_LOCALE;
}

export async function proxy(request: NextRequest) {
  const url = request.nextUrl;
  const token = process.env.PREVIEW_TOKEN;

  const previewParam = url.searchParams.get(PREVIEW_PARAM);
  if (previewParam !== null) {
    const clean = url.clone();
    clean.searchParams.delete(PREVIEW_PARAM);
    const response = NextResponse.redirect(clean);
    if (token && previewParam === token) {
      response.cookies.set(PREVIEW_COOKIE, token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        path: '/',
        maxAge: 60 * 60 * 24 * 30,
      });
    } else {
      response.cookies.delete(PREVIEW_COOKIE);
    }
    return response;
  }

  const { comingSoon, preferWww } = await switches();
  const host = preferredHost(request, preferWww);
  if (host) return NextResponse.redirect(host, 308);

  const [, first = '', ...rest] = url.pathname.split('/');
  if (!LOCALES.some((locale) => locale === first)) {
    const target = url.clone();
    target.pathname = `/${preferredLocale(request)}${url.pathname}`;
    return NextResponse.redirect(target);
  }

  const locale = first as Locale;
  const path = `/${rest.join('/')}`.replace(/\/$/, '') || '/';

  const redirect = (await redirects()).get(path);
  if (redirect) {
    const target = redirect.to.startsWith('http') ? new URL(redirect.to) : new URL(withSlash(`/${locale}${redirect.to}`), request.url);
    return NextResponse.redirect(target, redirect.permanent ? 308 : 307);
  }

  if (path === '/coming-soon') {
    return comingSoon ? NextResponse.next() : NextResponse.redirect(new URL(`/${locale}/`, request.url));
  }
  const previewing = Boolean(token) && request.cookies.get(PREVIEW_COOKIE)?.value === token;
  if (comingSoon && !previewing) {
    return NextResponse.redirect(new URL(`/${locale}/coming-soon/`, request.url), 307);
  }
  return NextResponse.next();
}

export const config = {
  // Skip Next internals, API routes, metadata routes and any file with an extension.
  matcher: ['/((?!_next/|api/|sitemap.xml|robots.txt|.*\\.\\w+$).*)'],
};
