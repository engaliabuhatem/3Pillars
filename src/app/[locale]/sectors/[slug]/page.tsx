import { notFound } from 'next/navigation';
import { ProjectCard, ServiceCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { SectionHeading } from '@/components/ui/Heading';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getSector } from '@/lib/cms';
import { resolveLocale } from '@/lib/page';
import { buildMetadata } from '@/lib/seo';

type Props = PageProps<'/[locale]/sectors/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const sector = await getSector(locale, (await params).slug);
  if (!sector) return {};
  return buildMetadata({ locale, path: `/sectors/${sector.slug}`, title: sector.name, description: sector.summary, seo: sector.seo, image: sector.image });
}

export default async function SectorPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const sector = await getSector(locale, (await params).slug);
  if (!sector) notFound();
  const t = getDictionary(locale);

  return (
    <>
      <PageHeader
        locale={locale}
        trail={[
          { name: t.sections.sectors, path: '/sectors' },
          { name: sector.name, path: `/sectors/${sector.slug}` },
        ]}
        eyebrow={t.sections.sectors}
        title={sector.name}
        intro={sector.summary}
        image={sector.image}
        gate={sector}
      />
      {sector.intro && (
        <Section tone="surface" tight>
          <div className="container-wide">
            <Reveal>
              <RichText html={sector.intro} className="text-lead" />
            </Reveal>
          </div>
        </Section>
      )}
      {sector.services.length > 0 && (
        <Section tight>
          <div className="container-wide">
            <SectionHeading title={t.common.relatedServices} />
            <ul className="grid auto-rows-fr gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {sector.services.map((service, i) => (
                <Reveal as="li" key={service.slug} index={i % 3}>
                  <ServiceCard service={service} locale={locale} />
                </Reveal>
              ))}
            </ul>
          </div>
        </Section>
      )}
      {sector.projects.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide">
            <SectionHeading title={t.common.relatedProjects} />
            <ul className="grid gap-5 md:grid-cols-3">
              {sector.projects.map((project) => (
                <li key={project.slug}>
                  <ProjectCard project={project} locale={locale} />
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
