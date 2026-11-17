import { locale as rootLocale } from 'next/root-params';
import { StatusScreen } from '@/components/content/StatusScreen';
import { ButtonLink } from '@/components/ui/Button';
import { DEFAULT_LOCALE, isLocale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';

export default async function NotFound() {
  const value = await rootLocale();
  const locale = isLocale(value) ? value : DEFAULT_LOCALE;
  const t = getDictionary(locale);
  return (
    <StatusScreen code="404" title={t.notFound.title} body={t.notFound.body}>
      <ButtonLink href="/" locale={locale} variant="inverse" size="lg" arrow>
        {t.notFound.cta}
      </ButtonLink>
      <ButtonLink href="/contact" locale={locale} variant="inverse-outline" size="lg">
        {t.sections.contact}
      </ButtonLink>
    </StatusScreen>
  );
}
