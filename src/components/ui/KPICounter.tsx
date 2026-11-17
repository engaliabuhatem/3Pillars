'use client';

import { useEffect, useRef } from 'react';
import { useLocale } from '@/i18n/LocaleProvider';
import { formatNumber } from '@/lib/utils';

interface KPICounterProps {
  value: number;
  prefix?: string;
  suffix?: string;
  label: string;
  source?: string;
  sourceLabel?: string;
}

const DURATION_MS = 1600;
/** The ease-out-expo curve from the motion tokens. */
const easeOutExpo = (t: number) => (t === 1 ? 1 : 1 - 2 ** (-10 * t));

/**
 * Counts up once on entry. The final number is in the server HTML and in an
 * aria-label, so a screen reader never hears the digits mid-count, and nothing
 * moves under reduced motion.
 */
export function KPICounter({ value, prefix = '', suffix = '', label, source, sourceLabel }: KPICounterProps) {
  const locale = useLocale();
  const ref = useRef<HTMLSpanElement>(null);
  const digits = Number.isInteger(value) ? 0 : 1;
  const final = `${prefix}${formatNumber(value, locale, digits)}${suffix}`;

  useEffect(() => {
    const node = ref.current;
    if (!node || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    // Already on screen at load: leave the final number alone.
    if (node.getBoundingClientRect().top < window.innerHeight) return;

    let frame = 0;
    const render = (v: number) => (node.textContent = `${prefix}${formatNumber(v, locale, digits)}${suffix}`);
    const io = new IntersectionObserver(
      ([entry]) => {
        if (!entry?.isIntersecting) return;
        io.disconnect();
        const start = performance.now();
        const tick = (now: number) => {
          const t = Math.min(1, (now - start) / DURATION_MS);
          render(value * easeOutExpo(t));
          if (t < 1) frame = requestAnimationFrame(tick);
        };
        frame = requestAnimationFrame(tick);
      },
      { threshold: 0.6 },
    );
    render(0);
    io.observe(node);
    return () => {
      io.disconnect();
      cancelAnimationFrame(frame);
      render(value);
    };
  }, [value, prefix, suffix, locale, digits]);

  return (
    <div className="flex flex-col gap-2">
      <span
        ref={ref}
        aria-label={final}
        className="text-[clamp(2.75rem,2rem+3vw,4.5rem)] leading-none font-semibold tabular-nums text-ink on-navy:text-white"
      >
        {final}
      </span>
      <span className="text-lg text-ink-muted on-navy:text-ink-inverse-muted">{label}</span>
      {source && (
        <span className="text-caption text-ink-muted on-navy:text-grey-300">
          {sourceLabel}: {source}
        </span>
      )}
    </div>
  );
}
