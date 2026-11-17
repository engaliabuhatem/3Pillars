import { InsightCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { Pagination } from '@/components/content/Pagination';
import { EmptyState } from '@/components/ui/Feedback';
import { Section } from '@/components/ui/Section';
import { SmartLink } from '@/components/ui/SmartLink';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getInsights } from '@/lib/cms';
import { pageCopy, pageMetadata, resolveLocale } from '@/lib/page';
import { cn } from '@/lib/utils';

type Props = PageProps<'/[locale]/insights'>;

export const generateMetadata = ({ params }: Props) =>
  pageMetadata(params, 'insights', '/insights', (l) => getDictionary(l).sections.insights);

export default async function InsightsPage({ params, searchParams }: Props) {
  const locale = await resolveLocale(params);
  const query = await searchParams;
  const category = typeof query.category === 'string' ? query.category : undefined;
  const pageNumber = typeof query.page === 'string' ? query.page : undefined;
  const t = getDictionary(locale);
  const [page, insights] = await Promise.all([
    pageCopy(locale, 'insights', t.sections.insights),
    getInsights(locale, { category, page: pageNumber }),
  ]);

  const chip = (active: boolean) =>
    cn(
      'inline-flex min-h-11 items-center rounded-pill px-5 font-semibold ring-1 ring-inset transition-colors duration-fast',
      active ? 'bg-navy text-white ring-navy' : 'bg-surface ring-hairline hover:ring-blue hover:text-blue',
    );

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: '/insights' }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} gate={page} />
      <Section tight>
        <div className="container-wide">
          {insights.categories.length > 1 && (
            <ul className="mb-10 flex flex-wrap gap-2">
              <li>
                <SmartLink href="/insights" locale={locale} className={chip(!category)} aria-current={!category ? 'page' : undefined}>
                  {t.filters.all}
                </SmartLink>
              </li>
              {insights.categories.map((c) => (
                <li key={c.slug}>
                  <SmartLink
                    href={`/insights?category=${c.slug}`}
                    locale={locale}
                    className={chip(category === c.slug)}
                    aria-current={category === c.slug ? 'page' : undefined}
                  >
                    {c.name}
                  </SmartLink>
                </li>
              ))}
            </ul>
          )}
          {insights.results.length === 0 ? (
            <EmptyState>{t.empty.insights}</EmptyState>
          ) : (
            <ul className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {insights.results.map((insight, i) => (
                <Reveal as="li" key={insight.slug} index={i % 3}>
                  <InsightCard insight={insight} locale={locale} />
                </Reveal>
              ))}
            </ul>
          )}
          <Pagination locale={locale} basePath="/insights" query={query} hasPrevious={Boolean(insights.previous)} hasNext={Boolean(insights.next)} />
        </div>
      </Section>
      <CtaBand locale={locale} />
    </>
  );
}
