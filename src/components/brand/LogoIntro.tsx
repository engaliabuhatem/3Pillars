'use client';

import { useEffect } from 'react';

/**
 * Runs before first paint (inlined via next/script beforeInteractive): marks
 * this visit for the logo draw-on. Once per session, never under reduced
 * motion.
 */
export const INTRO_SCRIPT = `try{if(!sessionStorage.getItem('3p-intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches){document.documentElement.dataset.intro='on'}sessionStorage.setItem('3p-intro','1')}catch(e){}`;

const DURATION_MS = 1400;

/**
 * The first-visit logo draw-on, played on the header logo in place: the
 * pillars rise (green, blue, grey, 80ms apart), the arcs draw, the name fades
 * in. It never covers the page, so content and LCP are not delayed, and there
 * is nothing to skip. The choreography lives in globals.css under
 * `[data-intro]`; this only ends it.
 */
export function LogoIntro() {
  useEffect(() => {
    const root = document.documentElement;
    if (root.dataset.intro !== 'on') return;
    const done = setTimeout(() => delete root.dataset.intro, DURATION_MS);
    return () => clearTimeout(done);
  }, []);

  return null;
}
