import { Blocks } from '@/components/content/Blocks';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { PillarFlow } from '@/components/content/PillarFlow';
import { PillarSection } from '@/components/content/Pillars';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getPillars, getSettings } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

const PATH = '/our-approach/';

export const generateMetadata = ({ params }: PageProps<'/[locale]/our-approach'>) =>
  pageMetadata(params, 'our-approach', PATH, (l) => getDictionary(l).sections.approach);

/**
 * The three-pillar framework: each pillar with its summary and core outcomes,
 * then how they work together. The page's first block carries the "How the
 * pillars work together" wording; the flow runs in the order it describes:
 * market intelligence, business development, then project and programme
 * management (pillar 03 → 02 → 01).
 */
export default async function OurApproachPage({ params }: PageProps<'/[locale]/our-approach'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, pillars, settings] = await Promise.all([
    pageCopy(locale, 'our-approach', t.sections.approach),
    getPillars(locale),
    getSettings(locale),
  ]);
  const [together, ...rest] = page.blocks;
  const flow = [...pillars].sort((a, b) => b.number - a.number).map(({ number, name, color }) => ({ number, name, color }));

  return (
    <>
      <PageHeader background={page.heroImage} locale={locale} trail={[{ name: page.title, path: PATH }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} gate={page} />

      {pillars.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide grid gap-16">
            {pillars.map((pillar) => (
              <PillarSection key={pillar.id} pillar={pillar} locale={locale} staging={settings.showPendingContent} />
            ))}
          </div>
        </Section>
      )}

      {together && (
        <Section tone="navy" arcs labelledBy="together-title">
          <div className="container-wide">
            <div className="max-w-3xl">
              <h2 id="together-title" className="text-h1 font-semibold text-balance">
                {together.title}
              </h2>
              {together.body && <RichText html={together.body} className="mt-6 text-lead text-ink-inverse-muted" />}
            </div>
            {flow.length > 0 && (
              <div className="mt-16">
                <PillarFlow steps={flow} label={together.title} />
              </div>
            )}
          </div>
        </Section>
      )}

      <Blocks blocks={rest} locale={locale} />
      <CtaBand locale={locale} />
    </>
  );
}
