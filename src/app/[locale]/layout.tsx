import type { Metadata, Viewport } from 'next';
import { notFound } from 'next/navigation';
import Script from 'next/script';
import { INTRO_SCRIPT, LogoIntro } from '@/components/brand/LogoIntro';
import { Analytics } from '@/components/layout/Analytics';
import { CookieNotice, WhatsAppButton } from '@/components/layout/Extras';
import { Footer } from '@/components/layout/Footer';
import { Header } from '@/components/layout/Header';
import { NavigationMarker } from '@/components/layout/NavigationMarker';
import { PillarProgress } from '@/components/layout/PillarProgress';
import { SmoothScroll } from '@/components/layout/SmoothScroll';
import { RevealController } from '@/components/motion/RevealController';
import { ToastProvider } from '@/components/ui/Toast';
import { LOCALES, dirFor, isLocale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import { LocaleProvider } from '@/i18n/LocaleProvider';
import { getHome, getNavigation, getOffices, getSettings } from '@/lib/cms';
import { CONSULTATION_PATH } from '@/components/content/CtaBand';
import type { NavItem } from '@/lib/cms/types';
import { buildMetadata, JsonLd, organizationJsonLd, websiteJsonLd } from '@/lib/seo';
import { sourceSans, tajawal } from '../fonts';
import '../globals.css';

export const viewport: Viewport = {
  themeColor: '#191747',
  width: 'device-width',
  initialScale: 1,
};

export function generateStaticParams() {
  return LOCALES.map((locale) => ({ locale }));
}

export async function generateMetadata({ params }: LayoutProps<'/[locale]'>): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const settings = await getSettings(locale);
  return {
    ...(await buildMetadata({ locale, path: '' })),
    title: { default: settings.seoTitle || settings.companyName, template: `%s · ${settings.shortName}` },
    applicationName: settings.shortName,
  };
}

export default async function LocaleLayout({ children, params }: LayoutProps<'/[locale]'>) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const [settings, navigation, offices, home] = await Promise.all([
    getSettings(locale),
    getNavigation(locale),
    getOffices(locale),
    getHome(locale),
  ]);
  const t = getDictionary(locale);
  const homeStartsDark = home.sections[0]?.kind === 'hero';
  const ctaItem = findCta(navigation.header);
  const cta = { label: ctaItem?.label || t.common.requestConsultation, href: ctaItem?.link || CONSULTATION_PATH };

  return (
    <html lang={locale} dir={dirFor(locale)} className={`${sourceSans.variable} ${tajawal.variable}`} suppressHydrationWarning>
      <body>
        <Script id="logo-intro" strategy="beforeInteractive">
          {INTRO_SCRIPT}
        </Script>
        <LocaleProvider locale={locale}>
          <ToastProvider>
            <a
              href="#main"
              className="fixed start-4 top-4 z-[70] -translate-y-24 rounded-md bg-navy px-4 py-3 font-semibold text-white focus:translate-y-0"
            >
              {t.a11y.skip}
            </a>
            <Header navigation={navigation} shortName={settings.shortName} cta={cta} homeStartsDark={homeStartsDark} />
            <main id="main" tabIndex={-1} className="outline-none">
              {children}
            </main>
            <Footer navigation={navigation} settings={settings} offices={offices} locale={locale} />
            {settings.showWhatsapp && settings.whatsapp && <WhatsAppButton number={settings.whatsapp} />}
            <CookieNotice text={settings.cookieNotice} />
            {settings.analytics && <Analytics config={settings.analytics} />}
            <PillarProgress />
            <SmoothScroll />
            <RevealController />
            <NavigationMarker />
            <LogoIntro />
          </ToastProvider>
        </LocaleProvider>
        <JsonLd data={organizationJsonLd(settings, offices, locale)} />
        <JsonLd data={websiteJsonLd(settings, locale)} />
      </body>
    </html>
  );
}

/** The header button: the navigation item marked as such in the admin (at any level). */
function findCta(items: NavItem[]): NavItem | undefined {
  for (const item of items) {
    if (item.isCta) return item;
    const child = findCta(item.children);
    if (child) return child;
  }
  return undefined;
}
