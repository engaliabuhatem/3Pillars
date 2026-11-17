import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { HomeSections } from '@/components/home/HomeSections';
import { isLocale } from '@/i18n/config';
import { getHome } from '@/lib/cms';
import { buildMetadata } from '@/lib/seo';

export async function generateMetadata({ params }: PageProps<'/[locale]'>): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return buildMetadata({ locale, path: '' });
}

export default async function HomePage({ params }: PageProps<'/[locale]'>) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const home = await getHome(locale);
  return <HomeSections sections={home.sections} locale={locale} />;
}
