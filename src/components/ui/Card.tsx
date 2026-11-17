import { ChevronRight } from 'lucide-react';
import type { ReactNode } from 'react';
import type { Locale } from '@/i18n/config';
import { cn } from '@/lib/utils';
import { SmartLink } from './SmartLink';

/*
 * Apple-style cards: large radius, no outline, a soft shadow (or a flat grey
 * tile on white sections, via the `tile` utility). On hover the card grows a
 * touch, the shadow deepens and the image inside zooms slowly; nothing jumps.
 */
const TONES = {
  surface: 'tile',
  navy: 'rounded-card bg-navy text-white shadow-card',
} as const;

export type CardTone = keyof typeof TONES;

const INTERACTIVE =
  'transition-[transform,box-shadow] duration-slow ease-out-expo hover:scale-[1.015] hover:shadow-card-hover ' +
  'motion-reduce:hover:scale-100 has-focus-visible:outline-2 has-focus-visible:outline-offset-4 has-focus-visible:outline-focus';

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
    <div
      className={cn('relative flex flex-col overflow-hidden', TONES[tone], interactive && INTERACTIVE, className)}
      data-surface={tone === 'navy' ? 'navy' : undefined}
    >
      {children}
    </div>
  );
}

/** The quiet label above a card title ("Energy · Ongoing", "Article"). */
export function CardEyebrow({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <p className={cn('mb-2 text-caption font-semibold text-ink-muted on-navy:text-ink-inverse-muted', className)}>{children}</p>
  );
}

/** Apple's "Learn more ›": a visual hint, not a second link (the whole card is the link). */
export function CardMore({ children, pushDown = true }: { children: ReactNode; pushDown?: boolean }) {
  return (
    <span
      aria-hidden
      className={cn('inline-flex items-center gap-0.5 font-semibold text-blue on-navy:text-blue-200', pushDown ? 'mt-auto pt-6' : 'pt-4')}
    >
      {children}
      <ChevronRight className="size-4 transition-transform duration-base ease-out-expo group-hover:translate-x-0.5 rtl:-scale-x-100 rtl:group-hover:-translate-x-0.5" />
    </span>
  );
}

/**
 * A card whose whole surface is one link. The title carries the link and a
 * pseudo-element stretches it over the card, so a screen reader hears one
 * link with a sensible name instead of a card full of them.
 */
export function LinkCard({
  href,
  locale,
  title,
  eyebrow,
  media,
  children,
  className,
  bodyClassName,
  titleClassName,
  titleSize = 'text-[1.375rem]',
  headingLevel: H = 'h3',
  tone,
}: {
  href: string;
  locale: Locale;
  title: ReactNode;
  eyebrow?: ReactNode;
  /** Full-bleed media at the top of the card (or behind it, when positioned absolutely). */
  media?: ReactNode;
  children?: ReactNode;
  className?: string;
  bodyClassName?: string;
  titleClassName?: string;
  /** Font-size class for the title; separate so it never fights a default. */
  titleSize?: string;
  headingLevel?: 'h2' | 'h3';
  tone?: CardTone;
}) {
  return (
    <Card interactive tone={tone} className={cn('group h-full', className)}>
      {media}
      <div className={cn('flex flex-1 flex-col p-7 md:p-8', bodyClassName)}>
        {eyebrow && <CardEyebrow>{eyebrow}</CardEyebrow>}
        <H className={cn(titleSize, 'leading-tight font-semibold tracking-tight text-balance', titleClassName)}>
          <SmartLink href={href} locale={locale} className="after:absolute after:inset-0 after:z-10 after:content-[''] focus-visible:outline-none">
            {title}
          </SmartLink>
        </H>
        {children}
      </div>
    </Card>
  );
}
