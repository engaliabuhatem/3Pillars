'use client';

import { useRef } from 'react';
import { useScrollTrigger } from '@/hooks/useScrollTrigger';
import type { PillarColor } from '@/lib/cms/types';
import { cn } from '@/lib/utils';
import { PILLAR_BAR, pillarNumber } from './pillarStyle';

export interface FlowStep {
  number: number;
  name: string;
  color: PillarColor;
}

/*
 * The three arcs of the stationery motif, one per step, drawn as the section
 * scrolls: market intelligence feeds business development, which hands over
 * to project and programme management. Grey, blue, green on-navy tints, as in
 * the brand ThreeArcs.
 */
const ARCS = [
  { d: 'M40 150C200 40 360 40 500 110', stroke: 'var(--color-grey-300)' },
  { d: 'M500 110C640 180 800 180 960 70', stroke: 'var(--color-blue-300)' },
];

/**
 * "How the pillars work together" as a three-step flow. The arcs between the
 * steps draw with the scroll (scrubbed). Without the scroll layer, under
 * reduced motion and on narrow screens they are simply drawn.
 */
export function PillarFlow({ steps, label }: { steps: FlowStep[]; label: string }) {
  const root = useRef<HTMLDivElement>(null);

  useScrollTrigger(
    root,
    (gsap) => {
      gsap.fromTo(
        '[data-flow-arc]',
        { strokeDashoffset: 1 },
        {
          strokeDashoffset: 0,
          ease: 'none',
          stagger: 0.5,
          scrollTrigger: { trigger: root.current, start: 'top 75%', end: 'bottom 55%', scrub: 0.4 },
        },
      );
      gsap.fromTo(
        '[data-flow-step]',
        { opacity: 0.35, y: 12 },
        {
          opacity: 1,
          y: 0,
          stagger: 0.5,
          ease: 'none',
          scrollTrigger: { trigger: root.current, start: 'top 75%', end: 'bottom 55%', scrub: 0.4 },
        },
      );
    },
    768,
  );

  return (
    <div ref={root} className="relative">
      <svg aria-hidden viewBox="0 0 1000 200" className="absolute inset-x-0 top-0 hidden h-24 w-full md:block" fill="none" preserveAspectRatio="none">
        {ARCS.map((arc) => (
          <path
            key={arc.d}
            data-flow-arc
            d={arc.d}
            stroke={arc.stroke}
            strokeWidth={1.5}
            strokeLinecap="round"
            pathLength={1}
            strokeDasharray={1}
            vectorEffect="non-scaling-stroke"
          />
        ))}
      </svg>
      <ol aria-label={label} className="relative grid gap-6 md:grid-cols-3 md:pt-28">
        {steps.map((step) => (
          <li key={step.number} data-flow-step className="border-t border-hairline-inverse pt-6">
            <p className="eyebrow flex items-center gap-2.5 tabular-nums text-ink-inverse-muted">
              <span aria-hidden className={cn('h-1 w-8 rounded-pill', PILLAR_BAR[step.color])} />
              {pillarNumber(step.number)}
            </p>
            <p className="mt-3 text-h3 font-semibold text-balance">{step.name}</p>
          </li>
        ))}
      </ol>
    </div>
  );
}
