import { Mail, MapPin, Phone } from 'lucide-react';
import { LinkedInIcon } from '@/components/brand/LinkedInIcon';
import { Logo } from '@/components/brand/Logo';
import { ThreeArcs } from '@/components/brand/ThreeArcs';
import { SmartLink } from '@/components/ui/SmartLink';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import type { Navigation, Office, SiteSettings } from '@/lib/cms/types';

const DEVELOPER_LINKEDIN = 'https://www.linkedin.com/in/ali-abuhatem';

const SOCIAL_LABEL: Record<SiteSettings['socials'][number]['network'], string> = {
  linkedin: 'LinkedIn',
  x_twitter: 'X',
  facebook: 'Facebook',
  instagram: 'Instagram',
  youtube: 'YouTube',
};

export function Footer({
  navigation,
  settings,
  offices,
  locale,
}: {
  navigation: Navigation;
  settings: SiteSettings;
  offices: Office[];
  locale: Locale;
}) {
  const t = getDictionary(locale);
  const year = new Date().getFullYear();
  // The CMS footer columns, then every published service and sector page.
  const columns = [
    ...navigation.footer.map((column) => ({
      title: column.title,
      links: column.items.map((item) => ({ label: item.label, href: item.link })),
    })),
    { title: t.sections.services, links: navigation.mega.services.map((s) => ({ label: s.name, href: `/services/${s.slug}/` })) },
    { title: t.sections.sectors, links: navigation.mega.sectors.map((s) => ({ label: s.name, href: `/sectors/${s.slug}/` })) },
  ].filter((column) => column.links.length > 0);
  // Contact details arrive empty until Site settings marks them verified.
  const hasContact = offices.length > 0 || Boolean(settings.phone || settings.email || settings.businessHours) || settings.socials.length > 0;

  return (
    <footer data-surface="navy" className="relative isolate overflow-hidden bg-navy text-ink-inverse">
      {/* The arcs sit in the far corner, clear of the text. */}
      <ThreeArcs className="pointer-events-none absolute -end-10 -bottom-10 -z-10 h-80 w-[36rem] opacity-40 rtl:-scale-x-100" />
      <div className="container-wide grid gap-14 py-16 md:py-20 lg:grid-cols-12 lg:gap-10">
        <div className="lg:col-span-4">
          <Logo variant="full" tone="white" className="h-28 w-auto" />
          {settings.tagline && <p className="mt-6 max-w-sm text-[0.9375rem] leading-relaxed text-ink-inverse-muted">{settings.tagline}</p>}
          {settings.groupRelationship && <p className="mt-3 max-w-sm text-caption text-grey-300">{settings.groupRelationship}</p>}

          {hasContact && (
            <div className="mt-8">
              <h2 className="sr-only">{t.sections.contact}</h2>
              <ul className="flex flex-col gap-2 text-[0.9375rem] text-ink-inverse-muted">
                {offices.map((office) => (
                  <li key={office.id} className="flex gap-3">
                    <MapPin aria-hidden className="mt-1 size-4 shrink-0 text-green-200" />
                    <span>
                      <span className="block font-semibold text-white">
                        {office.city}, {office.country}
                      </span>
                      {office.address}
                    </span>
                  </li>
                ))}
                {settings.phone && (
                  <li>
                    <a href={`tel:${settings.phone.replace(/s/g, '')}`} className="inline-flex min-h-11 items-center gap-3 hover:text-white" dir="ltr">
                      <Phone aria-hidden className="size-4 text-green-200" />
                      {settings.phone}
                    </a>
                  </li>
                )}
                {settings.email && (
                  <li>
                    <a href={`mailto:${settings.email}`} className="inline-flex min-h-11 items-center gap-3 hover:text-white">
                      <Mail aria-hidden className="size-4 text-green-200" />
                      {settings.email}
                    </a>
                  </li>
                )}
                {settings.businessHours && <li>{settings.businessHours}</li>}
              </ul>
              {settings.socials.length > 0 && (
                <ul className="mt-4 flex flex-wrap gap-2">
                  {settings.socials.map((social) => (
                    <li key={social.network}>
                      <a
                        href={social.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex min-h-11 items-center rounded-pill px-4 ring-1 ring-hairline-inverse ring-inset hover:bg-white/10"
                      >
                        {SOCIAL_LABEL[social.network]}
                        <span className="sr-only"> ({t.a11y.external})</span>
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>

        <nav aria-label={t.a11y.footerNav} className="grid grid-cols-2 gap-x-8 gap-y-10 sm:grid-cols-4 lg:col-span-8">
          {columns.map((column) => (
            <div key={column.title}>
              <h2 className="eyebrow mb-4 text-blue-200">{column.title}</h2>
              <ul className="flex flex-col">
                {column.links.map((link) => (
                  <li key={link.href}>
                    <SmartLink
                      href={link.href}
                      locale={locale}
                      className="inline-flex min-h-11 items-center py-1 text-[0.9375rem] leading-snug text-white/90 hover:text-blue-200"
                    >
                      {link.label}
                    </SmartLink>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </div>

      <div className="border-t border-hairline-inverse">
        <div className="container-wide flex flex-col gap-4 py-6 text-caption text-grey-300 md:flex-row md:items-center md:justify-between">
          <div className="flex flex-col gap-1 md:flex-row md:items-center md:gap-3">
            <p>
              © {year} {settings.companyName}
            </p>
            <span aria-hidden className="hidden md:inline">·</span>
            <p className="flex items-center gap-1.5">
              {t.credit.developedBy}
              <a
                href={DEVELOPER_LINKEDIN}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex min-h-11 items-center gap-1.5 font-semibold text-blue-200 hover:text-white"
              >
                <LinkedInIcon className="size-4" />
                {t.credit.developer}
                <span className="sr-only"> (LinkedIn, {t.a11y.external})</span>
              </a>
            </p>
          </div>
          <ul className="flex flex-wrap gap-x-6">
            {navigation.legal.map((item) => (
              <li key={item.link}>
                <SmartLink href={item.link} locale={locale} className="inline-flex min-h-11 items-center hover:text-white">
                  {item.label}
                </SmartLink>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </footer>
  );
}
