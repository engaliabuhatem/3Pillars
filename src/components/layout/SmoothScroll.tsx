'use client';

import { useEffect } from 'react';
import { useReducedMotion } from '@/hooks/useReducedMotion';

/**
 * Lenis smooth scrolling, never under reduced motion. Loaded after the page is
 * idle so it never competes with first paint. It scrolls the window, so
 * ScrollTrigger needs no bridge.
 */
export function SmoothScroll() {
  const reduced = useReducedMotion();

  useEffect(() => {
    if (reduced) return;
    let frame = 0;
    let destroy: (() => void) | undefined;
    let cancelled = false;

    const start = () =>
      import('lenis').then(({ default: Lenis }) => {
        if (cancelled) return;
        const lenis = new Lenis({ duration: 1.1, easing: (t) => 1 - Math.pow(1 - t, 4) });
        const loop = (time: number) => {
          lenis.raf(time);
          frame = requestAnimationFrame(loop);
        };
        frame = requestAnimationFrame(loop);
        destroy = () => lenis.destroy();
      });

    // Safari has no requestIdleCallback; a short timeout is close enough there.
    const hasIdle = typeof requestIdleCallback === 'function';
    const idle = hasIdle ? requestIdleCallback(start) : setTimeout(start, 1200);
    return () => {
      cancelled = true;
      if (hasIdle) cancelIdleCallback(idle as number);
      else clearTimeout(idle);
      cancelAnimationFrame(frame);
      destroy?.();
    };
  }, [reduced]);

  return null;
}
