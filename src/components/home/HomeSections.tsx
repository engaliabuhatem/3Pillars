import { CtaBand } from '@/components/content/CtaBand';
import { InsightCard, ProjectCard, SectorTile, ServiceCard } from '@/components/content/Cards';
import { ButtonLink } from '@/components/ui/Button';
import { Carousel } from '@/components/ui/Carousel';
import { SectionHeading } from '@/components/ui/Heading';
import { KPICounter } from '@/components/ui/KPICounter';
import { Section } from '@/components/ui/Section';
import { PendingMarker } from '@/components/ui/Tag';
import { Reveal } from '@/components/motion/Reveal';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { HomeSection } from '@/lib/cms/types';
import { cn } from '@/lib/utils';
import { ApproachTimeline } from './ApproachTimeline';
import { PillarsShowcase } from './PillarsShowcase';
import { TrustStrip } from './TrustStrip';
import { VideoHero } from './VideoHero';

type Props<K extends HomeSection['kind']> = { section: Extract<HomeSection, { kind: K }>; locale: Locale };

function heading(section: HomeSection, fallbackTitle: string) {
  return { eyebrow: section.eyebrow || undefined, title: section.title || fallbackTitle, intro: section.intro || undefined };
}

function SeeAll({ section, locale, href, label }: { section: HomeSection; locale: Locale; href: string; label: string }) {
  return (
    <ButtonLink href={section.ctaLink || href} locale={locale} variant="secondary" arrow>
      {section.ctaLabel || label}
    </ButtonLink>
  );
}

function Pillars({ section }: Props<'pillars'>) {
  return (
    <Section tone="surface" labelledBy="pillars-title">
      <div className="container-wide">
        <SectionHeading id="pillars-title" {...heading(section, '')} />
        <PillarsShowcase pillars={section.data} />
      </div>
    </Section>
  );
}

function Services({ section, locale }: Props<'services'>) {
  const t = getDictionary(locale);
  const [flagship, ...rest] = section.data;
  return (
    <Section labelledBy="services-title">
      <div className="container-wide">
        <SectionHeading
          id="services-title"
          {...heading(section, t.sections.services)}
          action={<SeeAll section={section} locale={locale} href="/services" label={t.common.viewAll} />}
        />
        <ul className="grid auto-rows-fr gap-5 md:grid-cols-2 lg:grid-cols-4">
          {flagship && (
            <Reveal as="li" className="md:col-span-2 md:row-span-2">
              <ServiceCard service={flagship} locale={locale} large />
            </Reveal>
          )}
          {rest.map((service, i) => (
            <Reveal as="li" key={service.slug} index={i}>
              <ServiceCard service={service} locale={locale} />
            </Reveal>
          ))}
        </ul>
      </div>
    </Section>
  );
}

function Kpis({ section, locale }: Props<'kpis'>) {
  const t = getDictionary(locale).common;
  return (
    <Section tone="navy" arcs labelledBy={section.title ? 'kpis-title' : undefined}>
      <div className="container-wide">
        {section.title && <SectionHeading id="kpis-title" {...heading(section, '')} />}
        <ul className="grid gap-12 sm:grid-cols-2 lg:grid-cols-4">
          {section.data.map((kpi) => (
            <li key={kpi.id} className="border-t border-hairline-inverse pt-6">
              <KPICounter value={kpi.value} prefix={kpi.prefix} suffix={kpi.suffix} label={kpi.label} source={kpi.source} sourceLabel={t.source} />
              <PendingMarker pending={kpi.pending} fallbacks={kpi.fallbacks} locale={locale} className="mt-3" />
            </li>
          ))}
        </ul>
      </div>
    </Section>
  );
}

function Projects({ section, locale }: Props<'projects'>) {
  const t = getDictionary(locale);
  return (
    <Section tone="surface" labelledBy="projects-title">
      <div className="container-wide">
        <SectionHeading
          id="projects-title"
          {...heading(section, t.sections.projects)}
          action={<SeeAll section={section} locale={locale} href="/projects" label={t.common.allProjects} />}
        />
        <Carousel label={section.title || t.sections.projects} itemClassName="w-[85vw] sm:w-[26rem]">
          {section.data.map((project) => (
            <ProjectCard key={project.slug} project={project} locale={locale} sizes="(min-width: 640px) 26rem, 85vw" />
          ))}
        </Carousel>
      </div>
    </Section>
  );
}

function Approach({ section, locale }: Props<'approach'>) {
  const t = getDictionary(locale);
  return (
    <Section labelledBy="approach-title">
      <div className="container-wide">
        <SectionHeading
          id="approach-title"
          {...heading(section, t.sections.approach)}
          action={section.ctaLabel ? <SeeAll section={section} locale={locale} href="/approach" label={t.common.learnMore} /> : undefined}
        />
        <ApproachTimeline stages={section.data} />
      </div>
    </Section>
  );
}

function Sectors({ section, locale }: Props<'sectors'>) {
  const t = getDictionary(locale);
  return (
    <Section tone="surface" labelledBy="sectors-title">
      <div className="container-wide">
        <SectionHeading
          id="sectors-title"
          {...heading(section, t.sections.sectors)}
          action={<SeeAll section={section} locale={locale} href="/sectors" label={t.common.viewAll} />}
        />
        <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {section.data.map((sector, i) => (
            <Reveal as="li" key={sector.slug} index={i} className={cn(i === 0 && 'lg:col-span-2')}>
              <SectorTile sector={sector} locale={locale} />
            </Reveal>
          ))}
        </ul>
      </div>
    </Section>
  );
}

function TestimonialBand({ section, locale }: Props<'testimonial'>) {
  const quote = section.data;
  return (
    <Section>
      <figure className="container-content max-w-4xl">
        <Reveal>
          <blockquote className="text-h2 font-medium text-balance">
            <p>“{quote.quote}”</p>
          </blockquote>
          <figcaption className="mt-8 text-lead">
            <span className="font-semibold">{quote.person}</span>
            {(quote.role || quote.company) && (
              <span className="text-ink-muted"> — {[quote.role, quote.company].filter(Boolean).join(', ')}</span>
            )}
          </figcaption>
          <PendingMarker pending={quote.pending} fallbacks={quote.fallbacks} locale={locale} className="mt-4" />
        </Reveal>
      </figure>
    </Section>
  );
}

function Insights({ section, locale }: Props<'insights'>) {
  const t = getDictionary(locale);
  return (
    <Section labelledBy="insights-title">
      <div className="container-wide">
        <SectionHeading
          id="insights-title"
          {...heading(section, t.sections.insights)}
          action={<SeeAll section={section} locale={locale} href="/insights" label={t.common.viewAll} />}
        />
        <ul className="grid gap-5 md:grid-cols-3">
          {section.data.map((insight, i) => (
            <Reveal as="li" key={insight.slug} index={i}>
              <InsightCard insight={insight} locale={locale} />
            </Reveal>
          ))}
        </ul>
      </div>
    </Section>
  );
}

function Trust({ section, locale }: Props<'trust'>) {
  return (
    <Section tight tone="surface" className="border-b border-hairline">
      <div className="container-wide">
        {section.eyebrow && <p className="eyebrow mb-8 text-center text-ink-muted">{section.eyebrow}</p>}
        <TrustStrip clients={section.data} label={section.eyebrow || getDictionary(locale).sections.about} />
      </div>
    </Section>
  );
}

export function HomeSections({ sections, locale }: { sections: HomeSection[]; locale: Locale }) {
  return sections.map((section) => {
    switch (section.kind) {
      case 'hero':
        return <VideoHero key="hero" hero={section.data} />;
      case 'trust':
        return <Trust key="trust" section={section} locale={locale} />;
      case 'pillars':
        return <Pillars key="pillars" section={section} locale={locale} />;
      case 'services':
        return <Services key="services" section={section} locale={locale} />;
      case 'kpis':
        return <Kpis key="kpis" section={section} locale={locale} />;
      case 'projects':
        return <Projects key="projects" section={section} locale={locale} />;
      case 'approach':
        return <Approach key="approach" section={section} locale={locale} />;
      case 'sectors':
        return <Sectors key="sectors" section={section} locale={locale} />;
      case 'testimonial':
        return <TestimonialBand key="testimonial" section={section} locale={locale} />;
      case 'insights':
        return <Insights key="insights" section={section} locale={locale} />;
      case 'cta':
        return (
          <CtaBand
            key="cta"
            locale={locale}
            eyebrow={section.eyebrow}
            title={section.title}
            intro={section.intro}
            primary={{ label: section.ctaLabel, href: section.ctaLink }}
            secondary={{ label: section.secondaryLabel, href: section.secondaryLink }}
          />
        );
    }
  });
}
