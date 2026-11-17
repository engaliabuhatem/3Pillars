import { CardMore, LinkCard } from '@/components/ui/Card';
import { MediaFrame } from '@/components/ui/CmsImage';
import { Icon } from '@/components/ui/Icon';
import { PendingMarker } from '@/components/ui/Tag';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { InsightCard as Insight, ProjectCard as Project, SectorCard as Sector, ServiceCard as Service } from '@/lib/cms/types';
import { cn, formatDate } from '@/lib/utils';

/*
 * Content cards in the Apple pattern: image edge to edge, a quiet grey label,
 * the title, one or two lines of grey summary, and "Learn more ›" in blue.
 * No pills, outlines or icon boxes competing with the title.
 */

const join = (...parts: Array<string | null | undefined | false>) => parts.filter(Boolean).join(' · ');

export function ProjectCard({ project, locale, sizes = '(min-width: 1024px) 33vw, 85vw' }: { project: Project; locale: Locale; sizes?: string }) {
  const t = getDictionary(locale);
  return (
    <LinkCard
      href={`/projects/${project.slug}`}
      locale={locale}
      title={project.title}
      eyebrow={join(project.sector?.name, t.project[project.status])}
      media={<MediaFrame media={project.image} sizes={sizes} ratio="video" bleed zoom />}
    >
      <p className="mt-3 line-clamp-2 text-ink-muted">{project.summary}</p>
      {project.country && (
        <p className="mt-3 text-caption text-ink-muted">{join(project.location, project.country)}</p>
      )}
      <CardMore>{t.common.learnMore}</CardMore>
      <PendingMarker pending={project.pending} fallbacks={project.fallbacks} locale={locale} className="mt-4" />
    </LinkCard>
  );
}

export function ServiceCard({ service, locale, large }: { service: Service; locale: Locale; large?: boolean }) {
  const t = getDictionary(locale).common;
  return (
    <LinkCard
      href={`/services/${service.slug}`}
      locale={locale}
      title={service.name}
      tone={large ? 'navy' : 'surface'}
      titleSize={large ? 'text-h2' : undefined}
      bodyClassName={large ? 'p-8 md:p-12' : undefined}
      media={
        <span
          aria-hidden
          className={cn('mx-7 mt-7 md:mx-8 md:mt-8', large ? 'text-blue-200 md:mx-12 md:mt-12' : 'text-blue')}
        >
          <Icon name={service.icon} className={large ? 'size-12' : 'size-9'} />
        </span>
      }
    >
      <p className={cn('mt-3', large ? 'max-w-md text-lead text-ink-inverse-muted' : 'line-clamp-3 text-ink-muted')}>{service.summary}</p>
      <CardMore>{t.learnMore}</CardMore>
      <PendingMarker pending={service.pending} fallbacks={service.fallbacks} locale={locale} className="mt-4" />
    </LinkCard>
  );
}

/** A full-bleed image tile with the words over a navy scrim, like Apple's product tiles. */
export function SectorTile({ sector, locale }: { sector: Sector; locale: Locale }) {
  const t = getDictionary(locale).common;
  return (
    <LinkCard
      href={`/sectors/${sector.slug}`}
      locale={locale}
      title={sector.name}
      tone="navy"
      className="min-h-96"
      bodyClassName="relative z-10 justify-end"
      titleSize="text-h3"
      media={
        <div className="absolute inset-0">
          <MediaFrame media={sector.image} sizes="(min-width: 1024px) 33vw, 100vw" className="size-full" ratio="square" bleed zoom />
          <div aria-hidden className="hero-scrim absolute inset-0" />
        </div>
      }
    >
      <p className="mt-2 max-w-sm text-white/85">{sector.summary}</p>
      <CardMore pushDown={false}>{t.learnMore}</CardMore>
      <PendingMarker pending={sector.pending} fallbacks={sector.fallbacks} locale={locale} className="mt-4" />
    </LinkCard>
  );
}

export function InsightCard({ insight, locale }: { insight: Insight; locale: Locale }) {
  const t = getDictionary(locale).common;
  return (
    <LinkCard
      href={`/insights/${insight.slug}`}
      locale={locale}
      title={insight.title}
      eyebrow={insight.category?.name}
      media={<MediaFrame media={insight.image} sizes="(min-width: 1024px) 33vw, 100vw" bleed zoom />}
    >
      <p className="mt-3 line-clamp-3 text-ink-muted">{insight.excerpt}</p>
      <p className="mt-auto pt-6 text-caption text-ink-muted">
        <time dateTime={insight.publishedAt}>{formatDate(insight.publishedAt, locale)}</time>
        {' · '}
        {t.minRead(insight.readingMinutes)}
      </p>
      <PendingMarker pending={insight.pending} fallbacks={insight.fallbacks} locale={locale} className="mt-4" />
    </LinkCard>
  );
}
