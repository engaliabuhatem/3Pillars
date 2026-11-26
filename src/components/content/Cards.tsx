import { CardMore, LinkCard } from '@/components/ui/Card';
import { MediaFrame } from '@/components/ui/CmsImage';
import { Icon } from '@/components/ui/Icon';
import { PendingMarker } from '@/components/ui/Tag';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { InsightCard as Insight, ProjectCard as Project, SectorCard as Sector, ServiceCard as Service } from '@/lib/cms/types';
import { cn, formatDate } from '@/lib/utils';
import { PILLAR_BAR, pillarNumber } from './pillarStyle';

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
      href={`/projects/${project.slug}/`}
      locale={locale}
      title={project.title}
      eyebrow={join(project.sector?.name, t.project.roles[project.roleKey] ?? project.ourRole)}
      media={<MediaFrame media={project.image} sizes={sizes} ratio="video" bleed zoom />}
    >
      <p className="mt-3 line-clamp-2 text-ink-muted">{project.summary}</p>
      <p className="mt-3 text-caption text-ink-muted">
        {t.sections.deliveredBy}: {project.deliveryEntity}
      </p>
      <CardMore>{t.common.learnMore}</CardMore>
      <PendingMarker pending={project.pending} fallbacks={project.fallbacks} locale={locale} className="mt-4" />
    </LinkCard>
  );
}

export function ServiceCard({ service, locale }: { service: Service; locale: Locale }) {
  const t = getDictionary(locale).common;
  return (
    <LinkCard
      href={`/services/${service.slug}/`}
      locale={locale}
      title={service.name}
      eyebrow={service.pillar ? pillarNumber(service.pillar.number) : undefined}
      media={
        <span aria-hidden className="mx-7 mt-7 flex items-center gap-3 text-blue md:mx-8 md:mt-8">
          <Icon name={service.icon} className="size-9" />
          {service.pillar && <span className={cn('h-1 w-8 rounded-pill', PILLAR_BAR[service.pillar.color])} />}
        </span>
      }
    >
      {service.summary && <p className="mt-3 line-clamp-3 text-ink-muted">{service.summary}</p>}
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
      href={`/sectors/${sector.slug}/`}
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
      {sector.focusSummary && <p className="mt-2 line-clamp-3 max-w-sm text-white/85">{sector.focusSummary}</p>}
      <CardMore pushDown={false}>{t.learnMore}</CardMore>
      <PendingMarker pending={sector.pending} fallbacks={sector.fallbacks} locale={locale} className="mt-4" />
    </LinkCard>
  );
}

export function InsightCard({ insight, locale }: { insight: Insight; locale: Locale }) {
  const dictionary = getDictionary(locale);
  const t = dictionary.common;
  return (
    <LinkCard
      href={`/insights/${insight.slug}/`}
      locale={locale}
      title={insight.title}
      eyebrow={join(dictionary.insights.kinds[insight.kind], insight.category?.name)}
      media={<MediaFrame media={insight.image} sizes="(min-width: 1024px) 33vw, 100vw" bleed zoom />}
    >
      <p className="mt-3 line-clamp-3 text-ink-muted">{insight.excerpt}</p>
      <p className="mt-auto pt-6 text-caption text-ink-muted">
        {insight.publishedAt && (
          <>
            <time dateTime={insight.publishedAt}>{formatDate(insight.publishedAt, locale)}</time>
            {' · '}
          </>
        )}
        {t.minRead(insight.readingMinutes)}
      </p>
      <PendingMarker pending={insight.pending} fallbacks={insight.fallbacks} locale={locale} className="mt-4" />
    </LinkCard>
  );
}
