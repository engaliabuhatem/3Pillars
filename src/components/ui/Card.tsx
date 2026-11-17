import type { ReactNode } from 'react';
import type { Locale } from '@/i18n/config';
import { cn } from '@/lib/utils';
import { SmartLink } from './SmartLink';

const BASE = 'relative flex flex-col overflow-hidden rounded-lg ring-1 ring-inset';

const TONES = {
  surface: 'bg-surface ring-hairline shadow-1 on-navy:bg-white/5 on-navy:ring-hairline-inverse on-navy:shadow-none',
  navy: 'bg-navy text-white ring-navy shadow-2',
} as const;

export type CardTone = keyof typeof TONES;

/*
 * Hover: lift 2px, step the shadow up, and draw the CI's thin blue card
 * stroke. Focus-within mirrors hover so keyboard users get the same signal.
 */
const INTERACTIVE =
  'transition-[transform,box-shadow] duration-base ease-out-expo ' +
  'hover:-translate-y-0.5 hover:shadow-2 hover:ring-blue focus-within:ring-2 focus-within:ring-blue ' +
  'on-navy:hover:ring-blue-300 on-navy:focus-within:ring-blue-200';

export function Card({
  children,
  className,
  interactive,
  tone = 'surface',
}: {
  children: ReactNode;
  className?: string;
  interactive?: boolean;
  tone?: CardTone;
}) {
  return (
    <div className={cn(BASE, TONES[tone], interactive && INTERACTIVE, className)} data-surface={tone === 'navy' ? 'navy' : undefined}>
      {children}
    </div>
  );
}

/**
 * A card whose whole surface is the link. The heading carries the link and a
 * pseudo-element stretches it, so screen readers hear one link, not a card
 * full of them.
 */
export function LinkCard({
  href,
  locale,
  title,
  titleClassName,
  children,
  className,
  headingLevel: H = 'h3',
  tone,
}: {
  href: string;
  locale: Locale;
  title: ReactNode;
  titleClassName?: string;
  children?: ReactNode;
  className?: string;
  headingLevel?: 'h2' | 'h3';
  tone?: CardTone;
}) {
  return (
    <Card interactive tone={tone} className={cn('group', className)}>
      {children}
      <H className={cn('order-first', titleClassName)}>
        <SmartLink href={href} locale={locale} className="after:absolute after:inset-0 after:content-[''] focus-visible:outline-none">
          {title}
        </SmartLink>
      </H>
    </Card>
  );
}
