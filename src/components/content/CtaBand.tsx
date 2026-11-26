import { ButtonLink } from '@/components/ui/Button';
import { Eyebrow } from '@/components/ui/Heading';
import { Section } from '@/components/ui/Section';
import { LineReveal } from '@/components/motion/LineReveal';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';

export const CONSULTATION_PATH = '/contact/request-a-consultation/';

interface CtaBandProps {
  locale: Locale;
  eyebrow?: string;
  title?: string;
  intro?: string;
  primary?: { label: string; href: string };
  secondary?: { label: string; href: string };
}

/**
 * The close every page ends on: navy, three arcs, one primary action. A page's
 * own headline and button come from the CMS; without them it offers a
 * consultation. A second action appears only when the CMS gives one.
 */
export function CtaBand({ locale, eyebrow, title, intro, primary, secondary }: CtaBandProps) {
  const t = getDictionary(locale).common;
  const main = primary?.label ? primary : { label: t.requestConsultation, href: CONSULTATION_PATH };

  return (
    <Section tone="navy" arcs labelledBy="cta-title">
      <div className="container-content">
        <div className="max-w-3xl">
          {eyebrow && <Eyebrow className="mb-5">{eyebrow}</Eyebrow>}
          <h2 id="cta-title" className="text-h1 font-semibold text-balance">
            <LineReveal text={title || t.requestConsultation} />
          </h2>
          {intro && <p className="mt-6 max-w-2xl text-lead text-ink-inverse-muted">{intro}</p>}
          <div className="mt-10 flex flex-wrap gap-3">
            <ButtonLink href={main.href || CONSULTATION_PATH} locale={locale} variant="inverse" size="lg" arrow track="cta_band_primary">
              {main.label}
            </ButtonLink>
            {secondary?.label && secondary.href && (
              <ButtonLink href={secondary.href} locale={locale} variant="inverse-outline" size="lg" track="cta_band_secondary">
                {secondary.label}
              </ButtonLink>
            )}
          </div>
        </div>
      </div>
    </Section>
  );
}
