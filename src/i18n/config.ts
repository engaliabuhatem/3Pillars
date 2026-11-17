export const LOCALES = ['en', 'ar'] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = 'en';

export const isLocale = (value: string | undefined): value is Locale =>
  LOCALES.includes(value as Locale);

export const dirFor = (locale: Locale) => (locale === 'ar' ? 'rtl' : 'ltr');

export const otherLocale = (locale: Locale): Locale => (locale === 'ar' ? 'en' : 'ar');

/** BCP 47 tags for Intl. Arabic keeps Latin digits, as the CI stationery does. */
export const INTL_LOCALE: Record<Locale, string> = { en: 'en-GB', ar: 'ar-u-nu-latn' };
