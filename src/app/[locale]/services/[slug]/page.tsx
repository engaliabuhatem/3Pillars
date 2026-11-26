import { notFound } from 'next/navigation';
import { ProjectCard, SectorTile } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { BulletList, CapabilityGrid, FaqSection, ProcessSteps, TextPanel } from '@/components/content/Sections';
import { MediaFrame } from '@/components/ui/CmsImage';
import { SectionHeading } from '@/components/ui/Heading';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getService } from '@/lib/cms';
import { heading, pageCopy, resolveLocale } from '@/lib/page';
import { buildMetadata } from '@/lib/seo';

type Props = PageProps<'/[locale]/services/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const service = await getService(locale, (await params).slug);
  if (!service) return {};
  return buildMetadata({ locale, path: `/services/${service.slug}/`, title: service.name, description: service.summary, seo: service.seo, image: service.image });
}

/**
 * intro → capabilities (cards) or bullet list → process steps → extra section
 * → who we support → related sectors → related projects → FAQ → the page's
 * own call to action. Every part is optional and disappears when empty.
 */
export default async function ServicePage({ params }: Props) {
  const locale = await resolveLocale(params);
  const service = await getService(locale, (await params).slug);
  if (!service) notFound();
  const t = getDictionary(locale);
  const index = await pageCopy(locale, 'services', t.sections.services);

  return (
    <>
      <PageHeader
        background={service.heroImage}
        locale={locale}
        trail={[
          { name: index.title, path: '/services/' },
          { name: service.name, path: `/services/${service.slug}/` },
        ]}
        eyebrow={index.title}
        title={heading({ name: service.name, seo: service.seo })}
        intro={service.summary}
        gate={service}
      />

      {service.intro && (
        <Section tone="surface" tight>
          <div className="container-wide grid gap-14 lg:grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)] lg:gap-20">
            <Reveal>
              <RichText html={service.intro} className="text-lead" />
            </Reveal>
            {service.image && <MediaFrame media={service.image} sizes="(min-width: 1024px) 40vw, 100vw" ratio="portrait" />}
          </div>
        </Section>
      )}

      <CapabilityGrid title={service.capabilitiesTitle} items={service.capabilities} />
      <BulletList title={service.bulletsTitle} items={service.bullets.map((b) => b.text)} caveat={service.scopeCaveat} />
      <ProcessSteps title={service.stepsTitle} steps={service.steps} />
      <TextPanel title={service.contextTitle} body={service.contextBody} />
      <TextPanel title={t.sections.whoWeSupport} body={service.whoWeSupport} tone="canvas" />

      {service.relatedSectors.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide">
            <SectionHeading title={t.common.relatedSectors} />
            <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {service.relatedSectors.map((sector, i) => (
                <Reveal as="li" key={sector.slug} index={i % 4}>
                  <SectorTile sector={sector} locale={locale} />
                </Reveal>
              ))}
            </ul>
          </div>
        </Section>
      )}

      {service.projects.length > 0 && (
        <Section tight>
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

      <FaqSection items={service.faqs} name="service-faq" locale={locale} />
      <CtaBand
        locale={locale}
        title={service.ctaHeadline || undefined}
        primary={service.ctaLabel ? { label: service.ctaLabel, href: '/contact/request-a-consultation/' } : undefined}
      />
    </>
  );
}
