'use client';

import { useEffect, useRef, type CSSProperties } from 'react';

/**
 * Scroll progress as the logo's three pillars: green, blue and grey bars
 * that fill one after another down the page. One rAF-throttled listener
 * writes a single CSS variable; the bars derive their fill from it in CSS.
 */
export function PillarProgress() {
  const root = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let frame = 0;
    const update = () => {
      frame = 0;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      root.current?.style.setProperty('--progress', String(max > 0 ? Math.min(1, window.scrollY / max) : 0));
    };
    const onScroll = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    update();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
    };
  }, []);

  return (
    <div ref={root} aria-hidden className="pillar-progress pointer-events-none fixed end-3 top-1/2 z-30 hidden -translate-y-1/2 gap-1 md:flex">
      {['bg-green', 'bg-blue', 'bg-grey'].map((color, i) => (
        <span key={color} className="h-28 w-[3px] overflow-hidden rounded-pill bg-navy/10">
          <span className={`block size-full origin-top rounded-pill ${color}`} style={{ '--i': i } as CSSProperties} />
        </span>
      ))}
    </div>
  );
}
