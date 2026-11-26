import 'server-only';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { isLocale, type Locale } from '@/i18n/config';
import { getPage } from './cms';
import { CmsUnavailable } from './cms/client';
import type { Page, Seo } from './cms/types';
import { buildMetadata } from './seo';

export async function resolveLocale(params: Promise<{ locale: string }>): Promise<Locale> {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  return locale;
}

/**
 * The editable copy around a listing page (services, projects, contact…).
 * Each has a CMS Page with the same slug for its title, intro, SEO and any
 * extra blocks; until one is approved the interface wording is used.
 */
export async function pageCopy(locale: Locale, slug: string, fallbackTitle: string): Promise<Page> {
  let page: Page | null = null;
  try {
    page = await getPage(locale, slug);
  } catch (error) {
    if (!(error instanceof CmsUnavailable)) throw error;
  }
  return (
    page ?? {
      slug,
      path: '',
      title: fallbackTitle,
      eyebrow: '',
      intro: '',
      ctaLabel: '',
      image: null,
      blocks: [],
      seo: EMPTY_SEO,
      updatedAt: '',
    }
  );
}

export const EMPTY_SEO: Seo = { title: '', description: '', h1: '', image: null, indexable: { en: false, ar: false } };

/** The page's one <h1>: the H1 field when set, otherwise its title. */
export const heading = (item: { title?: string; name?: string; seo: Seo }) => item.seo.h1 || item.title || item.name || '';

export async function pageMetadata(params: Promise<{ locale: string }>, slug: string, path: string, fallbackTitle: (l: Locale) => string): Promise<Metadata> {
  const locale = await resolveLocale(params);
  const page = await pageCopy(locale, slug, fallbackTitle(locale));
  return buildMetadata({ locale, path, title: page.title, description: page.intro, seo: page.seo, image: page.image });
}
