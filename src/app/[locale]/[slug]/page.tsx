import { notFound } from 'next/navigation';
import { Blocks } from '@/components/content/Blocks';
import { PageHeader } from '@/components/content/PageHeader';
import { getPage } from '@/lib/cms';
import { resolveLocale } from '@/lib/page';
import { buildMetadata } from '@/lib/seo';

/**
 * Any other CMS page by slug: privacy, terms, cookies, and whatever the team
 * adds later. Pages with their own route (about, approach…) never reach here,
 * because static segments win over this dynamic one.
 */
type Props = PageProps<'/[locale]/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const page = await getPage(locale, (await params).slug);
  if (!page) return {};
  return buildMetadata({ locale, path: `/${page.slug}`, title: page.title, description: page.intro, seo: page.seo, image: page.image });
}

export default async function CmsPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const page = await getPage(locale, (await params).slug);
  if (!page) notFound();

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: `/${page.slug}` }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} image={page.image} gate={page} />
      <Blocks blocks={page.blocks} locale={locale} />
    </>
  );
}
