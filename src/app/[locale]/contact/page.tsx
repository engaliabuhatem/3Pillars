import { Mail, Phone } from 'lucide-react';
import { Blocks } from '@/components/content/Blocks';
import { CONSULTATION_PATH } from '@/components/content/CtaBand';
import { OfficeCard } from '@/components/content/OfficeCard';
import { PageHeader } from '@/components/content/PageHeader';
import { ContactForm } from '@/components/forms/ContactForm';
import { ButtonLink } from '@/components/ui/Button';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getOffices, getSettings } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

type Props = PageProps<'/[locale]/contact'>;

const PATH = '/contact/';

export const generateMetadata = ({ params }: Props) => pageMetadata(params, 'contact', PATH, (l) => getDictionary(l).sections.contact);

/**
 * Intro, the enquiry form and, beside it, only the contact details Site
 * settings marks as verified (the API sends them empty until then).
 */
export default async function ContactPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, offices, settings] = await Promise.all([pageCopy(locale, 'contact', t.sections.contact), getOffices(locale), getSettings(locale)]);
  const details = [settings.phone, settings.email, settings.address, settings.businessHours].some(Boolean);

  return (
    <>
      <PageHeader background={page.heroImage} locale={locale} trail={[{ name: page.title, path: PATH }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} gate={page} />
      <Section tone="surface" tight>
        <div className="container-wide grid gap-14 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] lg:gap-20">
          <ContactForm
            turnstileKey={settings.turnstileEnabled ? settings.turnstileSiteKey : undefined}
            consentText={settings.consentText}
            submitLabel={page.ctaLabel}
          />
          <div className="grid content-start gap-5">
            {details && (
              <div className="tile grid gap-3 p-7 md:p-8">
                {settings.address && <p className="whitespace-pre-line">{settings.address}</p>}
                {settings.phone && (
                  <a href={`tel:${settings.phone.replace(/\s/g, '')}`} dir="ltr" className="inline-flex min-h-11 items-center gap-3 hover:text-blue">
                    <Phone aria-hidden className="size-4 text-green" />
                    {settings.phone}
                  </a>
                )}
                {settings.email && (
                  <a href={`mailto:${settings.email}`} className="inline-flex min-h-11 items-center gap-3 hover:text-blue">
                    <Mail aria-hidden className="size-4 text-green" />
                    {settings.email}
                  </a>
                )}
                {settings.businessHours && <p className="text-ink-muted">{settings.businessHours}</p>}
              </div>
            )}
            {offices.map((office) => (
              <OfficeCard key={office.id} office={office} locale={locale} />
            ))}
            <ButtonLink href={CONSULTATION_PATH} locale={locale} variant="secondary" arrow track="contact_to_consultation">
              {t.forms.consultationLink}
            </ButtonLink>
          </div>
        </div>
      </Section>
      <Blocks blocks={page.blocks} locale={locale} />
    </>
  );
}
