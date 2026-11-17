import 'server-only';
import type { Locale } from '@/i18n/config';

/**
 * Cache tags, one per content family. Django's webhook sends the same names
 * (each model's `cache_tags`), and /api/revalidate expires them.
 */
export type CacheTag =
  | 'settings'
  | 'navigation'
  | 'home'
  | 'pillars'
  | 'services'
  | 'sectors'
  | 'projects'
  | 'insights'
  | 'pages'
  | 'team'
  | 'offices'
  | 'certifications'
  | 'downloads'
  | 'jobs'
  | 'redirects'
  | 'kpis'
  | 'clients'
  | 'testimonials'
  | 'approach';

/** Safety net if a webhook is ever missed: content is never older than this. */
export const FALLBACK_REVALIDATE_SECONDS = 300;

const TIMEOUT_MS = 4000;

export function apiBase(): string | null {
  return process.env.CMS_API_URL?.replace(/\/$/, '') ?? null;
}

export class CmsUnavailable extends Error {}

interface Options {
  tags: CacheTag[];
  locale?: Locale;
  params?: Record<string, string | undefined>;
}

/**
 * GET a CMS endpoint. Returns `null` for a 404 (the page does not exist or is
 * not approved) and throws `CmsUnavailable` for anything else, so callers can
 * tell "no such page" from "the CMS is down" and fall back only for the latter.
 */
export async function cmsGet<T>(path: string, { tags, locale = 'en', params = {} }: Options): Promise<T | null> {
  const base = apiBase();
  if (!base) throw new CmsUnavailable('CMS_API_URL is not set');

  const query = new URLSearchParams({ locale });
  for (const [key, value] of Object.entries(params)) if (value) query.set(key, value);
  const url = `${base}/${path.replace(/^\//, '')}?${query}`;

  let response: Response;
  try {
    response = await fetch(url, {
      next: { tags, revalidate: FALLBACK_REVALIDATE_SECONDS },
      signal: AbortSignal.timeout(TIMEOUT_MS),
      headers: { Accept: 'application/json' },
    });
  } catch (error) {
    throw new CmsUnavailable(`${url}: ${(error as Error).message}`);
  }
  if (response.status === 404) return null;
  if (!response.ok) throw new CmsUnavailable(`${url}: HTTP ${response.status}`);
  return (await response.json()) as T;
}

/** Like cmsGet, but a CMS outage yields `fallback` instead of an error page. */
export async function cmsGetOr<T>(path: string, options: Options, fallback: T): Promise<T> {
  try {
    return (await cmsGet<T>(path, options)) ?? fallback;
  } catch (error) {
    if (error instanceof CmsUnavailable) {
      console.error('[cms] serving fallback:', error.message);
      return fallback;
    }
    throw error;
  }
}
