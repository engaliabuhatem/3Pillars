import { INTL_LOCALE, type Locale } from '@/i18n/config';

export function cn(...classes: Array<string | false | null | undefined>): string {
  return classes.filter(Boolean).join(' ');
}

export const isExternal = (href: string) => /^(https?:|mailto:|tel:)/.test(href);

/** CMS links are locale-free ("/services"); the site prefixes the active locale. */
export function localize(href: string, locale: Locale): string {
  if (!href || isExternal(href) || href.startsWith('#')) return href;
  const path = href.startsWith('/') ? href : `/${href}`;
  if (/^\/(en|ar)(\/|$)/.test(path)) return path;
  return path === '/' ? `/${locale}` : `/${locale}${path}`;
}

export function formatDate(iso: string, locale: Locale, style: 'long' | 'month' = 'long'): string {
  const options: Intl.DateTimeFormatOptions =
    style === 'month' ? { year: 'numeric', month: 'short' } : { year: 'numeric', month: 'long', day: 'numeric' };
  return new Intl.DateTimeFormat(INTL_LOCALE[locale], options).format(new Date(iso));
}

export function formatNumber(value: number, locale: Locale, fractionDigits = 0): string {
  return new Intl.NumberFormat(INTL_LOCALE[locale], {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  }).format(value);
}

export function formatMoney(amount: number, currency: string, locale: Locale): string {
  return new Intl.NumberFormat(INTL_LOCALE[locale], {
    style: 'currency',
    currency,
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(amount);
}
