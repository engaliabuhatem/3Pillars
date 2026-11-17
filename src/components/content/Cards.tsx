import { MapPin } from 'lucide-react';
import { ArrowIcon } from '@/components/ui/Button';
import { LinkCard } from '@/components/ui/Card';
import { MediaFrame } from '@/components/ui/CmsImage';
import { Icon } from '@/components/ui/Icon';
import { PendingMarker, Tag } from '@/components/ui/Tag';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { InsightCard as Insight, ProjectCard as Project, SectorCard as Sector, ServiceCard as Service } from '@/lib/cms/types';
import { cn, formatDate } from '@/lib/utils';

export function ProjectCard({ project, locale, sizes = '(min-width: 1024px) 33vw, 85vw' }: { project: Project; locale: Locale; sizes?: string }) {
  const t = getDictionary(locale).project;
  return (
    <LinkCard
      href={`/projects/${project.slug}`}
      locale={locale}
      title={project.title}
      titleClassName="px-6 pt-5 text-xl font-semibold text-balance"
      className="h-full"
    >
      <div className="order-first p-2 pb-0">
        <MediaFrame media={project.image} sizes={sizes} ratio="video" className="rounded-[calc(var(--radius-lg)-8px)]" />
      </div>
      <div className="flex flex-1 flex-col gap-4 px-6 pt-2 pb-6">
        <p className="line-clamp-2 text-ink-muted">{project.summary}</p>
        <div className="mt-auto flex flex-wrap items-center gap-2">
          <Tag tone={project.status === 'completed' ? 'green' : 'blue'}>{t[project.status]}</Tag>
          {project.sector && <Tag>{project.sector.name}</Tag>}
          {project.country && (
            <span className="inline-flex items-center gap-1 text-caption text-ink-muted">
              <MapPin aria-hidden className="size-3.5" />
              {project.location ? `${project.location}, ${project.country}` : project.country}
            </span>
          )}
        </div>
        <PendingMarker pending={project.pending} fallbacks={project.fallbacks} locale={locale} />
      </div>
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
      titleClassName={cn('font-semibold text-balance', large ? 'text-h3' : 'text-xl')}
      tone={large ? 'navy' : 'surface'}
      className="h-full gap-4 p-7 md:p-8"
    >
      <span
        className={cn(
          'order-first grid size-12 place-items-center rounded-md',
          large ? 'bg-white/10 text-blue-200' : 'bg-blue-50 text-blue on-navy:bg-white/10 on-navy:text-blue-200',
        )}
      >
        <Icon name={service.icon} className="size-6" />
      </span>
      <p className={cn(large ? 'max-w-md text-lead text-ink-inverse-muted' : 'line-clamp-3 text-ink-muted on-navy:text-ink-inverse-muted')}>{service.summary}</p>
      <span
        aria-hidden
        className={cn('group/button mt-auto inline-flex items-center gap-2 pt-2 font-semibold', large ? 'text-blue-200' : 'text-blue on-navy:text-blue-200')}
      >
        {t.learnMore}
        <ArrowIcon className="group-hover:translate-x-1 rtl:group-hover:-translate-x-1" />
      </span>
      <PendingMarker pending={service.pending} fallbacks={service.fallbacks} locale={locale} />
    </LinkCard>
  );
}

export function SectorTile({ sector, locale }: { sector: Sector; locale: Locale }) {
  return (
    <LinkCard
      href={`/sectors/${sector.slug}`}
      locale={locale}
      title={sector.name}
      titleClassName="relative z-10 text-h3 font-semibold text-white"
      tone="navy"
      className="min-h-80 justify-end p-7"
    >
      <div className="absolute inset-0 order-first">
        <MediaFrame media={sector.image} sizes="(min-width: 1024px) 33vw, 100vw" className="size-full rounded-none" ratio="square" />
        <div aria-hidden className="hero-scrim absolute inset-0" />
      </div>
      <p className="relative z-10 mt-2 max-w-sm text-white/85">{sector.summary}</p>
      <PendingMarker pending={sector.pending} fallbacks={sector.fallbacks} locale={locale} className="relative z-10 mt-3" />
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
      titleClassName="px-6 pt-5 text-xl font-semibold text-balance"
      className="h-full"
    >
      <div className="order-first p-2 pb-0">
        <MediaFrame media={insight.image} sizes="(min-width: 1024px) 33vw, 100vw" className="rounded-[calc(var(--radius-lg)-8px)]" />
      </div>
      <div className="flex flex-1 flex-col gap-3 px-6 pt-2 pb-6">
        <p className="line-clamp-3 text-ink-muted">{insight.excerpt}</p>
        <p className="mt-auto flex flex-wrap items-center gap-x-3 text-caption text-ink-muted">
          {insight.category && <span className="font-semibold text-blue">{insight.category.name}</span>}
          <time dateTime={insight.publishedAt}>{formatDate(insight.publishedAt, locale)}</time>
          <span>{t.minRead(insight.readingMinutes)}</span>
        </p>
        <PendingMarker pending={insight.pending} fallbacks={insight.fallbacks} locale={locale} />
      </div>
    </LinkCard>
  );
}
