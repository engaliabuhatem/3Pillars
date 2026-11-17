import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { Logo } from '@/components/brand/Logo';
import { InsightCard, ProjectCard, SectorTile, ServiceCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { Checkbox, Select, TextArea, TextField } from '@/components/forms/Field';
import { ApproachTimeline } from '@/components/home/ApproachTimeline';
import { PillarsShowcase } from '@/components/home/PillarsShowcase';
import { Accordion } from '@/components/ui/Accordion';
import { Button, ButtonLink } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Carousel } from '@/components/ui/Carousel';
import { MediaFrame } from '@/components/ui/CmsImage';
import { Alert, EmptyState, Skeleton } from '@/components/ui/Feedback';
import { Eyebrow, SectionHeading } from '@/components/ui/Heading';
import { KPICounter } from '@/components/ui/KPICounter';
import { Section } from '@/components/ui/Section';
import { Stepper } from '@/components/ui/Stepper';
import { Tabs } from '@/components/ui/Tabs';
import { PendingMarker, Tag } from '@/components/ui/Tag';
import { getDictionary } from '@/i18n/dictionaries';
import { resolveLocale } from '@/lib/page';
import { FormDemos } from './Demos';
import { FIXTURES } from './fixtures';

export const metadata: Metadata = { title: 'Styleguide', robots: { index: false, follow: false } };

/** Every primitive in one place, in both languages. Not linked, not indexed, off in production unless STYLEGUIDE=true. */
export default async function Styleguide({ params }: PageProps<'/[locale]/_styleguide'>) {
  if (process.env.NODE_ENV === 'production' && process.env.STYLEGUIDE !== 'true') notFound();
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const f = FIXTURES[locale];
  const swatches = ['navy', 'blue', 'green', 'grey'] as const;
  const steps = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950];

  return (
    <>
      <Section className="pt-32">
        <div className="container-wide grid gap-16 [&>*]:min-w-0">
          <SectionHeading as="h1" size="display" eyebrow="Design system" title={f.title} intro={f.intro} />

          <div className="grid gap-6">
            <h2 className="text-h3 font-semibold">Colour</h2>
            {swatches.map((name) => (
              <div key={name} className="grid grid-cols-11 gap-1">
                {steps.map((step) => (
                  <div key={step} className="flex flex-col gap-1 text-[11px]">
                    <span className="h-12 rounded-sm ring-1 ring-hairline" style={{ background: `var(--color-${name}-${step})` }} />
                    {name}-{step}
                  </div>
                ))}
              </div>
            ))}
          </div>

          <div className="grid gap-4">
            <h2 className="text-h3 font-semibold">Type</h2>
            <p className="text-display font-semibold">{f.display}</p>
            <p className="text-h1 font-semibold">H1 · {f.heading}</p>
            <p className="text-h2 font-semibold">H2 · {f.heading}</p>
            <p className="text-h3 font-semibold">H3 · {f.heading}</p>
            <p className="text-lead text-ink-muted">{f.intro}</p>
            <p className="max-w-prose">{f.body}</p>
            <p className="text-caption text-ink-muted">Caption · {f.caption}</p>
            <Eyebrow>Project management services</Eyebrow>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Button>Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="ghost">Ghost</Button>
            <Button disabled>Disabled</Button>
            <ButtonLink href="/request-a-proposal" locale={locale} arrow>
              {t.common.requestProposal}
            </ButtonLink>
            <Tag>Neutral</Tag>
            <Tag tone="blue">Blue</Tag>
            <Tag tone="green">Green</Tag>
            <PendingMarker pending fallbacks={['summary']} locale={locale} />
          </div>

          <div className="grid gap-5 md:grid-cols-3">
            <ServiceCard service={f.service} locale={locale} />
            <ProjectCard project={f.project} locale={locale} />
            <InsightCard insight={f.insight} locale={locale} />
          </div>
          <div className="grid gap-5 md:grid-cols-2">
            <SectorTile sector={f.sector} locale={locale} />
            <Card className="gap-4 p-8">
              <Skeleton className="h-6 w-1/2" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4" />
            </Card>
          </div>

          <div className="grid gap-4">
            <EmptyState>{t.empty.projects}</EmptyState>
            <Alert tone="error">{t.forms.fixErrors}</Alert>
            <Alert tone="success">{t.forms.sent}</Alert>
          </div>

          <MediaFrame media={null} sizes="100vw" ratio="wide" />

          <Carousel label="Carousel">
            {[1, 2, 3, 4, 5].map((n) => (
              <Card key={n} className="h-48 w-72 p-6">
                {f.heading} {n}
              </Card>
            ))}
          </Carousel>

          <Tabs label="Tabs" tabs={[{ label: 'One', content: <p>{f.body}</p> }, { label: 'Two', content: <p>{f.intro}</p> }]} />
          <Accordion name="sg" items={f.faqs} />
          <Stepper steps={t.proposal.steps} current={1} caption={t.proposal.stepOf(2, 4)} />

          <div className="grid max-w-3xl gap-6">
            <TextField label={t.forms.name} required placeholder="—" />
            <TextField label={t.forms.email} required error={t.forms.invalidEmail} defaultValue="name@" />
            <TextField label={t.forms.organisation} disabled defaultValue="—" />
            <Select label={t.proposal.budget} options={Object.entries(t.proposal.budgets).map(([value, label]) => ({ value, label }))} />
            <TextArea label={t.forms.message} hint={t.proposal.scopeHint} />
            <Checkbox label={t.forms.consent} />
            <FormDemos />
          </div>

          <PillarsShowcase pillars={f.pillars} />
          <ApproachTimeline stages={f.stages} />
        </div>
      </Section>
      <Section tone="navy" arcs>
        <div className="container-wide grid gap-12">
          <Logo variant="full" tone="white" className="h-40 w-auto" />
          <div className="grid gap-12 sm:grid-cols-3">
            <KPICounter value={25} suffix="+" label={f.heading} source={f.caption} sourceLabel={t.common.source} />
            <KPICounter value={4.5} label={f.heading} />
            <KPICounter value={98} suffix="%" label={f.heading} />
          </div>
          <div className="flex flex-wrap gap-3">
            <Button variant="inverse">Inverse</Button>
            <Button variant="inverse-outline">Inverse outline</Button>
            <Tag tone="blue">On navy</Tag>
          </div>
        </div>
      </Section>
      <CtaBand locale={locale} title={f.heading} />
    </>
  );
}

