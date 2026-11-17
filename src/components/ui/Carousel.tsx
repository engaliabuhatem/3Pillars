'use client';

import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import { useDictionary } from '@/i18n/LocaleProvider';
import { cn } from '@/lib/utils';

interface CarouselProps {
  label: string;
  children: ReactNode[];
  itemClassName?: string;
}

/**
 * Horizontal scroll-snap row. Native scrolling does the work (touch, trackpad,
 * keyboard via Tab); the buttons only nudge it by one card. Direction-aware:
 * in RTL, "next" scrolls toward the start of the line's physical left.
 */
export function Carousel({ label, children, itemClassName }: CarouselProps) {
  const t = useDictionary().a11y;
  const track = useRef<HTMLUListElement>(null);
  const [edges, setEdges] = useState({ start: true, end: false });

  const measure = useCallback(() => {
    const el = track.current;
    if (!el) return;
    const travelled = Math.abs(el.scrollLeft);
    setEdges({ start: travelled < 8, end: travelled + el.clientWidth >= el.scrollWidth - 8 });
  }, []);

  useEffect(() => {
    const el = track.current;
    if (!el) return;
    measure();
    el.addEventListener('scroll', measure, { passive: true });
    window.addEventListener('resize', measure);
    return () => {
      el.removeEventListener('scroll', measure);
      window.removeEventListener('resize', measure);
    };
  }, [measure]);

  const step = (direction: 1 | -1) => {
    const el = track.current;
    if (!el) return;
    const card = el.querySelector('li');
    const distance = (card?.getBoundingClientRect().width ?? el.clientWidth) + 24;
    const rtl = getComputedStyle(el).direction === 'rtl';
    el.scrollBy({ left: direction * distance * (rtl ? -1 : 1), behavior: 'smooth' });
  };

  return (
    <div role="region" aria-roledescription="carousel" aria-label={label} className="relative min-w-0">
      <ul
        ref={track}
        tabIndex={0}
        className="-mx-(--spacing-gutter) flex snap-x snap-mandatory scroll-px-(--spacing-gutter) gap-6 overflow-x-auto px-(--spacing-gutter) pb-6 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
      >
        {children.map((child, i) => (
          <li key={i} className={cn('shrink-0 snap-start', itemClassName)}>
            {child}
          </li>
        ))}
      </ul>
      <div className="mt-4 flex justify-end gap-3">
        <CarouselButton label={t.previous} disabled={edges.start} onClick={() => step(-1)}>
          <ChevronLeft aria-hidden className="size-5 rtl:-scale-x-100" />
        </CarouselButton>
        <CarouselButton label={t.next} disabled={edges.end} onClick={() => step(1)}>
          <ChevronRight aria-hidden className="size-5 rtl:-scale-x-100" />
        </CarouselButton>
      </div>
    </div>
  );
}

function CarouselButton({ label, disabled, onClick, children }: { label: string; disabled: boolean; onClick: () => void; children: ReactNode }) {
  return (
    <button
      type="button"
      aria-label={label}
      disabled={disabled}
      onClick={onClick}
      className="grid size-12 place-items-center rounded-pill bg-surface text-navy ring-1 ring-hairline-strong ring-inset transition-colors duration-fast hover:ring-blue hover:text-blue disabled:opacity-40 on-navy:bg-white/10 on-navy:text-white on-navy:ring-hairline-inverse"
    >
      {children}
    </button>
  );
}
