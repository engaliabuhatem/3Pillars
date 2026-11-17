import { ChevronRight } from 'lucide-react';
import type { ReactNode } from 'react';
import { MediaFrame } from '@/components/ui/CmsImage';
import { Eyebrow } from '@/components/ui/Heading';
import { SmartLink } from '@/components/ui/SmartLink';
import { PendingMarker } from '@/components/ui/Tag';
import { LineReveal } from '@/components/motion/LineReveal';
import { Reveal } from '@/components/motion/Reveal';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { Gated, Media } from '@/lib/cms/types';
import { breadcrumbJsonLd, JsonLd } from '@/lib/seo';

export interface Crumb {
  name: string;
  path: string;
}

export function Breadcrumbs({ trail, locale }: { trail: Crumb[]; locale: Locale }) {
  const t = getDictionary(locale);
  const full = [{ name: t.common.home, path: '' }, ...trail];
  return (
    <>
      <nav aria-label={t.a11y.breadcrumb} className="mb-8">
        <ol className="flex flex-wrap items-center gap-1 text-caption text-ink-muted">
          {full.map((crumb, i) => (
            <li key={crumb.path} className="flex items-center gap-1">
              {i > 0 && <ChevronRight aria-hidden className="size-3.5 rtl:-scale-x-100" />}
              {i === full.length - 1 ? (
                <span aria-current="page" className="font-semibold text-navy">
                  {crumb.name}
                </span>
              ) : (
                <SmartLink href={crumb.path || '/'} locale={locale} className="inline-flex min-h-11 items-center hover:text-blue">
                  {crumb.name}
                </SmartLink>
              )}
            </li>
          ))}
        </ol>
      </nav>
      <JsonLd data={breadcrumbJsonLd(locale, full)} />
    </>
  );
}

interface PageHeaderProps {
  locale: Locale;
  trail: Crumb[];
  eyebrow?: string;
  title: string;
  intro?: string;
  image?: Media | null;
  gate?: Gated;
  children?: ReactNode;
}

/**
 * The opening of every interior page: light, quiet, one big title. The
 * header bar sits over it, so the top padding clears the nav.
 */
export function PageHeader({ locale, trail, eyebrow, title, intro, image, gate, children }: PageHeaderProps) {
  return (
    <header className="bg-canvas pt-[calc(var(--spacing-nav)+3rem)] pb-14 md:pt-[calc(var(--spacing-nav)+5rem)] md:pb-20">
      <div className="container-wide">
        <Breadcrumbs trail={trail} locale={locale} />
        <div className="max-w-4xl">
          {eyebrow && <Eyebrow className="mb-5">{eyebrow}</Eyebrow>}
          <h1 className="text-h1 font-semibold text-balance">
            <LineReveal text={title} />
          </h1>
          {intro && (
            <Reveal delay={0.1}>
              <p className="mt-6 max-w-2xl text-lead text-ink-muted">{intro}</p>
            </Reveal>
          )}
          {gate && <PendingMarker pending={gate.pending} fallbacks={gate.fallbacks} locale={locale} className="mt-6" />}
          {children && <div className="mt-8">{children}</div>}
        </div>
        {image && (
          <Reveal delay={0.15} className="mt-14">
            <MediaFrame media={image} sizes="(min-width: 1440px) 1440px, 100vw" ratio="wide" priority />
          </Reveal>
        )}
      </div>
    </header>
  );
}
