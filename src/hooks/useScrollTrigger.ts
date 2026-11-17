'use client';

import { useEffect, type RefObject } from 'react';
import type { ScrollTrigger as ScrollTriggerType } from 'gsap/ScrollTrigger';

type Setup = (gsap: typeof import('gsap').gsap, ScrollTrigger: typeof ScrollTriggerType) => (() => void) | void;

/**
 * Lazily loads GSAP + ScrollTrigger for one section, only on wide screens and
 * only when motion is welcome. Sections render complete without it; this
 * only adds the scroll-driven layer on top.
 */
export function useScrollTrigger(ref: RefObject<HTMLElement | null>, setup: Setup, minWidth = 1024) {
  useEffect(() => {
    const motionOk = window.matchMedia(`(prefers-reduced-motion: no-preference) and (min-width: ${minWidth}px)`);
    if (!motionOk.matches || !ref.current) return;

    let cleanup: (() => void) | void;
    let cancelled = false;
    let context: { revert: () => void } | undefined;

    void Promise.all([import('gsap'), import('gsap/ScrollTrigger')]).then(([{ gsap }, { ScrollTrigger }]) => {
      if (cancelled || !ref.current) return;
      gsap.registerPlugin(ScrollTrigger);
      context = gsap.context(() => {
        cleanup = setup(gsap, ScrollTrigger);
      }, ref.current);
    });

    return () => {
      cancelled = true;
      cleanup?.();
      context?.revert();
    };
    // `setup` is intentionally read once: sections declare it inline.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ref, minWidth]);
}
