import type { ReactNode } from 'react';
import type { Locale } from '@/i18n/config';
import { getDictionary } from '@/i18n/dictionaries';
import { cn } from '@/lib/utils';

type Tone = 'neutral' | 'blue' | 'green' | 'warning';

const TONES: Record<Tone, string> = {
  neutral: 'bg-grey-100 text-navy on-navy:bg-white/10 on-navy:text-white',
  blue: 'bg-blue-50 text-blue-700 on-navy:bg-white/10 on-navy:text-blue-200',
  green: 'bg-green-50 text-green-700 on-navy:bg-white/10 on-navy:text-green-200',
  warning: 'bg-warning-50 text-warning',
};

export function Tag({ children, tone = 'neutral', className }: { children: ReactNode; tone?: Tone; className?: string }) {
  return (
    <span
      className={cn('inline-flex items-center gap-1.5 rounded-pill px-3 py-1 text-caption font-semibold', TONES[tone], className)}
    >
      {children}
    </span>
  );
}

/**
 * Staging-only marker for content awaiting approval, plus a note when Arabic
 * fell back to English. The API only sends pending rows when the gate is open,
 * so on the live site this never renders.
 */
export function PendingMarker({
  pending,
  fallbacks,
  locale,
  className,
}: {
  pending?: boolean;
  fallbacks?: string[];
  locale: Locale;
  className?: string;
}) {
  const t = getDictionary(locale).a11y;
  const showFallback = locale === 'ar' && Boolean(fallbacks?.length);
  if (!pending && !showFallback) return null;
  return (
    <span className={cn('inline-flex flex-wrap gap-2', className)}>
      {pending && <Tag tone="warning">{t.pending}</Tag>}
      {showFallback && <Tag tone="warning">{t.fallback}</Tag>}
    </span>
  );
}
