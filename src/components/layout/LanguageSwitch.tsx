'use client';

import Link from 'next/link';
import { usePathname, useSearchParams } from 'next/navigation';
import { otherLocale } from '@/i18n/config';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import { cn } from '@/lib/utils';

/**
 * Swaps the locale segment and keeps the rest of the URL: slugs are shared
 * between languages, so /en/services/x and /ar/services/x are the same page.
 */
export function LanguageSwitch({ className }: { className?: string }) {
  const locale = useLocale();
  const t = useDictionary().common;
  const pathname = usePathname();
  const search = useSearchParams().toString();
  const target = otherLocale(locale);
  const href = `${pathname.replace(/^\/(en|ar)(?=\/|$)/, `/${target}`)}${search ? `?${search}` : ''}`;

  return (
    <Link
      href={href}
      hrefLang={target}
      lang={target}
      title={t.languageLabel}
      onClick={() => {
        document.cookie = `locale=${target}; path=/; max-age=31536000; samesite=lax`;
      }}
      className={cn(
        'inline-grid min-h-11 min-w-11 place-items-center rounded-pill px-3 text-[0.9375rem] font-semibold transition-colors duration-fast',
        className,
      )}
    >
      {t.languageShort}
      <span className="sr-only"> {t.language}</span>
    </Link>
  );
}
