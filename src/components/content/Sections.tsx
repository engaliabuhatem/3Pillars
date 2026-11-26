import { Accordion } from '@/components/ui/Accordion';
import { SectionHeading } from '@/components/ui/Heading';
import { Section } from '@/components/ui/Section';
import { SmartLink } from '@/components/ui/SmartLink';
import { Reveal } from '@/components/motion/Reveal';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { Faq, Project } from '@/lib/cms/types';
import { formatDate, formatMoney } from '@/lib/utils';
import { pillarNumber } from './pillarStyle';

/*
 * The building blocks of the service, sector and case-study templates. Each
 * renders nothing when it has nothing to show, so a template never prints an
 * empty heading.
 */

/** A capability: title and one-line description, as a quiet card. */
export function CapabilityCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="tile h-full p-7 md:p-8">
      <h3 className="text-xl font-semibold text-balance">{title}</h3>
      {description && <p className="mt-3 text-ink-muted">{description}</p>}
    </div>
  );
}

export function CapabilityGrid({ title, items }: { title: string; items: Array<{ title: string; description: string }> }) {
  if (items.length === 0) return null;
  return (
    <Section tight>
      <div className="container-wide">
        {title && <SectionHeading title={title} />}
        <ul className="grid auto-rows-fr gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((item, i) => (
            <Reveal as="li" key={item.title} index={i % 3}>
              <CapabilityCard title={item.title} description={item.description} />
            </Reveal>
          ))}
        </ul>
      </div>
    </Section>
  );
}

/** A plain bullet list with an optional heading and small print beneath it. */
export function BulletList({ title, items, caveat, tone = 'canvas' }: { title: string; items: string[]; caveat?: string; tone?: 'canvas' | 'surface' }) {
  if (items.length === 0) return null;
  return (
    <Section tone={tone} tight>
      <div className="container-wide">
        {title && <SectionHeading title={title} />}
        <ul className="grid gap-x-10 gap-y-1 md:grid-cols-2">
          {items.map((text, i) => (
            <Reveal as="li" key={text} index={i % 4} className="flex items-start gap-4 border-b border-hairline py-5 text-lg">
              <span aria-hidden className="mt-2.5 size-2 shrink-0 rounded-pill bg-green" />
              {text}
            </Reveal>
          ))}
        </ul>
        {caveat && <p className="mt-8 max-w-3xl text-caption text-ink-muted">{caveat}</p>}
      </div>
    </Section>
  );
}

/** A numbered process; a step may have a title, a body or both. */
export function ProcessSteps({ title, steps }: { title: string; steps: Array<{ title: string; body: string }> }) {
  if (steps.length === 0) return null;
  return (
    <Section tone="navy" arcs tight>
      <div className="container-wide">
        {title && <SectionHeading title={title} />}
        <ol className="grid gap-6 md:grid-cols-2 lg:grid-cols-5">
          {steps.map((step, i) => (
            <Reveal as="li" key={`${step.title}${step.body}`} index={i} className="border-t border-hairline-inverse pt-6">
              <span className="text-caption font-semibold text-blue-200 tabular-nums">{pillarNumber(i + 1)}</span>
              {step.title && <h3 className="mt-2 text-xl font-semibold">{step.title}</h3>}
              {step.body && <p className="mt-3 text-ink-inverse-muted">{step.body}</p>}
            </Reveal>
          ))}
        </ol>
      </div>
    </Section>
  );
}

/** A short titled paragraph, e.g. "Who we support" or "Why a structured PMO matters". */
export function TextPanel({ title, body, tone = 'surface' }: { title: string; body: string; tone?: 'canvas' | 'surface' }) {
  if (!body) return null;
  return (
    <Section tone={tone} tight>
      <div className="container-wide grid gap-6 lg:grid-cols-[1fr_2fr] lg:gap-16">
        <h2 className="text-h2 font-semibold text-balance">{title}</h2>
        <Reveal>
          <p className="text-lead text-ink-muted">{body}</p>
        </Reveal>
      </div>
    </Section>
  );
}

/** Chips linking to related pages: services from a sector, sectors from a service. */
export function RelatedLinks({ title, base, items, locale }: { title: string; base: string; items: Array<{ slug: string; name: string }>; locale: Locale }) {
  if (items.length === 0) return null;
  return (
    <Section tight>
      <div className="container-wide">
        <SectionHeading title={title} />
        <ul className="flex flex-wrap gap-3">
          {items.map((item) => (
            <li key={item.slug}>
              <SmartLink
                href={`${base}/${item.slug}/`}
                locale={locale}
                className="inline-flex min-h-11 items-center rounded-pill bg-surface px-5 font-semibold ring-1 ring-hairline ring-inset hover:text-blue hover:ring-blue"
              >
                {item.name}
              </SmartLink>
            </li>
          ))}
        </ul>
      </div>
    </Section>
  );
}

export function FaqSection({ items, name, locale }: { items: Faq[]; name: string; locale: Locale }) {
  if (items.length === 0) return null;
  return (
    <Section tone="surface" tight>
      <div className="container-wide grid gap-10 lg:grid-cols-[1fr_2fr]">
        <SectionHeading title={getDictionary(locale).sections.faq} />
        <Accordion name={name} items={items} />
      </div>
    </Section>
  );
}

/** The case study's "Project overview": the facts that are known, and always who delivered it. */
export function CaseStudyFacts({ project, locale }: { project: Project; locale: Locale }) {
  const t = getDictionary(locale);
  const dates = [project.facts.start, project.facts.end].filter((d): d is string => Boolean(d)).map((d) => formatDate(d, locale, 'month'));
  const rows: Array<[string, string | null]> = [
    [t.sections.deliveredBy, project.deliveryEntity],
    [t.sections.ourRole, [t.project.roles[project.roleKey] ?? project.ourRole, project.ourRoleDetail].filter(Boolean).join(' · ')],
    [t.project.client, project.client],
    [t.project.country, [project.location, project.country].filter(Boolean).join(', ') || null],
    [t.project.sector, project.sector?.name ?? null],
    [t.project.status, t.project[project.status]],
    [t.project.dates, dates.length ? dates.join(' – ') : null],
    [t.project.value, project.facts.value ? formatMoney(project.facts.value.amount, project.facts.value.currency, locale) : null],
  ];
  return (
    <dl className="grid gap-x-10 gap-y-6 sm:grid-cols-2 lg:grid-cols-4">
      {rows
        .filter(([, value]) => Boolean(value))
        .map(([label, value]) => (
          <div key={label} className="border-t border-hairline pt-4">
            <dt className="text-caption font-semibold text-ink-muted">{label}</dt>
            <dd className="mt-1 text-lg font-semibold">{value}</dd>
          </div>
        ))}
    </dl>
  );
}
