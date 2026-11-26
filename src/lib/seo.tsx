import type { Metadata } from 'next';
import type { Locale } from '@/i18n/config';
import { getSettings } from './cms';
import type { Indexable, Media, Office, Seo, SiteSettings } from './cms/types';
import { withSlash } from './utils';

export const siteUrl = () => (process.env.SITE_URL ?? 'http://localhost:3000').replace(/\/$/, '');

/** The one canonical form of a page address: absolute, locale-prefixed, trailing slash. */
export function pageUrl(locale: Locale, path: string): string {
  return `${siteUrl()}${withSlash(`/${locale}${path === '/' ? '' : path}`)}`;
}

const NOT_INDEXABLE: Indexable = { en: false, ar: false };

interface MetaInput {
  locale: Locale;
  /** Locale-free path, e.g. "/services/pmo-project-controls/" ("" for home). */
  path: string;
  title?: string;
  description?: string;
  seo?: Seo;
  image?: Media | null;
  type?: 'website' | 'article';
}

/**
 * Page metadata from CMS fields: SEO overrides first, then the page's own
 * title/summary, then the site defaults.
 *
 * Indexing follows the content's approval. A page awaiting approval is
 * noindex. An Arabic page is indexable, and listed in hreflang, only once its
 * translation is reviewed; machine drafts and English fallbacks never compete
 * in search. A page without CMS SEO data is noindex.
 */
export async function buildMetadata({ locale, path, title, description, seo, image, type = 'website' }: MetaInput): Promise<Metadata> {
  const settings = await getSettings(locale);
  const indexable = seo?.indexable ?? NOT_INDEXABLE;
  const finalDescription = seo?.description || description || settings.seoDescription || settings.tagline;
  const ogImage = seo?.image ?? image ?? settings.defaultOgImage;
  const url = pageUrl(locale, path);
  const languages: Record<string, string> = {};
  if (indexable.en) languages.en = languages['x-default'] = pageUrl('en', path);
  if (indexable.ar) languages.ar = pageUrl('ar', path);
  const socialTitle = seo?.title || title || settings.seoTitle || settings.companyName;

  return {
    metadataBase: new URL(siteUrl()),
    // A CMS SEO title is complete ("… | 3 Pillars"); a plain page title gets the site name appended.
    ...(seo?.title ? { title: { absolute: seo.title } } : title ? { title } : {}),
    description: finalDescription || undefined,
    robots: indexable[locale] ? { index: true, follow: true } : { index: false, follow: true },
    alternates: { canonical: url, languages },
    openGraph: {
      type,
      url,
      siteName: settings.companyName,
      locale: locale === 'ar' ? 'ar_YE' : 'en_GB',
      title: socialTitle,
      description: finalDescription || undefined,
      // Without a CMS image the route's generated opengraph-image applies.
      ...(ogImage ? { images: [{ url: ogImage.src, alt: ogImage.alt, width: ogImage.width ?? undefined, height: ogImage.height ?? undefined }] } : {}),
    },
    twitter: { card: 'summary_large_image' },
  };
}

export function organizationJsonLd(settings: SiteSettings, offices: Office[], locale: Locale) {
  const base = siteUrl();
  return {
    '@context': 'https://schema.org',
    '@type': ['Organization', 'ProfessionalService'],
    '@id': `${base}/#organization`,
    name: settings.companyName,
    url: pageUrl(locale, ''),
    logo: `${base}/brand/logo-full.svg`,
    ...(settings.tagline ? { description: settings.tagline } : {}),
    ...(settings.email ? { email: settings.email } : {}),
    ...(settings.phone ? { telephone: settings.phone } : {}),
    sameAs: settings.socials.map((s) => s.href),
    address: offices.map((office) => ({
      '@type': 'PostalAddress',
      addressLocality: office.city,
      addressCountry: office.country,
      ...(office.address ? { streetAddress: office.address } : {}),
    })),
  };
}

export function websiteJsonLd(settings: SiteSettings, locale: Locale) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${siteUrl()}/#website`,
    name: settings.companyName,
    url: pageUrl(locale, ''),
    inLanguage: locale,
    publisher: { '@id': `${siteUrl()}/#organization` },
  };
}

export function breadcrumbJsonLd(locale: Locale, trail: Array<{ name: string; path: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: trail.map((crumb, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: crumb.name,
      item: pageUrl(locale, crumb.path),
    })),
  };
}

export function articleJsonLd(
  article: { title: string; excerpt: string; publishedAt: string | null; updatedAt: string; author: string; image: Media | null },
  url: string,
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: article.title,
    description: article.excerpt,
    ...(article.publishedAt ? { datePublished: article.publishedAt } : {}),
    dateModified: article.updatedAt,
    mainEntityOfPage: url,
    ...(article.author ? { author: { '@type': 'Person', name: article.author } } : {}),
    ...(article.image ? { image: article.image.src } : {}),
    publisher: { '@id': `${siteUrl()}/#organization` },
  };
}

/**
 * JobPosting structured data, or null when a field Google requires is missing:
 * an incomplete posting is worse than none.
 */
export function jobPostingJsonLd(
  job: { title: string; description: string; postedAt: string; closesAt: string | null; location: string; employmentType: string },
  companyName: string,
) {
  if (!job.title || !job.description || !job.postedAt || !job.location) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'JobPosting',
    title: job.title,
    description: job.description,
    datePosted: job.postedAt,
    ...(job.closesAt ? { validThrough: job.closesAt } : {}),
    employmentType: job.employmentType.toUpperCase().replace(/[^A-Z]+/g, '_'),
    hiringOrganization: { '@type': 'Organization', name: companyName, sameAs: siteUrl() },
    jobLocation: { '@type': 'Place', address: { '@type': 'PostalAddress', addressLocality: job.location } },
  };
}

export function JsonLd({ data }: { data: object | null }) {
  if (!data) return null;
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, '\\u003c') }} />;
}
