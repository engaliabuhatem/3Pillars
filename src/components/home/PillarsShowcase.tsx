'use client';

import { useRef, useState } from 'react';
import { Icon } from '@/components/ui/Icon';
import { PendingMarker } from '@/components/ui/Tag';
import { useScrollTrigger } from '@/hooks/useScrollTrigger';
import { useLocale } from '@/i18n/LocaleProvider';
import type { Pillar } from '@/lib/cms/types';
import { cn } from '@/lib/utils';

const ACCENT: Record<Pillar['color'], { bar: string; text: string; tint: string }> = {
  green: { bar: 'bg-green', text: 'text-green', tint: 'bg-green-50' },
  blue: { bar: 'bg-blue', text: 'text-blue', tint: 'bg-blue-50' },
  grey: { bar: 'bg-grey', text: 'text-grey', tint: 'bg-grey-50' },
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
                'relative flex flex-col overflow-hidden rounded-lg bg-surface p-8 ring-1 ring-hairline ring-inset transition-[opacity,transform] duration-slow ease-out-expo md:p-10',
                dimmed && 'lg:scale-[0.97] lg:opacity-45',
              )}
            >
              <span aria-hidden className={cn('absolute inset-y-0 start-0 w-1.5', accent.bar)} />
              <div className="flex items-center justify-between gap-4">
                <span className={cn('grid size-12 place-items-center rounded-md', accent.tint, accent.text)}>
                  <Icon name={pillar.icon} className="size-6" />
                </span>
                {/* Decorative numeral drawn as generated content, so it is not text to assistive tech or contrast checks. */}
                <span
                  aria-hidden
                  data-num={`0${i + 1}`}
                  className={cn('text-h2 font-semibold tabular-nums opacity-20 before:content-[attr(data-num)]', accent.text)}
                />
              </div>
              <h3 className="mt-8 text-h3 font-semibold">{pillar.name}</h3>
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
