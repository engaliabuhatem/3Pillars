import { Blocks } from '@/components/content/Blocks';
import { ServiceCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { EmptyState } from '@/components/ui/Feedback';
import { Section } from '@/components/ui/Section';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getServices } from '@/lib/cms';
import { pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

export const generateMetadata = ({ params }: PageProps<'/[locale]/services'>) =>
  pageMetadata(params, 'services', '/services', (l) => getDictionary(l).sections.services);

export default async function ServicesPage({ params }: PageProps<'/[locale]/services'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, services] = await Promise.all([pageCopy(locale, 'services', t.sections.services), getServices(locale)]);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: '/services' }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} gate={page} />
      <Section tight>
        <div className="container-wide">
          {services.length === 0 ? (
            <EmptyState>{t.empty.generic}</EmptyState>
          ) : (
            <ul className="grid auto-rows-fr gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {services.map((service, i) => (
                <Reveal as="li" key={service.slug} index={i % 3}>
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
