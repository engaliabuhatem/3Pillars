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
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';
import { cn } from '@/lib/utils';

type Props = PageProps<'/[locale]/insights'>;

const PATH = '/insights/';

export const generateMetadata = ({ params }: Props) =>
  pageMetadata(params, 'insights', PATH, (l) => getDictionary(l).sections.insights);

const one = (value: string | string[] | undefined) => (typeof value === 'string' ? value : undefined);

/** Kind and category filters are plain links, so every filtered view has its own shareable address. */
export default async function InsightsPage({ params, searchParams }: Props) {
  const locale = await resolveLocale(params);
  const query = await searchParams;
  const category = one(query.category);
  const kind = one(query.kind);
  const t = getDictionary(locale);
  const [page, insights] = await Promise.all([
    pageCopy(locale, 'insights', t.sections.insights),
    getInsights(locale, { category, kind, page: one(query.page) }),
  ]);

  const chip = (active: boolean) =>
    cn(
      'inline-flex min-h-11 items-center rounded-pill px-5 font-semibold ring-1 ring-inset transition-colors duration-fast',
      active ? 'bg-navy text-white ring-navy' : 'bg-surface ring-hairline hover:ring-blue hover:text-blue',
    );
  const href = (next: { kind?: string; category?: string }) => {
    const params = new URLSearchParams(Object.entries(next).filter((entry): entry is [string, string] => Boolean(entry[1])));
    return `${PATH}${params.size ? `?${params}` : ''}`;
  };

  return (
    <>
      <PageHeader background={page.heroImage} locale={locale} trail={[{ name: page.title, path: PATH }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} gate={page} />
      <Section tight>
        <div className="container-wide">
          <nav aria-label={t.filters.type} className="mb-4">
            <ul className="flex flex-wrap gap-2">
              <li>
                <SmartLink href={href({ category })} locale={locale} className={chip(!kind)} aria-current={!kind ? 'page' : undefined}>
                  {t.insights.allKinds}
                </SmartLink>
              </li>
              {insights.kinds.map((k) => (
                <li key={k.value}>
                  <SmartLink
                    href={href({ kind: k.value, category })}
                    locale={locale}
                    className={chip(kind === k.value)}
                    aria-current={kind === k.value ? 'page' : undefined}
                  >
                    {t.insights.kinds[k.value] ?? k.label}
                  </SmartLink>
                </li>
              ))}
            </ul>
          </nav>
          {insights.categories.length > 0 && (
            <nav aria-label={t.insights.category} className="mb-10">
              <ul className="flex flex-wrap gap-2">
                <li>
                  <SmartLink href={href({ kind })} locale={locale} className={chip(!category)} aria-current={!category ? 'page' : undefined}>
                    {t.filters.all}
                  </SmartLink>
                </li>
                {insights.categories.map((c) => (
                  <li key={c.slug}>
                    <SmartLink
                      href={href({ kind, category: c.slug })}
                      locale={locale}
                      className={chip(category === c.slug)}
                      aria-current={category === c.slug ? 'page' : undefined}
                    >
                      {c.name}
                    </SmartLink>
                  </li>
                ))}
              </ul>
            </nav>
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
          <Pagination locale={locale} basePath={PATH} query={query} hasPrevious={Boolean(insights.previous)} hasNext={Boolean(insights.next)} />
        </div>
      </Section>
      <CtaBand locale={locale} />
    </>
  );
}
