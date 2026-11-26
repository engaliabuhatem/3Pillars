import { CONSULTATION_PATH } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { ConsultationWizard } from '@/components/forms/ConsultationWizard';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getSectors, getServices, getSettings } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

type Props = PageProps<'/[locale]/contact/request-a-consultation'>;

export const generateMetadata = ({ params }: Props) =>
  pageMetadata(params, 'request-a-consultation', CONSULTATION_PATH, (l) => getDictionary(l).common.requestConsultation);

export default async function RequestConsultationPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, contact, sectors, services, settings] = await Promise.all([
    pageCopy(locale, 'request-a-consultation', t.common.requestConsultation),
    pageCopy(locale, 'contact', t.sections.contact),
    getSectors(locale),
    getServices(locale),
    getSettings(locale),
  ]);

  return (
    <>
      <PageHeader
        locale={locale}
        trail={[
          { name: contact.title, path: '/contact/' },
          { name: page.title, path: CONSULTATION_PATH },
        ]}
        eyebrow={page.eyebrow}
        title={heading(page)}
        intro={page.intro}
        gate={page}
      />
      <Section tone="surface" tight>
        <div className="container-content max-w-4xl">
          <ConsultationWizard
            sectors={sectors.map(({ slug, name }) => ({ slug, name }))}
            services={services.map(({ slug, name }) => ({ slug, name }))}
            turnstileKey={settings.turnstileEnabled ? settings.turnstileSiteKey : undefined}
            consentText={settings.consentText}
          />
        </div>
      </Section>
    </>
  );
}
