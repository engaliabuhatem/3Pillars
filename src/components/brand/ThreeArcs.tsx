import type { CSSProperties } from 'react';

/*
 * The stationery motif: three thin parallel arcs (grey, blue, green) on navy.
 * Drawn with the on-navy tints, because the CI blue/green/grey fall below
 * 3:1 on navy and these strokes are meant to be seen.
 *
 * `data-reveal="draw"` makes the arcs draw themselves on entry (globals.css).
 */
const ARCS = [
  { d: 'M-40 560C220 500 600 360 820 80C880 0 900 -60 900 -120', stroke: 'var(--color-grey-300)' },
  { d: 'M-40 600C240 540 640 400 880 110C950 20 980 -40 990 -100', stroke: 'var(--color-blue-300)' },
  { d: 'M-40 640C260 580 680 440 940 140C1020 50 1060 -20 1080 -80', stroke: 'var(--color-green-300)' },
];

export function ThreeArcs({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 1000 640"
      preserveAspectRatio="xMaxYMax slice"
      aria-hidden
      className={className}
      fill="none"
      data-reveal="draw"
    >
      {ARCS.map((arc, i) => (
        <path
          key={arc.d}
          d={arc.d}
          stroke={arc.stroke}
          strokeWidth={1.25}
          strokeLinecap="round"
          vectorEffect="non-scaling-stroke"
          pathLength={1}
          opacity={0.75}
          style={{ '--arc-delay': `${i * 150}ms` } as CSSProperties}
        />
      ))}
    </svg>
  );
}
