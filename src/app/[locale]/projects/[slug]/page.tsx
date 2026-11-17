import { notFound } from 'next/navigation';
import type { ReactNode } from 'react';
import { ProjectCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { SectionHeading } from '@/components/ui/Heading';
import { Lightbox } from '@/components/ui/Lightbox';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { SmartLink } from '@/components/ui/SmartLink';
import { Tag } from '@/components/ui/Tag';
import { Reveal } from '@/components/motion/Reveal';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import { getProject } from '@/lib/cms';
import type { Project } from '@/lib/cms/types';
import { resolveLocale } from '@/lib/page';
import { buildMetadata } from '@/lib/seo';
import { formatDate, formatMoney } from '@/lib/utils';

type Props = PageProps<'/[locale]/projects/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const project = await getProject(locale, (await params).slug);
  if (!project) return {};
  return buildMetadata({ locale, path: `/projects/${project.slug}`, title: project.title, description: project.summary, seo: project.seo, image: project.image });
}

function Facts({ project, locale }: { project: Project; locale: Locale }) {
  const t = getDictionary(locale).project;
  const { facts } = project;
  const rows: Array<[string, ReactNode]> = [
    [t.client, project.client],
    [t.location, [project.location, project.country].filter(Boolean).join(', ')],
    [t.sector, project.sector && <SmartLink href={`/sectors/${project.sector.slug}`} locale={locale} className="text-blue hover:underline">{project.sector.name}</SmartLink>],
    [t.value, facts.value && formatMoney(facts.value.amount, facts.value.currency, locale)],
    [
      t.duration,
      facts.start &&
        `${formatDate(facts.start, locale, 'month')} – ${facts.end ? formatDate(facts.end, locale, 'month') : t.ongoing}${facts.durationMonths ? ` · ${t.months(facts.durationMonths)}` : ''}`,
    ],
    [t.role, project.role],
    [t.status, <Tag key="status" tone={project.status === 'completed' ? 'green' : 'blue'}>{t[project.status]}</Tag>],
  ];

  return (
    <aside className="tile p-7 md:p-8 lg:sticky lg:top-[calc(var(--spacing-nav)+2rem)]">
      <dl className="divide-y divide-hairline">
        {rows
          .filter(([, value]) => Boolean(value))
          .map(([label, value]) => (
            <div key={label} className="grid gap-1 py-4 first:pt-0 last:pb-0">
              <dt className="text-caption font-semibold text-ink-muted">{label}</dt>
              <dd className="font-semibold">{value}</dd>
            </div>
          ))}
      </dl>
      {project.services.length > 0 && (
        <div className="mt-6 border-t border-hairline pt-6">
          <p className="mb-3 text-caption font-semibold text-ink-muted">{t.services}</p>
          <ul className="flex flex-wrap gap-2">
            {project.services.map((service) => (
              <li key={service.slug}>
                <SmartLink href={`/services/${service.slug}`} locale={locale}>
                  <Tag tone="blue">{service.name}</Tag>
                </SmartLink>
              </li>
            ))}
          </ul>
        </div>
      )}
    </aside>
  );
}

export default async function ProjectPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const project = await getProject(locale, (await params).slug);
  if (!project) notFound();
  const t = getDictionary(locale);

  const story = [
    { title: t.sections.challenge, html: project.challenge },
    { title: t.sections.ourApproach, html: project.approach },
    { title: t.sections.outcome, html: project.outcome },
  ].filter((part) => part.html);

  return (
    <>
      <PageHeader
        locale={locale}
        trail={[
          { name: t.sections.projects, path: '/projects' },
          { name: project.title, path: `/projects/${project.slug}` },
        ]}
        eyebrow={project.sector?.name || t.sections.projects}
        title={project.title}
        intro={project.summary}
        image={project.image}
        gate={project}
      />

      <Section tone="surface" tight>
        <div className="container-wide grid gap-14 lg:grid-cols-[minmax(0,1fr)_22rem] lg:gap-20">
          <div className="flex flex-col gap-16">
            {story.map((part, i) => (
              <Reveal key={part.title}>
                <p className="mb-2 text-caption font-semibold text-blue tabular-nums">0{i + 1}</p>
                <h2 className="mb-6 text-h2 font-semibold">{part.title}</h2>
                <RichText html={part.html} />
              </Reveal>
            ))}
          </div>
          <Facts project={project} locale={locale} />
        </div>
      </Section>

      {project.metrics.length > 0 && (
        <Section tone="navy" arcs tight>
          <div className="container-wide">
            <SectionHeading title={t.sections.results} />
            <ul className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
              {project.metrics.map((metric) => (
                <li key={metric.label} className="border-t border-hairline-inverse pt-6">
                  <p className="text-[clamp(2.5rem,2rem+2vw,3.75rem)] leading-none font-semibold tabular-nums">
                    {metric.value}
                    <span className="text-h3 text-blue-200">{metric.unit}</span>
                  </p>
                  <p className="mt-3 text-lg text-ink-inverse-muted">{metric.label}</p>
                  {metric.delta && <Tag tone="green" className="mt-3">{metric.delta}</Tag>}
                </li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      {project.gallery.some((item) => item.image) && (
        <Section tight>
          <div className="container-wide">
            <SectionHeading title={t.sections.gallery} />
            <Lightbox items={project.gallery} />
          </div>
        </Section>
      )}

      {project.related.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide">
            <SectionHeading title={t.common.relatedProjects} />
            <ul className="grid gap-5 md:grid-cols-3">
              {project.related.map((related) => (
                <li key={related.slug}>
                  <ProjectCard project={related} locale={locale} />
                </li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      <CtaBand locale={locale} />
    </>
  );
}
