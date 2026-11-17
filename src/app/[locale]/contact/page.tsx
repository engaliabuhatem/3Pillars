import { Blocks } from '@/components/content/Blocks';
import { OfficeCard } from '@/components/content/OfficeCard';
import { PageHeader } from '@/components/content/PageHeader';
import { ContactForm } from '@/components/forms/ContactForm';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getOffices, getSettings } from '@/lib/cms';
import { pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

type Props = PageProps<'/[locale]/contact'>;

export const generateMetadata = ({ params }: Props) => pageMetadata(params, 'contact', '/contact', (l) => getDictionary(l).sections.contact);

export default async function ContactPage({ params, searchParams }: Props) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const topic = (await searchParams).topic;
  const [page, offices, settings] = await Promise.all([pageCopy(locale, 'contact', t.sections.contact), getOffices(locale), getSettings(locale)]);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: '/contact' }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} gate={page} />
      <Section tone="surface" tight>
        <div className="container-wide grid gap-14 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] lg:gap-20">
          <ContactForm turnstileKey={settings.turnstileEnabled ? settings.turnstileSiteKey : undefined} initialTopic={typeof topic === 'string' ? topic : undefined} />
          <div className="grid content-start gap-5">
            {offices.map((office) => (
              <OfficeCard key={office.id} office={office} locale={locale} />
            ))}
          </div>
        </div>
      </Section>
      <Blocks blocks={page.blocks} locale={locale} />
    </>
  );
}
