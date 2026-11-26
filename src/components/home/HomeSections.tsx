import { CtaBand } from '@/components/content/CtaBand';
import { InsightCard, ProjectCard, SectorTile } from '@/components/content/Cards';
import { PillarCard, ValuePoints } from '@/components/content/Pillars';
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
import { TrustStrip } from './TrustStrip';
import { VideoHero } from './VideoHero';

type Props<K extends HomeSection['kind']> = { section: Extract<HomeSection, { kind: K }>; locale: Locale; staging: boolean };

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

function Intro({ section, locale }: Props<'intro'>) {
  if (!section.title && !section.intro) return null;
  return (
    <Section labelledBy={section.title ? 'intro-title' : undefined}>
      <div className="container-wide grid gap-8 lg:grid-cols-12 lg:gap-16">
        {section.title && (
          <h2 id="intro-title" className="text-h2 font-semibold text-balance lg:col-span-5">
            {section.title}
          </h2>
        )}
        {section.intro && (
          <Reveal className="lg:col-span-7">
            <p className="text-lead text-ink-muted">{section.intro}</p>
          </Reveal>
        )}
        <PendingMarker pending={section.pending} fallbacks={section.fallbacks} locale={locale} className="lg:col-span-12" />
      </div>
    </Section>
  );
}

function Pillars({ section, locale, staging }: Props<'pillars'>) {
  const t = getDictionary(locale);
  return (
    <Section tone="surface" labelledBy="pillars-title">
      <div className="container-wide">
        <SectionHeading
          id="pillars-title"
          {...heading(section, t.sections.services)}
          action={<SeeAll section={section} locale={locale} href="/services/" label={t.common.viewAll} />}
        />
        <ol className="grid auto-rows-fr gap-5 md:grid-cols-3">
          {section.data.map((pillar, i) => (
            <Reveal as="li" key={pillar.id} index={i}>
              <PillarCard pillar={pillar} locale={locale} staging={staging} />
            </Reveal>
          ))}
        </ol>
      </div>
    </Section>
  );
}

function Value({ section, locale }: Props<'value'>) {
  return (
    <Section tone="navy" arcs labelledBy={section.title ? 'value-title' : undefined}>
      <div className="container-wide">
        {section.title && <SectionHeading id="value-title" {...heading(section, '')} />}
        <ValuePoints points={section.data} locale={locale} />
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
          action={<SeeAll section={section} locale={locale} href="/projects/" label={t.common.allProjects} />}
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

function Sectors({ section, locale }: Props<'sectors'>) {
  const t = getDictionary(locale);
  return (
    <Section labelledBy="sectors-title">
      <div className="container-wide">
        <SectionHeading
          id="sectors-title"
          {...heading(section, t.sections.sectors)}
          action={<SeeAll section={section} locale={locale} href="/sectors/" label={t.common.viewAll} />}
        />
        <ul className="grid gap-5 sm:grid-cols-2">
          {section.data.map((sector, i) => (
            <Reveal as="li" key={sector.slug} index={i % 2}>
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
          action={<SeeAll section={section} locale={locale} href="/insights/" label={t.common.viewAll} />}
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

/** Home renders its sections in the CMS order; `staging` shows the "Proposed" tag on pillar 03. */
export function HomeSections({ sections, locale, staging }: { sections: HomeSection[]; locale: Locale; staging: boolean }) {
  return sections.map((section) => {
    const props = { locale, staging };
    switch (section.kind) {
      case 'hero':
        return <VideoHero key="hero" hero={section.data} />;
      case 'intro':
        return <Intro key="intro" section={section} {...props} />;
      case 'pillars':
        return <Pillars key="pillars" section={section} {...props} />;
      case 'sectors':
        return <Sectors key="sectors" section={section} {...props} />;
      case 'value':
        return <Value key="value" section={section} {...props} />;
      case 'trust':
        return <Trust key="trust" section={section} {...props} />;
      case 'kpis':
        return <Kpis key="kpis" section={section} {...props} />;
      case 'projects':
        return <Projects key="projects" section={section} {...props} />;
      case 'testimonial':
        return <TestimonialBand key="testimonial" section={section} {...props} />;
      case 'insights':
        return <Insights key="insights" section={section} {...props} />;
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
