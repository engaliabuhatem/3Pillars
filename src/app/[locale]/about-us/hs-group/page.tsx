import { Blocks } from '@/components/content/Blocks';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getSettings } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

const PATH = '/about-us/hs-group/';
type Props = PageProps<'/[locale]/about-us/hs-group'>;

export const generateMetadata = ({ params }: Props) => pageMetadata(params, 'hs-group', PATH, (l) => getDictionary(l).sections.group);

/**
 * The approved statement of how 3 Pillars relates to HS Group, and nothing
 * more: no group projects, figures, offices or history. Its menu item stays
 * hidden until the wording is approved.
 */
export default async function GroupRelationshipPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, about, settings] = await Promise.all([
    pageCopy(locale, 'hs-group', t.sections.group),
    pageCopy(locale, 'about-us', t.sections.about),
    getSettings(locale),
  ]);

  return (
    <>
      <PageHeader
        locale={locale}
        trail={[
          { name: about.title, path: '/about-us/' },
          { name: page.title, path: PATH },
        ]}
        eyebrow={page.eyebrow}
        title={heading(page)}
        intro={page.intro}
        gate={page}
      />
      {settings.groupRelationship && (
        <Section tone="surface" tight>
          <div className="container-wide max-w-4xl">
            <p className="text-h3 font-medium text-balance">{settings.groupRelationship}</p>
          </div>
        </Section>
      )}
      <Blocks blocks={page.blocks} locale={locale} />
      <CtaBand locale={locale} />
    </>
  );
}
