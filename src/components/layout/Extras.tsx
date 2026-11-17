'use client';

import { MessageCircle } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { setConsent, useConsent } from '@/hooks/useConsent';
import { useDictionary } from '@/i18n/LocaleProvider';

export function WhatsAppButton({ number }: { number: string }) {
  const t = useDictionary().a11y;
  return (
    <a
      href={`https://wa.me/${number.replace(/\D/g, '')}`}
      target="_blank"
      rel="noopener noreferrer"
      data-track="whatsapp_click"
      aria-label={t.whatsapp}
      className="fixed end-5 bottom-5 z-30 grid size-14 place-items-center rounded-pill bg-green text-white shadow-3 transition-transform duration-base ease-out-expo hover:-translate-y-0.5"
    >
      <MessageCircle aria-hidden className="size-6" />
    </a>
  );
}

/** Analytics load only after "Accept"; the choice is remembered on this device. */
export function CookieNotice({ text }: { text: string }) {
  const t = useDictionary().cookie;
  const consent = useConsent();

  if (consent !== null || !text) return null;

  return (
    <section
      aria-label={t.title}
      className="fixed inset-x-4 bottom-4 z-40 mx-auto flex max-w-2xl flex-col gap-4 rounded-lg bg-surface p-5 text-[0.9375rem] shadow-3 ring-1 ring-hairline ring-inset sm:flex-row sm:items-center"
    >
      <p className="flex-1 text-ink-muted">{text}</p>
      <div className="flex gap-2">
        <Button variant="secondary" onClick={() => setConsent('essential')}>
          {t.decline}
        </Button>
        <Button onClick={() => setConsent('all')}>{t.accept}</Button>
      </div>
    </section>
  );
}
