import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { ThreeArcs } from '../brand/ThreeArcs';

type Tone = 'canvas' | 'surface' | 'navy';

const TONES: Record<Tone, string> = {
  canvas: 'bg-canvas text-ink',
  surface: 'bg-surface text-ink',
  navy: 'bg-navy text-ink-inverse',
};

interface SectionProps {
  tone?: Tone;
  id?: string;
  labelledBy?: string;
  /** The stationery motif: three thin arcs that draw in on navy sections. */
  arcs?: boolean;
  tight?: boolean;
  className?: string;
  children: ReactNode;
}

/**
 * One band of a page. `data-surface="navy"` switches every child to the
 * on-navy palette (see the `on-navy:` variant), so components never have to
 * be told which background they sit on.
 */
export function Section({ tone = 'canvas', id, labelledBy, arcs, tight, className, children }: SectionProps) {
  return (
    <section
      id={id}
      aria-labelledby={labelledBy}
      data-surface={tone === 'navy' ? 'navy' : undefined}
      data-tone={tone}
      className={cn('relative isolate overflow-clip', tight ? 'py-16 md:py-24' : 'py-section', TONES[tone], className)}
    >
      {arcs && tone === 'navy' && <ThreeArcs className="pointer-events-none absolute inset-0 -z-10 size-full" />}
      {children}
    </section>
  );
}
