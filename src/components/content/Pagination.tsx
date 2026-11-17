import { ChevronLeft, ChevronRight } from 'lucide-react';
import { buttonClass } from '@/components/ui/Button';
import { SmartLink } from '@/components/ui/SmartLink';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';

type Query = Record<string, string | string[] | undefined>;

function withPage(basePath: string, query: Query, page: number) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query)) {
    if (key !== 'page' && typeof value === 'string' && value) params.set(key, value);
  }
  if (page > 1) params.set('page', String(page));
  return `${basePath}${params.size ? `?${params}` : ''}`;
}

export function Pagination({
  locale,
  basePath,
  query,
  hasPrevious,
  hasNext,
}: {
  locale: Locale;
  basePath: string;
  query: Query;
  hasPrevious: boolean;
  hasNext: boolean;
}) {
  if (!hasPrevious && !hasNext) return null;
  const t = getDictionary(locale).a11y;
  const current = Number(typeof query.page === 'string' ? query.page : 1) || 1;
  return (
    <nav aria-label={t.pagination} className="mt-12 flex justify-between gap-4">
      {hasPrevious ? (
        <SmartLink href={withPage(basePath, query, current - 1)} locale={locale} className={buttonClass('secondary')} rel="prev">
          <ChevronLeft aria-hidden className="size-4 rtl:-scale-x-100" />
          {t.previous}
        </SmartLink>
      ) : (
        <span />
      )}
      {hasNext && (
        <SmartLink href={withPage(basePath, query, current + 1)} locale={locale} className={buttonClass('secondary')} rel="next">
          {t.next}
          <ChevronRight aria-hidden className="size-4 rtl:-scale-x-100" />
        </SmartLink>
      )}
    </nav>
  );
}
