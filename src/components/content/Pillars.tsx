import { Card, CardMore, LinkCard } from '@/components/ui/Card';
import { PendingMarker, Tag } from '@/components/ui/Tag';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { Pillar, ValuePoint } from '@/lib/cms/types';
import { cn } from '@/lib/utils';
import { PILLAR_BAR, pillarNumber } from './pillarStyle';

/**
 * The "Proposed" tag on pillar 03: shown only on staging (content awaiting
 * approval visible), never on the live site.
 */
export function ProposedTag({ pillar, staging, locale }: { pillar: Pick<Pillar, 'isProposed'>; staging: boolean; locale: Locale }) {
  if (!pillar.isProposed || !staging) return null;
  return <Tag tone="warning">{getDictionary(locale).common.proposed}</Tag>;
}

function PillarNumber({ pillar }: { pillar: Pillar }) {
  return (
    <p className="eyebrow flex items-center gap-2.5 tabular-nums text-ink-muted on-navy:text-ink-inverse-muted">
      <span aria-hidden className={cn('h-1 w-8 rounded-pill', PILLAR_BAR[pillar.color])} />
      {pillarNumber(pillar.number)}
    </p>
  );
}

/** A pillar as a numbered card in its colour, linking to its service page. */
export function PillarCard({ pillar, locale, staging }: { pillar: Pillar; locale: Locale; staging: boolean }) {
  const t = getDictionary(locale).common;
  const body = (
    <>
      <p className="mt-3 text-ink-muted">{pillar.summary}</p>
      <span className="mt-4 inline-flex flex-wrap gap-2">
        <ProposedTag pillar={pillar} staging={staging} locale={locale} />
        <PendingMarker pending={pillar.pending} fallbacks={pillar.fallbacks} locale={locale} />
      </span>
    </>
  );
  if (!pillar.service) {
    return (
      <Card className="h-full p-7 md:p-8">
        <PillarNumber pillar={pillar} />
        <h3 className="mt-4 text-[1.375rem] leading-tight font-semibold tracking-tight text-balance">{pillar.name}</h3>
        {body}
      </Card>
    );
  }
  return (
    <LinkCard href={`/services/${pillar.service.slug}/`} locale={locale} title={pillar.name} eyebrow={<PillarNumber pillar={pillar} />}>
      {body}
      <CardMore>{t.learnMore}</CardMore>
    </LinkCard>
  );
}

/** "Clarity / Control / Growth": three short statements in a row. */
export function ValuePoints({ points, locale }: { points: ValuePoint[]; locale: Locale }) {
  return (
    <ul className="grid gap-10 md:grid-cols-3">
      {points.map((point, i) => (
        <li key={point.id} className="border-t border-hairline pt-6 on-navy:border-hairline-inverse">
          <p className="eyebrow tabular-nums text-ink-muted on-navy:text-ink-inverse-muted">{pillarNumber(i + 1)}</p>
          <h3 className="mt-3 text-h3 font-semibold">{point.title}</h3>
          <p className="mt-3 text-lead text-ink-muted on-navy:text-ink-inverse-muted">{point.body}</p>
          <PendingMarker pending={point.pending} fallbacks={point.fallbacks} locale={locale} className="mt-4" />
        </li>
      ))}
    </ul>
  );
}

/** One pillar on Our Approach: number, name, summary and its core outcomes. */
export function PillarSection({ pillar, locale, staging }: { pillar: Pillar; locale: Locale; staging: boolean }) {
  const t = getDictionary(locale).sections;
  return (
    <article aria-labelledby={`pillar-${pillar.number}`} className="grid gap-8 border-t border-hairline pt-10 lg:grid-cols-12 lg:gap-16">
      <div className="lg:col-span-5">
        <PillarNumber pillar={pillar} />
        <h2 id={`pillar-${pillar.number}`} className="mt-4 text-h2 font-semibold text-balance">
          {pillar.name}
        </h2>
        <span className="mt-4 inline-flex flex-wrap gap-2">
          <ProposedTag pillar={pillar} staging={staging} locale={locale} />
          <PendingMarker pending={pillar.pending} fallbacks={pillar.fallbacks} locale={locale} />
        </span>
      </div>
      <div className="lg:col-span-7">
        <p className="text-lead text-ink-muted">{pillar.detail}</p>
        {pillar.coreOutcomes && (
          <div className="mt-8 rounded-card bg-surface p-7 ring-1 ring-hairline ring-inset">
            <h3 className="eyebrow text-blue">{t.coreOutcomes}</h3>
            <p className="mt-3 text-lg">{pillar.coreOutcomes}</p>
          </div>
        )}
      </div>
    </article>
  );
}
