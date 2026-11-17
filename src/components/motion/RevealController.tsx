'use client';

import { usePathname } from 'next/navigation';
import { useEffect } from 'react';

const PENDING = 'reveal-pending';
const DONE = 'reveal-done';

/**
 * Drives every `[data-reveal]` element on the page with one observer.
 *
 * Only elements starting below the fold are hidden, so nothing visible ever
 * flashes. New elements (route changes, client-rendered lists) are picked up
 * by a MutationObserver.
 */
export function RevealController() {
  const pathname = usePathname();

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          entry.target.classList.remove(PENDING);
          entry.target.classList.add(DONE);
          io.unobserve(entry.target);
        }
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.12 },
    );

    const arm = (root: ParentNode) => {
      // Pending elements are re-observed too: a previous run of this effect
      // (StrictMode, a route change) may have hidden them and then disconnected.
      root.querySelectorAll<HTMLElement>(`[data-reveal]:not(.${DONE})`).forEach((el) => {
        if (el.classList.contains(PENDING)) {
          io.observe(el);
        } else if (el.getBoundingClientRect().top > window.innerHeight * 0.92) {
          el.classList.add(PENDING);
          io.observe(el);
        } else {
          el.classList.add(DONE);
        }
      });
    };

    arm(document);
    const mo = new MutationObserver((records) => {
      for (const record of records) record.addedNodes.forEach((node) => node instanceof HTMLElement && arm(node.parentNode ?? node));
    });
    mo.observe(document.body, { childList: true, subtree: true });

    return () => {
      io.disconnect();
      mo.disconnect();
    };
  }, [pathname]);

  return null;
}
