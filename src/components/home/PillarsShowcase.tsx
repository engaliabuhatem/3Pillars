'use client';

import { useRef, useState } from 'react';
import { Icon } from '@/components/ui/Icon';
import { PendingMarker } from '@/components/ui/Tag';
import { useScrollTrigger } from '@/hooks/useScrollTrigger';
import { useLocale } from '@/i18n/LocaleProvider';
import type { Pillar } from '@/lib/cms/types';
import { cn } from '@/lib/utils';

const ACCENT: Record<Pillar['color'], { bar: string; text: string }> = {
  green: { bar: 'bg-green', text: 'text-green' },
  blue: { bar: 'bg-blue', text: 'text-blue' },
  grey: { bar: 'bg-grey', text: 'text-grey' },
};

/**
 * The three pillars, each tinted with its pillar colour. On wide screens the
 * section pins and each pillar takes the stage in turn as you scroll; on small
 * screens and under reduced motion it is a plain three-column layout with
 * every pillar fully visible.
 */
export function PillarsShowcase({ pillars }: { pillars: Pillar[] }) {
  const locale = useLocale();
  const root = useRef<HTMLDivElement>(null);
  const [active, setActive] = useState<number | null>(null);

  useScrollTrigger(root, (_gsap, ScrollTrigger) => {
    const trigger = ScrollTrigger.create({
      trigger: root.current,
      start: 'top top',
      end: `+=${pillars.length * 70}%`,
      pin: true,
      onUpdate: (self) => setActive(Math.min(pillars.length - 1, Math.floor(self.progress * pillars.length))),
      onLeaveBack: () => setActive(null),
    });
    return () => trigger.kill();
  });

  return (
    <div ref={root} className="motion-safe:lg:flex motion-safe:lg:min-h-svh motion-safe:lg:items-center">
      <ol className="grid w-full gap-6 lg:grid-cols-3">
        {pillars.map((pillar, i) => {
          const accent = ACCENT[pillar.color];
          const dimmed = active !== null && active !== i;
          return (
            <li
              key={pillar.id}
              className={cn(
                'tile relative flex flex-col p-8 transition-[opacity,transform] duration-slow ease-out-expo md:p-10',
                dimmed && 'lg:scale-[0.97] lg:opacity-45',
              )}
            >
              <div className="flex items-start justify-between gap-4">
                <span className={accent.text}>
                  <Icon name={pillar.icon} className="size-10" />
                </span>
                {/* Decorative numeral drawn as generated content, so it is not text to assistive tech or contrast checks. */}
                <span
                  aria-hidden
                  data-num={`0${i + 1}`}
                  className={cn('text-h2 font-semibold tabular-nums opacity-20 before:content-[attr(data-num)]', accent.text)}
                />
              </div>
              {/* The pillar's own colour, as in the logo: a short bar, nothing louder. */}
              <span aria-hidden className={cn('mt-10 h-1 w-10 rounded-pill', accent.bar)} />
              <h3 className="mt-5 text-h3 font-semibold tracking-tight">{pillar.name}</h3>
              <p className="mt-3 text-lead text-ink-muted">{pillar.summary}</p>
              {pillar.detail && <p className="mt-4 text-ink-muted">{pillar.detail}</p>}
              <PendingMarker pending={pillar.pending} fallbacks={pillar.fallbacks} locale={locale} className="mt-6" />
            </li>
          );
        })}
      </ol>
    </div>
  );
}
