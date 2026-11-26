import type { Locale } from '@/i18n/config';
import type { Home, Navigation, SiteSettings } from '@/lib/cms/types';

/**
 * What the site shows when the CMS cannot be reached and nothing is cached.
 * Deliberately thin: the brand, the way to get in touch, and nothing that
 * could go stale or claim anything. Detail pages have no fallback; their last
 * good render keeps being served by the cache instead. Nothing here is
 * indexable.
 */

const NAME = { en: '3 Pillars Project Management Services', ar: 'ثري بيلارز لخدمات إدارة المشاريع' };
const NOT_INDEXABLE = { en: false, ar: false };

export function fallbackSettings(locale: Locale): SiteSettings {
  const ar = locale === 'ar';
  return {
    companyName: NAME[locale],
    shortName: ar ? 'ثري بيلارز' : '3 Pillars',
    tagline: '',
    groupRelationship: '',
    hero: {
      h1: '',
      eyebrow: '',
      headline: NAME[locale],
      subline: '',
      primary: { label: ar ? 'اطلب استشارة' : 'Request a Consultation', href: '/contact/request-a-consultation/' },
      secondary: { label: ar ? 'تواصل معنا' : 'Contact Us', href: '/contact/' },
      video: { mp4: null, webm: null, mobile: null },
      poster: null,
      posterMobile: null,
    },
    logos: { light: null, dark: null, favicon: null },
    phone: '',
    email: '',
    whatsapp: '',
    showWhatsapp: false,
    address: '',
    businessHours: '',
    socials: [],
    seoTitle: NAME[locale],
    seoDescription: '',
    homeSeo: { title: '', description: '', h1: '', image: null, indexable: NOT_INDEXABLE },
    preferWww: false,
    defaultOgImage: null,
    analytics: null,
    cookieNotice: '',
    consentText: '',
    turnstileEnabled: false,
    turnstileSiteKey: '',
    capabilityGate: false,
    capabilityStatement: null,
    comingSoon: false,
    showPendingContent: false,
    copyPending: true,
  };
}

export function fallbackNavigation(locale: Locale): Navigation {
  const ar = locale === 'ar';
  const item = (label: string, link: string, isCta = false) => ({ label, link, megaMenu: '' as const, isCta, children: [] });
  return {
    header: [
      item(ar ? 'الخدمات' : 'Services', '/services/'),
      item(ar ? 'من نحن' : 'About Us', '/about-us/'),
      item(ar ? 'تواصل' : 'Contact', '/contact/'),
    ],
    footer: [],
    legal: [item(ar ? 'الخصوصية' : 'Privacy', '/privacy/')],
    mega: { services: [], sectors: [] },
  };
}

export function fallbackHome(locale: Locale): Home {
  const hero = fallbackSettings(locale).hero;
  const blank = { eyebrow: '', title: '', intro: '', ctaLabel: '', ctaLink: '', secondaryLabel: '', secondaryLink: '', image: null };
  return { sections: [{ ...blank, kind: 'hero', data: hero }] };
}
