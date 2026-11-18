import type { Locale } from '@/i18n/config';
import type { Home, Navigation, SiteSettings } from '@/lib/cms/types';

/**
 * What the site shows when the CMS cannot be reached and nothing is cached.
 * Deliberately thin: the brand, the way to get in touch, and nothing that
 * could go stale or claim anything. Detail pages have no fallback; their last
 * good render keeps being served by the cache instead.
 */

const NAME = { en: '3 Pillars Project Management Services', ar: 'ثري بيلارز لخدمات إدارة المشاريع' };

export function fallbackSettings(locale: Locale): SiteSettings {
  const ar = locale === 'ar';
  return {
    companyName: NAME[locale],
    shortName: ar ? 'ثري بيلارز' : '3 Pillars',
    tagline: ar ? 'خدمات إدارة المشاريع' : 'Project management services',
    groupRelationship: '',
    hero: {
      eyebrow: ar ? 'خدمات إدارة المشاريع' : 'Project Management Services',
      headline: NAME[locale],
      subline: '',
      primary: { label: ar ? 'اطلب عرضاً' : 'Request a proposal', href: '/request-a-proposal' },
      secondary: { label: ar ? 'اتصل بنا' : 'Contact us', href: '/contact' },
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
    socials: [],
    seoTitle: NAME[locale],
    seoDescription: '',
    defaultOgImage: null,
    analytics: null,
    cookieNotice: '',
    turnstileEnabled: false,
    turnstileSiteKey: '',
    capabilityGate: false,
    capabilityStatement: null,
    comingSoon: false,
    showPendingContent: false,
  };
}

export function fallbackNavigation(locale: Locale): Navigation {
  const ar = locale === 'ar';
  const item = (label: string, link: string) => ({ label, link, megaMenu: '' as const, children: [] });
  return {
    header: [
      item(ar ? 'الخدمات' : 'Services', '/services'),
      item(ar ? 'المشاريع' : 'Projects', '/projects'),
      item(ar ? 'من نحن' : 'About', '/about'),
      item(ar ? 'اتصل بنا' : 'Contact', '/contact'),
    ],
    footer: [],
    legal: [item(ar ? 'الخصوصية' : 'Privacy', '/privacy')],
    mega: { services: [], sectors: [] },
  };
}

export function fallbackHome(locale: Locale): Home {
  const hero = fallbackSettings(locale).hero;
  const blank = { eyebrow: '', title: '', intro: '', ctaLabel: '', ctaLink: '', secondaryLabel: '', secondaryLink: '', image: null };
  return { sections: [{ ...blank, kind: 'hero', data: hero }] };
}
