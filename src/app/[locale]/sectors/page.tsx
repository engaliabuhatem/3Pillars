import { Blocks } from '@/components/content/Blocks';
import { SectorTile } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { EmptyState } from '@/components/ui/Feedback';
import { Section } from '@/components/ui/Section';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getSectors } from '@/lib/cms';
import { pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

export const generateMetadata = ({ params }: PageProps<'/[locale]/sectors'>) =>
  pageMetadata(params, 'sectors', '/sectors', (l) => getDictionary(l).sections.sectors);

export default async function SectorsPage({ params }: PageProps<'/[locale]/sectors'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, sectors] = await Promise.all([pageCopy(locale, 'sectors', t.sections.sectors), getSectors(locale)]);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: '/sectors' }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} gate={page} />
      <Section tight>
        <div className="container-wide">
          {sectors.length === 0 ? (
            <EmptyState>{t.empty.generic}</EmptyState>
          ) : (
            <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {sectors.map((sector, i) => (
                <Reveal as="li" key={sector.slug} index={i % 3}>
                  <SectorTile sector={sector} locale={locale} />
                </Reveal>
              ))}
            </ul>
          )}
        </div>
      </Section>
      <Blocks blocks={page.blocks} locale={locale} />
      <CtaBand locale={locale} />
    </>
  );
}
