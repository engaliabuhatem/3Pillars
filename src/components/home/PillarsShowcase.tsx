'use client';

import { useEffect, useRef, useState } from 'react';
import { Icon } from '@/components/ui/Icon';
import { PendingMarker } from '@/components/ui/Tag';
import { useLocale } from '@/i18n/LocaleProvider';
import type { Pillar } from '@/lib/cms/types';
import { cn } from '@/lib/utils';

const ACCENT: Record<Pillar['color'], { bar: string; text: string }> = {
  green: { bar: 'bg-green', text: 'text-green' },
  blue: { bar: 'bg-blue', text: 'text-blue' },
  grey: { bar: 'bg-grey-300', text: 'text-grey' },
};

const EASE = 'ease-apple';

/**
 * The three pillars told the way Apple tells a product story. On wide screens
 * a dark stage stays put while the copy scrolls past it: the pillar being read
 * rises on the stage and its heading lights up, the others rest in grey. The
 * motion is scroll-led, slow to settle and never more than a rise and a fade.
 * On small screens, without JavaScript and under reduced motion every pillar
 * is fully shown as a plain card.
 */
export function PillarsShowcase({ pillars }: { pillars: Pillar[] }) {
  const locale = useLocale();
  const items = useRef<Array<HTMLLIElement | null>>([]);
  const [active, setActive] = useState<number | null>(null);

  useEffect(() => {
    const wide = window.matchMedia('(min-width: 1024px)');
    let observer: IntersectionObserver | undefined;

    const attach = () => {
      observer?.disconnect();
      if (!wide.matches) {
        setActive(null);
        return;
      }
      // A thin band across the middle of the viewport: whichever pillar crosses it is the one being read.
      observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) setActive(Number((entry.target as HTMLElement).dataset.index));
          }
        },
        { rootMargin: '-45% 0px -45% 0px' },
      );
      items.current.forEach((el) => el && observer!.observe(el));
    };

    attach();
    wide.addEventListener('change', attach);
    return () => {
      wide.removeEventListener('change', attach);
      observer?.disconnect();
    };
  }, [pillars.length]);

  const current = active ?? 0;

  return (
    <div className="grid gap-6 lg:grid-cols-12 lg:gap-16">
      {/* The stage: decorative, so assistive tech reads the list alone. */}
      <div aria-hidden className="hidden lg:col-span-6 lg:block">
        <div className="sticky top-28 flex h-[calc(100svh-9rem)] max-h-[44rem] items-center">
          <div className="relative flex size-full flex-col overflow-hidden rounded-card bg-navy p-10 text-white shadow-card">
            <div className="flex items-center justify-between">
              <div className="relative size-12">
                {pillars.map((pillar, i) => (
                  <span
                    key={pillar.id}
                    className={cn(
                      'absolute inset-0 transition-[opacity,transform] duration-cinematic',
                      EASE,
                      i === current ? 'scale-100 opacity-100' : 'scale-90 opacity-0',
                    )}
                  >
                    <Icon name={pillar.icon} className="size-12 text-white" />
                  </span>
                ))}
              </div>
              <p dir="ltr" className="text-caption font-semibold tabular-nums text-white/70">
                <span className="text-white">0{current + 1}</span> / 0{pillars.length}
              </p>
            </div>

            {/* The logo's three pillars, rising in turn. */}
            <div className="mt-auto flex h-3/5 items-end justify-center gap-5">
              {pillars.map((pillar, i) => (
                <span
                  key={pillar.id}
                  className={cn(
                    'w-1/5 max-w-24 origin-bottom rounded-t-pill rounded-b-lg transition-[transform,opacity] duration-cinematic',
                    EASE,
                    ACCENT[pillar.color].bar,
                    i <= current ? 'scale-y-100' : 'scale-y-[0.28]',
                    i === current ? 'opacity-100' : 'opacity-30',
                  )}
                  style={{ height: `${70 + i * 15}%`, transitionDelay: `${i * 60}ms` }}
                />
              ))}
            </div>
            <div className="mt-6 h-px bg-white/15" />
          </div>
        </div>
      </div>

      <ol className="grid gap-6 lg:col-span-6 lg:gap-0">
        {pillars.map((pillar, i) => {
          const accent = ACCENT[pillar.color];
          const resting = active !== null && active !== i;
          return (
            <li
              key={pillar.id}
              ref={(el) => {
                items.current[i] = el;
              }}
              data-index={i}
              className="flex flex-col max-lg:tile max-lg:p-8 md:max-lg:p-10 lg:min-h-[70svh] lg:justify-center"
            >
              <Icon name={pillar.icon} className={cn('mb-6 size-9 lg:hidden', accent.text)} />
              <p className="eyebrow flex items-center gap-2.5 tabular-nums text-ink-muted">
                <span aria-hidden className={cn('h-1 w-6 rounded-pill', accent.bar)} />
                0{i + 1}
              </p>
              <h3
                className={cn(
                  'mt-3 text-h3 font-semibold tracking-tight transition-colors duration-slow lg:text-h2',
                  EASE,
                  resting ? 'text-ink-muted' : 'text-ink',
                )}
              >
                {pillar.name}
              </h3>
              <p className="mt-4 max-w-xl text-lead text-ink-muted">{pillar.summary}</p>
              {pillar.detail && <p className="mt-4 max-w-xl text-ink-muted">{pillar.detail}</p>}
              <PendingMarker pending={pillar.pending} fallbacks={pillar.fallbacks} locale={locale} className="mt-6" />
            </li>
          );
        })}
      </ol>
    </div>
  );
}
