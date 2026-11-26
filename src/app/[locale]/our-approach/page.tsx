import { Blocks } from '@/components/content/Blocks';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { ApproachTimeline } from '@/components/home/ApproachTimeline';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getApproachStages } from '@/lib/cms';
import { pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

export const generateMetadata = ({ params }: PageProps<'/[locale]/approach'>) =>
  pageMetadata(params, 'approach', '/approach', (l) => getDictionary(l).sections.approach);

export default async function ApproachPage({ params }: PageProps<'/[locale]/approach'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, stages] = await Promise.all([pageCopy(locale, 'approach', t.sections.approach), getApproachStages(locale)]);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: '/approach' }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} image={page.image} gate={page} />
      {stages.length > 0 && (
        <Section tone="surface">
          <div className="container-wide">
            <ApproachTimeline stages={stages} />
          </div>
        </Section>
      )}
      <Blocks blocks={page.blocks} locale={locale} />
      <CtaBand locale={locale} />
    </>
  );
}
