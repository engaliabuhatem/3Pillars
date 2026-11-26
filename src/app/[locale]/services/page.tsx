import { Blocks } from '@/components/content/Blocks';
import { ServiceCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { ProposedTag } from '@/components/content/Pillars';
import { PILLAR_BAR, pillarNumber } from '@/components/content/pillarStyle';
import { EmptyState } from '@/components/ui/Feedback';
import { Section } from '@/components/ui/Section';
import { SmartLink } from '@/components/ui/SmartLink';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getPillars, getServices, getSettings } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';
import { cn } from '@/lib/utils';

const PATH = '/services/';

export const generateMetadata = ({ params }: PageProps<'/[locale]/services'>) =>
  pageMetadata(params, 'services', PATH, (l) => getDictionary(l).sections.services);

/** Intro, the service-line table (one row per pillar), then every service page. */
export default async function ServicesPage({ params }: PageProps<'/[locale]/services'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, services, pillars, settings] = await Promise.all([
    pageCopy(locale, 'services', t.sections.services),
    getServices(locale),
    getPillars(locale),
    getSettings(locale),
  ]);
  const lines = pillars.filter((pillar) => pillar.covers);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: PATH }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} gate={page} />

      {lines.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide">
            <table className="w-full border-collapse text-start">
              <thead>
                <tr className="border-b border-hairline text-caption text-ink-muted">
                  <th scope="col" className="w-2/5 py-4 pe-8 text-start font-semibold">
                    {t.sections.serviceLine}
                  </th>
                  <th scope="col" className="py-4 text-start font-semibold">
                    {t.sections.whatItCovers}
                  </th>
                </tr>
              </thead>
              <tbody>
                {lines.map((pillar) => (
                  <tr key={pillar.id} className="border-b border-hairline align-top">
                    <th scope="row" className="py-6 pe-8 text-start">
                      <span className="flex items-center gap-2.5 text-caption tabular-nums text-ink-muted">
                        <span aria-hidden className={cn('h-1 w-6 rounded-pill', PILLAR_BAR[pillar.color])} />
                        {pillarNumber(pillar.number)}
                      </span>
                      {pillar.service ? (
                        <SmartLink href={`/services/${pillar.service.slug}/`} locale={locale} className="mt-2 block text-xl font-semibold hover:text-blue">
                          {pillar.name}
                        </SmartLink>
                      ) : (
                        <span className="mt-2 block text-xl font-semibold">{pillar.name}</span>
                      )}
                      <ProposedTag pillar={pillar} staging={settings.showPendingContent} locale={locale} />
                    </th>
                    <td className="py-6 text-lg text-ink-muted">{pillar.covers}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      <Section tight>
        <div className="container-wide">
          {services.length === 0 ? (
            <EmptyState>{t.empty.generic}</EmptyState>
          ) : (
            <ul className="grid auto-rows-fr gap-5 sm:grid-cols-2">
              {services.map((service, i) => (
                <Reveal as="li" key={service.slug} index={i % 2}>
                  <ServiceCard service={service} locale={locale} />
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
