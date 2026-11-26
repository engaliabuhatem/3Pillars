import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { HomeSections } from '@/components/home/HomeSections';
import { isLocale } from '@/i18n/config';
import { getHome, getSettings } from '@/lib/cms';
import { buildMetadata } from '@/lib/seo';

export async function generateMetadata({ params }: PageProps<'/[locale]'>): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const settings = await getSettings(locale);
  return buildMetadata({ locale, path: '', seo: settings.homeSeo });
}

export default async function HomePage({ params }: PageProps<'/[locale]'>) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const [home, settings] = await Promise.all([getHome(locale), getSettings(locale)]);
  return <HomeSections sections={home.sections} locale={locale} staging={settings.showPendingContent} />;
}
