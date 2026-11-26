import type { MetadataRoute } from 'next';
import { getSitemap } from '@/lib/cms';
import { pageUrl } from '@/lib/seo';

/**
 * Approved pages only, from the CMS. Each English page is listed; its Arabic
 * version is listed (and paired in hreflang) only once the translation has
 * been reviewed, matching the pages' own robots and hreflang tags.
 */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const entries = await getSitemap();
  return entries.flatMap(({ path, updatedAt, ar }) => {
    const lastModified = updatedAt ? new Date(updatedAt) : undefined;
    const languages = { en: pageUrl('en', path), ...(ar ? { ar: pageUrl('ar', path) } : {}) };
    const english = { url: languages.en, lastModified, alternates: { languages } };
    return ar ? [english, { url: pageUrl('ar', path), lastModified, alternates: { languages } }] : [english];
  });
}
