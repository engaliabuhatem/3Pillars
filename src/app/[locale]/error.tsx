'use client';

import { useEffect } from 'react';
import { StatusScreen } from '@/components/content/StatusScreen';
import { Button, ButtonLink } from '@/components/ui/Button';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';

export default function ErrorPage({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  const locale = useLocale();
  const t = useDictionary();

  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <StatusScreen code="500" title={t.error.title} body={t.error.body}>
      <Button variant="inverse" size="lg" onClick={reset}>
        {t.error.retry}
      </Button>
      <ButtonLink href="/contact" locale={locale} variant="inverse-outline" size="lg">
        {t.sections.contact}
      </ButtonLink>
    </StatusScreen>
  );
}
