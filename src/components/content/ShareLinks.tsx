'use client';

import { Link2 } from 'lucide-react';
import { useToast } from '@/components/ui/Toast';
import { useDictionary } from '@/i18n/LocaleProvider';

const BUTTON =
  'inline-flex min-h-11 items-center gap-2 rounded-pill px-4 text-[0.9375rem] font-semibold ring-1 ring-hairline-strong ring-inset hover:ring-blue hover:text-blue';

export function ShareLinks({ url, title }: { url: string; title: string }) {
  const t = useDictionary();
  const toast = useToast();
  const encoded = encodeURIComponent(url);

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="me-2 text-caption font-semibold text-ink-muted">{t.common.share}</span>
      <a className={BUTTON} target="_blank" rel="noopener noreferrer" href={`https://www.linkedin.com/sharing/share-offsite/?url=${encoded}`}>
        LinkedIn<span className="sr-only"> ({t.a11y.external})</span>
      </a>
      <a className={BUTTON} target="_blank" rel="noopener noreferrer" href={`https://wa.me/?text=${encodeURIComponent(`${title} ${url}`)}`}>
        WhatsApp<span className="sr-only"> ({t.a11y.external})</span>
      </a>
      <button
        type="button"
        className={BUTTON}
        onClick={() => navigator.clipboard.writeText(url).then(() => toast(t.common.copied))}
      >
        <Link2 aria-hidden className="size-4" />
        {t.common.copyLink}
      </button>
    </div>
  );
}
