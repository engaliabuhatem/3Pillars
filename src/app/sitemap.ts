import type { MetadataRoute } from 'next';
import { getSitemap } from '@/lib/cms';
import { siteUrl } from '@/lib/seo';

/** Static routes plus every approved detail page from the CMS, in both languages. */
const STATIC = ['', '/services', '/sectors', '/projects', '/insights', '/about', '/approach', '/careers', '/contact', '/request-a-proposal', '/capability-statement'];

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base = siteUrl();
  const entries = await getSitemap();
  const seen = new Set(STATIC);
  const paths = [
    ...STATIC.map((path) => ({ path, updatedAt: undefined as string | undefined })),
    ...entries.filter((entry) => !seen.has(entry.path)).map((entry) => ({ path: entry.path, updatedAt: entry.updatedAt })),
  ];

  return paths.map(({ path, updatedAt }) => ({
    url: `${base}/en${path}`,
    lastModified: updatedAt ? new Date(updatedAt) : undefined,
    alternates: { languages: { en: `${base}/en${path}`, ar: `${base}/ar${path}` } },
  }));
}
