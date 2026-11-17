import { ExternalLink, Mail, Phone } from 'lucide-react';
import { MediaFrame } from '@/components/ui/CmsImage';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { Office } from '@/lib/cms/types';

/**
 * Static map image plus an "Open in Maps" link: no third-party map script,
 * cookies or layout shift until the visitor chooses to open one.
 */
export function OfficeCard({ office, locale }: { office: Office; locale: Locale }) {
  const t = getDictionary(locale).common;
  const mapsUrl = office.coordinates
    ? `https://www.google.com/maps/search/?api=1&query=${office.coordinates.lat},${office.coordinates.lng}`
    : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${office.address} ${office.city} ${office.country}`)}`;

  return (
    <article className="tile overflow-hidden">
      {office.mapImage && <MediaFrame media={office.mapImage} sizes="(min-width: 1024px) 40vw, 100vw" ratio="video" bleed />}
      <div className="grid gap-3 p-7 md:p-8">
        <h3 className="text-xl font-semibold">
          {office.city}, {office.country}
        </h3>
        {office.address && <p className="whitespace-pre-line text-ink-muted">{office.address}</p>}
        {office.phone && (
          <a href={`tel:${office.phone.replace(/\s/g, '')}`} dir="ltr" className="inline-flex min-h-11 w-fit items-center gap-2 hover:text-blue">
            <Phone aria-hidden className="size-4 text-green" />
            {office.phone}
          </a>
        )}
        {office.email && (
          <a href={`mailto:${office.email}`} className="inline-flex min-h-11 w-fit items-center gap-2 hover:text-blue">
            <Mail aria-hidden className="size-4 text-green" />
            {office.email}
          </a>
        )}
        <a href={mapsUrl} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 w-fit items-center gap-2 font-semibold text-blue hover:underline">
          {t.openInMaps}
          <ExternalLink aria-hidden className="size-4" />
        </a>
      </div>
    </article>
  );
}
