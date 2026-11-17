import { ExternalLink } from 'lucide-react';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';

export function Linkedin({ href, name, locale }: { href: string; name: string; locale: Locale }) {
  const t = getDictionary(locale).a11y;
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="mt-3 inline-flex min-h-11 items-center gap-1.5 font-semibold text-blue hover:underline"
    >
      LinkedIn
      <ExternalLink aria-hidden className="size-3.5" />
      <span className="sr-only">
        {' '}
        — {name} ({t.external})
      </span>
    </a>
  );
}
