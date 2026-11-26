import { notFound } from 'next/navigation';
import { InsightCard, ProjectCard, ServiceCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { BulletList, FaqSection } from '@/components/content/Sections';
import { SectionHeading } from '@/components/ui/Heading';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getSector } from '@/lib/cms';
import { heading, pageCopy, resolveLocale } from '@/lib/page';
import { buildMetadata } from '@/lib/seo';

type Props = PageProps<'/[locale]/sectors/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const sector = await getSector(locale, (await params).slug);
  if (!sector) return {};
  return buildMetadata({ locale, path: `/sectors/${sector.slug}/`, title: sector.name, description: sector.focusSummary, seo: sector.seo, image: sector.image });
}

/**
 * intro → list (its heading set per sector) → "Our focus" → related services
 * → related projects and insights → FAQ → call to action. Empty parts vanish.
 */
export default async function SectorPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const sector = await getSector(locale, (await params).slug);
  if (!sector) notFound();
  const t = getDictionary(locale);
  const index = await pageCopy(locale, 'sectors', t.sections.sectors);

  return (
    <>
      <PageHeader
        locale={locale}
        trail={[
          { name: index.title, path: '/sectors/' },
          { name: sector.name, path: `/sectors/${sector.slug}/` },
        ]}
        eyebrow={sector.name}
        title={heading({ name: sector.name, seo: sector.seo })}
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

      <BulletList title={sector.listTitle} items={sector.listItems.map((item) => item.text)} caveat={sector.scopeCaveat} />

      {sector.ourFocus && (
        <Section tone="navy" arcs tight labelledBy="focus-title">
          <div className="container-wide max-w-4xl">
            <h2 id="focus-title" className="eyebrow text-blue-200">
              {t.sections.ourFocus}
            </h2>
            <p className="mt-5 text-h3 font-medium text-balance">{sector.ourFocus}</p>
          </div>
        </Section>
      )}

      {sector.relatedServices.length > 0 && (
        <Section tight>
          <div className="container-wide">
            <SectionHeading title={t.common.relatedServices} />
            <ul className="grid auto-rows-fr gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {sector.relatedServices.map((service, i) => (
                <Reveal as="li" key={service.slug} index={i % 4}>
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

      {sector.insights.length > 0 && (
        <Section tight>
          <div className="container-wide">
            <SectionHeading title={t.common.relatedInsights} />
            <ul className="grid gap-5 md:grid-cols-3">
              {sector.insights.map((insight) => (
                <li key={insight.slug}>
                  <InsightCard insight={insight} locale={locale} />
                </li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      <FaqSection items={sector.faqs} name="sector-faq" locale={locale} />
      <CtaBand locale={locale} />
    </>
  );
}
