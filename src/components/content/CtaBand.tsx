import { ButtonLink } from '@/components/ui/Button';
import { Eyebrow } from '@/components/ui/Heading';
import { Section } from '@/components/ui/Section';
import { LineReveal } from '@/components/motion/LineReveal';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';

interface CtaBandProps {
  locale: Locale;
  eyebrow?: string;
  title?: string;
  intro?: string;
  primary?: { label: string; href: string };
  secondary?: { label: string; href: string };
}

/**
 * The business-development close every page ends on: navy, three arcs, one
 * primary action. Falls back to the standard pair of actions when the CMS
 * gives none.
 */
export function CtaBand({ locale, eyebrow, title, intro, primary, secondary }: CtaBandProps) {
  const t = getDictionary(locale).common;
  const main = primary?.label ? primary : { label: t.requestProposal, href: '/request-a-proposal' };
  const alt = secondary?.label ? secondary : { label: t.capability, href: '/capability-statement' };

  return (
    <Section tone="navy" arcs labelledBy="cta-title">
      <div className="container-content">
        <div className="max-w-3xl">
          {eyebrow && <Eyebrow className="mb-5">{eyebrow}</Eyebrow>}
          <h2 id="cta-title" className="text-h1 font-semibold text-balance">
            <LineReveal text={title || t.requestProposal} />
          </h2>
          {intro && <p className="mt-6 max-w-2xl text-lead text-ink-inverse-muted">{intro}</p>}
          <div className="mt-10 flex flex-wrap gap-3">
            <ButtonLink href={main.href} locale={locale} variant="inverse" size="lg" arrow track="cta_band_primary">
              {main.label}
            </ButtonLink>
            <ButtonLink href={alt.href} locale={locale} variant="inverse-outline" size="lg" track="cta_band_secondary">
              {alt.label}
            </ButtonLink>
          </div>
        </div>
      </div>
    </Section>
  );
}
