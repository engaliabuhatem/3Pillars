import { ChevronRight } from 'lucide-react';
import type { ReactNode } from 'react';
import { ThreeArcs } from '@/components/brand/ThreeArcs';
import { CmsImage } from '@/components/ui/CmsImage';
import { Eyebrow } from '@/components/ui/Heading';
import { SmartLink } from '@/components/ui/SmartLink';
import { PendingMarker } from '@/components/ui/Tag';
import { LineReveal } from '@/components/motion/LineReveal';
import { Reveal } from '@/components/motion/Reveal';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import { getSettings } from '@/lib/cms';
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
        <ol className="flex flex-wrap items-center gap-1 text-caption text-ink-muted on-navy:text-ink-inverse-muted">
          {full.map((crumb, i) => (
            <li key={crumb.path} className="flex items-center gap-1">
              {i > 0 && <ChevronRight aria-hidden className="size-3.5 rtl:-scale-x-100" />}
              {i === full.length - 1 ? (
                <span aria-current="page" className="font-semibold text-navy on-navy:text-white">
                  {crumb.name}
                </span>
              ) : (
                <SmartLink href={crumb.path || '/'} locale={locale} className="inline-flex min-h-11 items-center hover:text-blue on-navy:hover:text-white">
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
  /** The page's own hero background (its "Hero background" field). */
  background?: Media | null;
  /** A second choice when there is no hero background, e.g. the page's cover image. */
  image?: Media | null;
  gate?: Gated;
  children?: ReactNode;
}

/**
 * The opening of every interior page: a navy hero with one big white title.
 * Behind it sits the page's hero background, else its cover image, else the
 * site's default hero background, else the brand arcs on navy, so no page
 * opens without one. The scrim keeps the white text readable over any photo.
 * The header bar sits over it, so the top padding clears the nav.
 */
export async function PageHeader({ locale, trail, eyebrow, title, intro, background, image, gate, children }: PageHeaderProps) {
  const backdrop = background ?? image ?? (await getSettings(locale)).defaultHeroImage;

  return (
    <header
      data-surface="navy"
      data-hero-dark
      className="relative isolate flex min-h-[26rem] items-end overflow-hidden bg-navy pt-[calc(var(--spacing-nav)+3rem)] pb-14 text-white md:min-h-[32rem] md:pt-[calc(var(--spacing-nav)+5rem)] md:pb-20"
    >
      {backdrop ? (
        <div aria-hidden className="absolute inset-0 -z-10">
          <CmsImage media={{ ...backdrop, alt: '' }} sizes="100vw" priority />
          <div className="hero-scrim absolute inset-0" />
        </div>
      ) : (
        <ThreeArcs className="pointer-events-none absolute inset-0 -z-10 size-full opacity-60" />
      )}
      <div className="container-wide w-full">
        <Breadcrumbs trail={trail} locale={locale} />
        <div className="max-w-4xl">
          {eyebrow && <Eyebrow className="mb-5">{eyebrow}</Eyebrow>}
          <h1 className="text-h1 font-semibold text-balance">
            <LineReveal text={title} />
          </h1>
          {intro && (
            <Reveal delay={0.1}>
              <p className="mt-6 max-w-2xl text-lead text-white/85">{intro}</p>
            </Reveal>
          )}
          {gate && <PendingMarker pending={gate.pending} fallbacks={gate.fallbacks} locale={locale} className="mt-6" />}
          {children && <div className="mt-8">{children}</div>}
        </div>
      </div>
    </header>
  );
}
