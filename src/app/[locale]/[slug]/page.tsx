import { notFound } from 'next/navigation';
import { Blocks } from '@/components/content/Blocks';
import { PageHeader } from '@/components/content/PageHeader';
import { getPage } from '@/lib/cms';
import { heading, resolveLocale } from '@/lib/page';
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
  if (!page || page.path !== `/${page.slug}/`) return {};
  return buildMetadata({ locale, path: page.path, title: page.title, description: page.intro, seo: page.seo, image: page.image });
}

export default async function CmsPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const page = await getPage(locale, (await params).slug);
  // Pages that live under another address (e.g. /about-us/leadership-team/) are only served there.
  if (!page || page.path !== `/${page.slug}/`) notFound();

  return (
    <>
      <PageHeader background={page.heroImage} locale={locale} trail={[{ name: page.title, path: page.path }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} image={page.image} gate={page} />
      <Blocks blocks={page.blocks} locale={locale} />
    </>
  );
}
