'use client';

import { ChevronLeft, ChevronRight, X } from 'lucide-react';
import Image from 'next/image';
import { useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import { useDictionary } from '@/i18n/LocaleProvider';
import type { Media } from '@/lib/cms/types';

interface GalleryItem {
  image: Media | null;
  caption: string;
}

/**
 * Thumbnail grid that opens a native <dialog>: focus trapping, Escape and the
 * inert background come from the platform. Arrow keys move between images.
 */
export function Lightbox({ items }: { items: GalleryItem[] }) {
  const t = useDictionary().a11y;
  const dialog = useRef<HTMLDialogElement>(null);
  const [index, setIndex] = useState(0);
  const images = items.filter((item): item is { image: Media; caption: string } => Boolean(item.image));

  const open = (i: number) => {
    setIndex(i);
    dialog.current?.showModal();
  };
  const move = useCallback((by: number) => setIndex((i) => (i + by + images.length) % images.length), [images.length]);

  useEffect(() => {
    const el = dialog.current;
    if (!el) return;
    const onKey = (event: KeyboardEvent) => {
      const rtl = document.documentElement.dir === 'rtl';
      if (event.key === 'ArrowRight') move(rtl ? -1 : 1);
      if (event.key === 'ArrowLeft') move(rtl ? 1 : -1);
    };
    el.addEventListener('keydown', onKey);
    return () => el.removeEventListener('keydown', onKey);
  }, [move]);

  const current = images[index];

  return (
    <>
      <ul className="grid grid-cols-2 gap-4 md:grid-cols-3">
        {images.map((item, i) => (
          <li key={item.image.src}>
            <button
              type="button"
              onClick={() => open(i)}
              className="group relative block aspect-[4/3] w-full overflow-hidden rounded-lg"
              aria-label={`${t.openImage}: ${item.image.alt}`}
            >
              <Image
                src={item.image.src}
                alt=""
                fill
                sizes="(min-width: 768px) 33vw, 50vw"
                className="object-cover transition-transform duration-slow ease-out-expo group-hover:scale-105"
              />
            </button>
          </li>
        ))}
      </ul>

      <dialog
        ref={dialog}
        aria-label={current?.image.alt}
        className="m-auto h-dvh max-h-none w-dvw max-w-none bg-navy/95 p-0 text-white backdrop:bg-transparent"
        onClick={(event) => event.target === dialog.current && dialog.current?.close()}
      >
        {current && (
          <figure className="relative flex size-full flex-col items-center justify-center gap-4 p-6 md:p-16">
            <div className="relative size-full">
              <Image src={current.image.src} alt={current.image.alt} fill sizes="100vw" className="object-contain" />
            </div>
            {current.caption && <figcaption className="text-center text-ink-inverse-muted">{current.caption}</figcaption>}
          </figure>
        )}
        <div className="absolute inset-x-0 top-0 flex justify-end p-4">
          <IconButton label={t.close} onClick={() => dialog.current?.close()}>
            <X aria-hidden className="size-6" />
          </IconButton>
        </div>
        {images.length > 1 && (
          <div className="absolute inset-x-0 bottom-0 flex justify-center gap-3 p-6">
            <IconButton label={t.previous} onClick={() => move(-1)}>
              <ChevronLeft aria-hidden className="size-6 rtl:-scale-x-100" />
            </IconButton>
            <IconButton label={t.next} onClick={() => move(1)}>
              <ChevronRight aria-hidden className="size-6 rtl:-scale-x-100" />
            </IconButton>
          </div>
        )}
      </dialog>
    </>
  );
}

function IconButton({ label, onClick, children }: { label: string; onClick: () => void; children: ReactNode }) {
  return (
    <button
      type="button"
      aria-label={label}
      onClick={onClick}
      className="grid size-12 place-items-center rounded-pill bg-white/10 text-white transition-colors duration-fast hover:bg-white/20"
    >
      {children}
    </button>
  );
}
