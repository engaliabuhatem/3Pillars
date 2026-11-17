import { notFound } from 'next/navigation';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { ShareLinks } from '@/components/content/ShareLinks';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getInsight } from '@/lib/cms';
import { resolveLocale } from '@/lib/page';
import { articleJsonLd, buildMetadata, JsonLd, siteUrl } from '@/lib/seo';
import { formatDate } from '@/lib/utils';

type Props = PageProps<'/[locale]/insights/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const insight = await getInsight(locale, (await params).slug);
  if (!insight) return {};
  return buildMetadata({
    locale,
    path: `/insights/${insight.slug}`,
    title: insight.title,
    description: insight.excerpt,
    seo: insight.seo,
    image: insight.image,
    type: 'article',
  });
}

export default async function InsightPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const insight = await getInsight(locale, (await params).slug);
  if (!insight) notFound();
  const t = getDictionary(locale);
  const url = `${siteUrl()}/${locale}/insights/${insight.slug}`;

  return (
    <>
      <PageHeader
        locale={locale}
        trail={[
          { name: t.sections.insights, path: '/insights' },
          { name: insight.title, path: `/insights/${insight.slug}` },
        ]}
        eyebrow={insight.category?.name}
        title={insight.title}
        intro={insight.excerpt}
        image={insight.image}
        gate={insight}
      >
        <p className="flex flex-wrap gap-x-4 text-caption text-ink-muted">
          {insight.author && <span className="font-semibold text-navy">{insight.author}</span>}
          <time dateTime={insight.publishedAt}>{formatDate(insight.publishedAt, locale)}</time>
          <span>{t.common.minRead(insight.readingMinutes)}</span>
        </p>
      </PageHeader>
      <Section tone="surface" tight>
        <article className="container-content">
          <RichText html={insight.body} className="mx-auto text-lead" />
          <div className="mx-auto mt-14 max-w-prose border-t border-hairline pt-8">
            <ShareLinks url={url} title={insight.title} />
          </div>
        </article>
      </Section>
      <CtaBand locale={locale} />
      <JsonLd data={articleJsonLd(insight, url)} />
    </>
  );
}
