import { notFound } from 'next/navigation';
import { ProjectCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { CaseStudyFacts, RelatedLinks } from '@/components/content/Sections';
import { pillarNumber } from '@/components/content/pillarStyle';
import { SectionHeading } from '@/components/ui/Heading';
import { Lightbox } from '@/components/ui/Lightbox';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { Tag } from '@/components/ui/Tag';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getProject } from '@/lib/cms';
import { heading, pageCopy, resolveLocale } from '@/lib/page';
import { buildMetadata } from '@/lib/seo';

type Props = PageProps<'/[locale]/projects/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const project = await getProject(locale, (await params).slug);
  if (!project) return {};
  return buildMetadata({ locale, path: `/projects/${project.slug}/`, title: project.title, description: project.summary, seo: project.seo, image: project.image });
}

/**
 * The case-study order from the content document: overview facts, the
 * challenge, our role, scope of services, approach, results, visuals. Who
 * delivered the project is always stated, first among the facts.
 */
export default async function ProjectPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const project = await getProject(locale, (await params).slug);
  if (!project) notFound();
  const t = getDictionary(locale);
  const index = await pageCopy(locale, 'projects', t.sections.projects);
  const role = [t.project.roles[project.roleKey] ?? project.ourRole, project.ourRoleDetail].filter(Boolean).join(' · ');

  const story = [
    { title: t.sections.challenge, html: project.challenge },
    { title: t.sections.ourRole, text: role },
    { title: t.sections.scopeOfServices, html: project.scopeOfServices },
    { title: t.sections.approachTaken, html: project.approach },
    { title: t.sections.results, html: project.results },
  ].filter((part) => part.html || part.text);

  return (
    <>
      <PageHeader
        background={project.heroImage}
        locale={locale}
        trail={[
          { name: index.title, path: '/projects/' },
          { name: project.title, path: `/projects/${project.slug}/` },
        ]}
        eyebrow={t.filters.types[project.entryType.replace('_', '-')]}
        title={heading({ title: project.title, seo: project.seo })}
        intro={project.summary}
        image={project.image}
        gate={project}
      />

      <Section tone="surface" tight labelledBy="overview-title">
        <div className="container-wide">
          <h2 id="overview-title" className="mb-8 text-h3 font-semibold">
            {t.sections.overview}
          </h2>
          <CaseStudyFacts project={project} locale={locale} />
        </div>
      </Section>

      {story.length > 0 && (
        <Section tight>
          <div className="container-content flex flex-col gap-16">
            {story.map((part, i) => (
              <Reveal key={part.title}>
                <p className="mb-2 text-caption font-semibold text-blue tabular-nums">{pillarNumber(i + 1)}</p>
                <h2 className="mb-6 text-h2 font-semibold">{part.title}</h2>
                {part.html ? <RichText html={part.html} /> : <p className="text-lead">{part.text}</p>}
              </Reveal>
            ))}
          </div>
        </Section>
      )}

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
            <SectionHeading title={t.sections.visuals} />
            <Lightbox items={project.gallery} />
          </div>
        </Section>
      )}

      <RelatedLinks title={t.project.services} base="/services" items={project.services} locale={locale} />

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
