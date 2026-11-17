import type { Metadata } from 'next';
import type { Locale } from '@/i18n/config';
import { getSettings } from './cms';
import type { Media, Office, Seo, SiteSettings } from './cms/types';

export const siteUrl = () => (process.env.SITE_URL ?? 'http://localhost:3000').replace(/\/$/, '');

interface MetaInput {
  locale: Locale;
  /** Locale-free path, e.g. "/services/pmc" ("" for home). */
  path: string;
  title?: string;
  description?: string;
  seo?: Seo;
  image?: Media | null;
  type?: 'website' | 'article';
}

/**
 * Page metadata from CMS fields: SEO overrides first, then the page's own
 * title/summary, then the site defaults. Every page gets a canonical URL and
 * hreflang links for both languages plus x-default (English).
 */
export async function buildMetadata({ locale, path, title, description, seo, image, type = 'website' }: MetaInput): Promise<Metadata> {
  const settings = await getSettings(locale);
  const base = siteUrl();
  const finalTitle = seo?.title || title;
  const finalDescription = seo?.description || description || settings.seoDescription || settings.tagline;
  const ogImage = seo?.image ?? image ?? settings.defaultOgImage;
  const url = `${base}/${locale}${path}`;

  return {
    metadataBase: new URL(base),
    ...(finalTitle ? { title: finalTitle } : {}),
    description: finalDescription || undefined,
    alternates: {
      canonical: url,
      languages: { en: `${base}/en${path}`, ar: `${base}/ar${path}`, 'x-default': `${base}/en${path}` },
    },
    openGraph: {
      type,
      url,
      siteName: settings.companyName,
      locale: locale === 'ar' ? 'ar_YE' : 'en_GB',
      title: finalTitle || settings.seoTitle || settings.companyName,
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
    url: `${base}/${locale}`,
    logo: `${base}/brand/logo-full.svg`,
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

export function breadcrumbJsonLd(locale: Locale, trail: Array<{ name: string; path: string }>) {
  const base = siteUrl();
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: trail.map((crumb, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: crumb.name,
      item: `${base}/${locale}${crumb.path}`,
    })),
  };
}

export function articleJsonLd(article: { title: string; excerpt: string; publishedAt: string; updatedAt: string; author: string; image: Media | null }, url: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: article.title,
    description: article.excerpt,
    datePublished: article.publishedAt,
    dateModified: article.updatedAt,
    mainEntityOfPage: url,
    ...(article.author ? { author: { '@type': 'Person', name: article.author } } : {}),
    ...(article.image ? { image: article.image.src } : {}),
    publisher: { '@id': `${siteUrl()}/#organization` },
  };
}

export function jobPostingJsonLd(
  job: { title: string; description: string; postedAt: string; closesAt: string | null; location: string; employmentType: string },
  companyName: string,
) {
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

export function JsonLd({ data }: { data: object }) {
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, '\\u003c') }} />;
}
