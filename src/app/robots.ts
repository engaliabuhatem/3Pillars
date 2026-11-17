import type { MetadataRoute } from 'next';
import { getSettings } from '@/lib/cms';
import { siteUrl } from '@/lib/seo';

/** While the site is behind coming-soon (or on staging), nothing is indexed. */
export default async function robots(): Promise<MetadataRoute.Robots> {
  const settings = await getSettings('en');
  const closed = settings.comingSoon || settings.showPendingContent || process.env.ALLOW_INDEXING === 'false';
  return {
    rules: closed ? { userAgent: '*', disallow: '/' } : { userAgent: '*', allow: '/', disallow: ['/api/', '/*/coming-soon'] },
    sitemap: `${siteUrl()}/sitemap.xml`,
  };
}
