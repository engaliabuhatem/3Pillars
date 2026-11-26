import { Blocks } from '@/components/content/Blocks';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { SectionHeading } from '@/components/ui/Heading';
import { Section } from '@/components/ui/Section';
import { PendingMarker } from '@/components/ui/Tag';
import { getDictionary } from '@/i18n/dictionaries';
import { getCertifications } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

const PATH = '/about-us/';

export const generateMetadata = ({ params }: PageProps<'/[locale]/about-us'>) =>
  pageMetadata(params, 'about-us', PATH, (l) => getDictionary(l).sections.about);

/** Who We Are → Vision → Mission → Values → Our Approach → (affiliation, once approved): all CMS blocks. */
export default async function AboutPage({ params }: PageProps<'/[locale]/about-us'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, certifications] = await Promise.all([pageCopy(locale, 'about-us', t.sections.about), getCertifications(locale)]);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: PATH }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} image={page.image} gate={page} />
      <Blocks blocks={page.blocks} locale={locale} />

      {certifications.length > 0 && (
        <Section tight>
          <div className="container-wide">
            <SectionHeading title={t.sections.certifications} />
            <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {certifications.map((cert) => (
                <li key={cert.id} className="tile p-7 md:p-8">
                  <p className="text-lg font-semibold">{cert.name}</p>
                  <p className="text-ink-muted">
                    {cert.issuer}
                    {cert.year ? ` · ${cert.year}` : ''}
                  </p>
                  <PendingMarker pending={cert.pending} locale={locale} className="mt-3" />
                </li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      <CtaBand locale={locale} />
    </>
  );
}
