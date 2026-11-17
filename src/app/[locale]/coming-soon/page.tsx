import type { Metadata } from 'next';
import { StatusScreen } from '@/components/content/StatusScreen';
import { getDictionary } from '@/i18n/dictionaries';
import { getSettings } from '@/lib/cms';
import { resolveLocale } from '@/lib/page';

export const metadata: Metadata = { robots: { index: false } };

/** Shown to every visitor while Site settings → "Show the coming-soon page" is on (see proxy.ts). */
export default async function ComingSoonPage({ params }: PageProps<'/[locale]/coming-soon'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const settings = await getSettings(locale);

  return (
    <StatusScreen title={t.comingSoon.title} body={t.comingSoon.body}>
      {settings.email && (
        <a href={`mailto:${settings.email}`} className="inline-flex min-h-11 items-center rounded-md bg-white px-6 font-semibold text-navy">
          {settings.email}
        </a>
      )}
      {settings.phone && (
        <a href={`tel:${settings.phone.replace(/\s/g, '')}`} dir="ltr" className="inline-flex min-h-11 items-center rounded-md px-6 font-semibold ring-1 ring-white/40 ring-inset">
          {settings.phone}
        </a>
      )}
    </StatusScreen>
  );
}
