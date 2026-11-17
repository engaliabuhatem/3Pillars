import { notFound } from 'next/navigation';
import { ProjectCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { Accordion } from '@/components/ui/Accordion';
import { MediaFrame } from '@/components/ui/CmsImage';
import { SectionHeading } from '@/components/ui/Heading';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { SmartLink } from '@/components/ui/SmartLink';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getService } from '@/lib/cms';
import { resolveLocale } from '@/lib/page';
import { buildMetadata } from '@/lib/seo';

type Props = PageProps<'/[locale]/services/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const service = await getService(locale, (await params).slug);
  if (!service) return {};
  return buildMetadata({ locale, path: `/services/${service.slug}`, title: service.name, description: service.summary, seo: service.seo, image: service.image });
}

export default async function ServicePage({ params }: Props) {
  const locale = await resolveLocale(params);
  const service = await getService(locale, (await params).slug);
  if (!service) notFound();
  const t = getDictionary(locale);

  return (
    <>
      <PageHeader
        locale={locale}
        trail={[
          { name: t.sections.services, path: '/services' },
          { name: service.name, path: `/services/${service.slug}` },
        ]}
        eyebrow={t.sections.services}
        title={service.name}
        intro={service.summary}
        gate={service}
      />

      <Section tone="surface" tight>
        <div className="container-wide grid gap-14 lg:grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)] lg:gap-20">
          <Reveal>
            <RichText html={service.overview} className="text-lead" />
          </Reveal>
          {service.image && <MediaFrame media={service.image} sizes="(min-width: 1024px) 40vw, 100vw" ratio="portrait" />}
        </div>
      </Section>

      {service.deliverables.length > 0 && (
        <Section tight>
          <div className="container-wide">
            <SectionHeading title={t.sections.deliverables} />
            <ul className="grid gap-x-10 gap-y-1 md:grid-cols-2">
              {service.deliverables.map((item, i) => (
                <Reveal as="li" key={item.text} index={i} className="flex items-start gap-4 border-b border-hairline py-5 text-lg">
                  <span aria-hidden className="mt-2.5 size-2 shrink-0 rounded-pill bg-green" />
                  {item.text}
                </Reveal>
              ))}
            </ul>
          </div>
        </Section>
      )}

      {service.steps.length > 0 && (
        <Section tone="navy" arcs tight>
          <div className="container-wide">
            <SectionHeading title={t.sections.steps} />
            <ol className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {service.steps.map((step, i) => (
                <Reveal as="li" key={step.title} index={i} className="border-t border-hairline-inverse pt-6">
                  <span className="text-caption font-semibold text-blue-200 tabular-nums">0{i + 1}</span>
                  <h3 className="mt-2 text-xl font-semibold">{step.title}</h3>
                  <p className="mt-3 text-ink-inverse-muted">{step.body}</p>
                </Reveal>
              ))}
            </ol>
          </div>
        </Section>
      )}

      {service.projects.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide">
            <SectionHeading title={t.common.relatedProjects} />
            <ul className="grid gap-5 md:grid-cols-3">
              {service.projects.map((project) => (
                <li key={project.slug}>
                  <ProjectCard project={project} locale={locale} />
                </li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      {service.sectors.length > 0 && (
        <Section tight>
          <div className="container-wide">
            <SectionHeading title={t.common.relatedSectors} />
            <ul className="flex flex-wrap gap-3">
              {service.sectors.map((sector) => (
                <li key={sector.slug}>
                  <SmartLink
                    href={`/sectors/${sector.slug}`}
                    locale={locale}
                    className="inline-flex min-h-11 items-center rounded-pill bg-surface px-5 font-semibold ring-1 ring-hairline ring-inset hover:text-blue hover:ring-blue"
                  >
                    {sector.name}
                  </SmartLink>
                </li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      {service.faqs.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide grid gap-10 lg:grid-cols-[1fr_2fr]">
            <SectionHeading title={t.sections.faq} />
            <Accordion name="service-faq" items={service.faqs} />
          </div>
        </Section>
      )}

      <CtaBand locale={locale} />
    </>
  );
}

