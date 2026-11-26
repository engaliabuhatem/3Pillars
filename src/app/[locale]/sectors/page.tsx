import { Blocks } from '@/components/content/Blocks';
import { SectorTile } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { EmptyState } from '@/components/ui/Feedback';
import { Section } from '@/components/ui/Section';
import { SmartLink } from '@/components/ui/SmartLink';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getSectors } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

const PATH = '/sectors/';

export const generateMetadata = ({ params }: PageProps<'/[locale]/sectors'>) =>
  pageMetadata(params, 'sectors', PATH, (l) => getDictionary(l).sections.sectors);

/** Intro, the sector table (sector and 3 Pillars' focus), then the sector tiles. */
export default async function SectorsPage({ params }: PageProps<'/[locale]/sectors'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, sectors] = await Promise.all([pageCopy(locale, 'sectors', t.sections.sectors), getSectors(locale)]);
  const focused = sectors.filter((sector) => sector.focusSummary);

  return (
    <>
      <PageHeader background={page.heroImage} locale={locale} trail={[{ name: page.title, path: PATH }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} gate={page} />

      {focused.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide">
            <table className="w-full border-collapse text-start">
              <thead>
                <tr className="border-b border-hairline text-caption text-ink-muted">
                  <th scope="col" className="w-2/5 py-4 pe-8 text-start font-semibold">
                    {t.sections.sector}
                  </th>
                  <th scope="col" className="py-4 text-start font-semibold">
                    {t.sections.sectorFocus}
                  </th>
                </tr>
              </thead>
              <tbody>
                {focused.map((sector) => (
                  <tr key={sector.slug} className="border-b border-hairline align-top">
                    <th scope="row" className="py-6 pe-8 text-start">
                      <SmartLink href={`/sectors/${sector.slug}/`} locale={locale} className="text-xl font-semibold hover:text-blue">
                        {sector.name}
                      </SmartLink>
                    </th>
                    <td className="py-6 text-lg text-ink-muted">{sector.focusSummary}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      <Section tight>
        <div className="container-wide">
          {sectors.length === 0 ? (
            <EmptyState>{t.empty.generic}</EmptyState>
          ) : (
            <ul className="grid gap-5 sm:grid-cols-2">
              {sectors.map((sector, i) => (
                <Reveal as="li" key={sector.slug} index={i % 2}>
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
