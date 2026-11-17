import Image from 'next/image';
import type { Media } from '@/lib/cms/types';
import { cn } from '@/lib/utils';

interface CmsImageProps {
  media: Media;
  sizes: string;
  priority?: boolean;
  className?: string;
  /** Fill the positioned parent instead of using intrinsic dimensions. */
  fill?: boolean;
}

/**
 * An image from the CMS through next/image (which negotiates AVIF/WebP). The
 * CMS's own renditions are a fallback for anything that bypasses this.
 */
export function CmsImage({ media, sizes, priority, className, fill = true }: CmsImageProps) {
  const intrinsic = !fill && media.width && media.height;
  return (
    <Image
      src={media.src}
      alt={media.alt}
      sizes={sizes}
      priority={priority}
      className={cn('object-cover', className)}
      {...(intrinsic ? { width: media.width ?? undefined, height: media.height ?? undefined } : { fill: true })}
    />
  );
}

interface MediaFrameProps {
  media: Media | null;
  sizes: string;
  ratio?: 'video' | 'portrait' | 'square' | 'wide';
  priority?: boolean;
  className?: string;
  /** Slow scroll drift of the image inside its frame (media only, never text). */
  parallax?: boolean;
  /** Edge to edge inside a card: the card does the rounding and clipping. */
  bleed?: boolean;
  /** Slow zoom when a parent `.group` (a card) is hovered. */
  zoom?: boolean;
}

const RATIOS = { video: 'aspect-video', portrait: 'aspect-[4/5]', square: 'aspect-square', wide: 'aspect-[21/9]' } as const;

const ZOOM = 'transition-transform duration-cinematic ease-out-expo group-hover:scale-[1.04] motion-reduce:group-hover:scale-100';

/** A rounded media cell. With no image it renders the branded placeholder, never a broken box. */
export function MediaFrame({ media, sizes, ratio = 'video', priority, className, parallax, bleed, zoom }: MediaFrameProps) {
  return (
    <div
      className={cn(
        'relative overflow-hidden bg-navy-50',
        !bleed && 'rounded-card',
        RATIOS[ratio],
        parallax && 'parallax-media',
        className,
      )}
    >
      {media ? (
        <CmsImage media={media} sizes={sizes} priority={priority} className={zoom ? ZOOM : undefined} />
      ) : (
        <div aria-hidden className="absolute inset-0 bg-[linear-gradient(135deg,var(--color-navy-50),var(--color-blue-50))]">
          <svg viewBox="0 0 400 225" preserveAspectRatio="xMidYMid slice" className="size-full" fill="none">
            <path d="M-10 200C80 170 220 120 300 40" stroke="var(--color-grey-200)" />
            <path d="M-10 215C90 185 240 130 330 45" stroke="var(--color-blue-200)" />
            <path d="M-10 230C100 200 260 140 360 50" stroke="var(--color-green-200)" />
          </svg>
        </div>
      )}
    </div>
  );
}
