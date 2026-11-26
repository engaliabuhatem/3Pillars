'use client';

import { useRef } from 'react';
import { Icon } from '@/components/ui/Icon';
import { useScrollTrigger } from '@/hooks/useScrollTrigger';
import type { LifecycleStage } from '@/lib/cms/types';

/**
 * Project lifecycle, Initiation → Closeout. A line draws down through the
 * stages as the section scrolls (scrubbed, so it follows the reader exactly).
 * Without the scroll layer the line is simply drawn in full.
 */
export function ApproachTimeline({ stages }: { stages: LifecycleStage[] }) {
  const root = useRef<HTMLOListElement>(null);

  useScrollTrigger(
    root,
    (gsap) => {
      gsap.fromTo(
        '[data-line]',
        { scaleY: 0 },
        { scaleY: 1, ease: 'none', scrollTrigger: { trigger: root.current, start: 'top 70%', end: 'bottom 60%', scrub: 0.4 } },
      );
      gsap.utils.toArray<HTMLElement>('[data-stage]').forEach((stage) => {
        gsap.fromTo(
          stage.querySelector('[data-dot]'),
          { scale: 0.6, backgroundColor: 'var(--color-navy-100)' },
          {
            scale: 1,
            backgroundColor: 'var(--color-blue)',
            duration: 0.3,
            scrollTrigger: { trigger: stage, start: 'top 60%', toggleActions: 'play none none reverse' },
          },
        );
      });
    },
    768,
  );

  return (
    <ol ref={root} className="relative grid gap-12 ps-12 md:ps-20">
      <span aria-hidden className="absolute start-[11px] top-2 bottom-2 w-px bg-navy-100 md:start-[19px]" />
      <span aria-hidden data-line className="absolute start-[11px] top-2 bottom-2 w-px origin-top bg-blue md:start-[19px]" />
      {stages.map((stage, i) => (
        <li key={stage.id} data-stage className="relative grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)] md:gap-12">
          <span
            aria-hidden
            data-dot
            className="absolute -start-12 top-1 grid size-6 place-items-center rounded-pill bg-blue text-white ring-4 ring-canvas md:-start-20 md:size-10"
          >
            <Icon name={stage.icon} className="size-3 md:size-5" />
          </span>
          <div>
            <p className="text-caption font-semibold text-blue tabular-nums">0{i + 1}</p>
            <h3 className="mt-1 text-h3 font-semibold">{stage.name}</h3>
          </div>
          <div>
            <p className="text-lead text-ink-muted">{stage.summary}</p>
            {stage.deliverables.length > 0 && (
              <ul className="mt-5 flex flex-wrap gap-2">
                {stage.deliverables.map((item) => (
                  <li key={item} className="rounded-pill bg-surface px-3 py-1 text-caption ring-1 ring-hairline ring-inset">
                    {item}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}
