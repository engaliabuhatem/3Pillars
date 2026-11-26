'use client';

import { Pause, Play } from 'lucide-react';
import Image, { getImageProps } from 'next/image';
import { useEffect, useRef, useState } from 'react';
import { ButtonLink } from '@/components/ui/Button';
import { Eyebrow } from '@/components/ui/Heading';
import { LineReveal } from '@/components/motion/LineReveal';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import { track } from '@/lib/analytics';
import type { Hero, Media } from '@/lib/cms/types';
import { cn } from '@/lib/utils';

/**
 * Full-viewport hero with an admin-uploaded background video.
 *
 * - The poster is the LCP element and is shown until the video can play.
 * - Playback pauses off-screen and in hidden tabs, and a visible button lets
 *   anyone stop it (WCAG 2.2.2).
 * - Reduced motion: poster only, no video download at all.
 * - Desktop and phones get their own video and poster (art direction): a
 *   portrait cut on phones, falling back to the desktop files.
 * - No video uploaded: the poster with a slow Ken Burns drift.
 * - The navy scrim keeps text ≥ 4.5:1 over the brightest frame: at the text's
 *   position the scrim is ≥ 80% navy, so even pure white beneath composites
 *   to a colour that white text clears comfortably (tests/e2e/hero.spec.ts).
 */
export function VideoHero({ hero }: { hero: Hero }) {
  const locale = useLocale();
  const t = useDictionary().a11y;
  const reduced = useReducedMotion();
  const video = useRef<HTMLVideoElement>(null);
  const section = useRef<HTMLElement>(null);
  const [ready, setReady] = useState(false);
  const [userPaused, setUserPaused] = useState(false);
  const [playing, setPlaying] = useState(false);

  // null until mounted: the server cannot know the screen, and the poster covers the gap.
  const [phone, setPhone] = useState<boolean | null>(null);

  const hasVideo = Boolean(hero.video.mp4 || hero.video.webm || hero.video.mobile);
  const showVideo = hasVideo && !reduced && phone !== null;
  const sources = videoSources(hero.video, phone ?? false);

  // A <video> picks its <source> once, so follow the breakpoint ourselves:
  // rotating a tablet or resizing a window swaps to the right cut.
  useEffect(() => {
    const query = window.matchMedia(PHONE);
    const update = () => {
      setReady(false);
      setPhone(query.matches);
    };
    update();
    query.addEventListener('change', update);
    return () => query.removeEventListener('change', update);
  }, []);

  useEffect(() => {
    const el = video.current;
    const host = section.current;
    if (!el || !host || !showVideo) return;

    let visible = true;
    const sync = () => {
      if (visible && !document.hidden && !userPaused) el.play().catch(() => setPlaying(false));
      else el.pause();
    };
    const io = new IntersectionObserver(([entry]) => {
      visible = Boolean(entry?.isIntersecting);
      sync();
    });
    io.observe(host);
    document.addEventListener('visibilitychange', sync);
    sync();
    return () => {
      io.disconnect();
      document.removeEventListener('visibilitychange', sync);
    };
  }, [showVideo, userPaused, phone]);

  const toggle = () => {
    track(userPaused ? 'hero_video_play' : 'hero_video_pause');
    setUserPaused(!userPaused);
  };

  return (
    <section
      ref={section}
      data-surface="navy"
      aria-labelledby="hero-title"
      className="relative isolate flex min-h-svh items-end overflow-hidden bg-navy text-white"
    >
      <div className="absolute inset-0 -z-10">
        {hero.poster && (
          <Poster
            desktop={hero.poster}
            mobile={hero.posterMobile}
            className={cn('object-cover', !hasVideo && !reduced && 'animate-ken-burns')}
          />
        )}
        {showVideo && (
          <video
            key={sources.map((source) => source.src).join()}
            ref={video}
            muted
            loop
            playsInline
            preload="metadata"
            aria-hidden
            onCanPlay={() => setReady(true)}
            onPlay={() => setPlaying(true)}
            onPause={() => setPlaying(false)}
            className={cn('absolute inset-0 size-full object-cover transition-opacity duration-slow', ready ? 'opacity-100' : 'opacity-0')}
          >
            {sources.map((source) => (
              <source key={source.src} src={source.src} type={source.type} />
            ))}
          </video>
        )}
        <div
          data-testid="hero-scrim"
          className="hero-scrim absolute inset-0"
        />
      </div>

      <div className="container-wide pt-32 pb-20 md:pb-28">
        <div className="max-w-4xl">
          {hero.eyebrow && <Eyebrow className="mb-6 text-blue-200">{hero.eyebrow}</Eyebrow>}
          {/*
           * The page heading search engines read is the small line; the large
           * display headline is styling, so it is a paragraph. Without an H1
           * set, the headline itself is the heading.
           */}
          {hero.h1 ? (
            <>
              <h1 id="hero-title" className="mb-4 text-lead font-semibold text-balance text-white/90">
                {hero.h1}
              </h1>
              <p className="max-w-3xl text-h1 font-semibold text-balance">
                <LineReveal text={hero.headline} delay={0.2} />
              </p>
            </>
          ) : (
            <h1 id="hero-title" className="text-display font-semibold text-balance">
              <LineReveal text={hero.headline} delay={0.2} />
            </h1>
          )}
          {hero.subline && <p className="mt-6 max-w-2xl text-lead text-white/85">{hero.subline}</p>}
          <div className="mt-10 flex flex-wrap gap-3">
            {hero.primary.label && (
              <ButtonLink href={hero.primary.href} locale={locale} variant="inverse" size="lg" arrow track="cta_hero_primary">
                {hero.primary.label}
              </ButtonLink>
            )}
            {hero.secondary.label && (
              <ButtonLink href={hero.secondary.href} locale={locale} variant="inverse-outline" size="lg" track="cta_hero_secondary">
                {hero.secondary.label}
              </ButtonLink>
            )}
          </div>
        </div>
      </div>

      {showVideo && (
        <button
          type="button"
          onClick={toggle}
          aria-label={playing ? t.pauseVideo : t.playVideo}
          aria-pressed={!playing}
          data-testid="hero-video-toggle"
          className="absolute end-5 bottom-5 grid size-12 place-items-center rounded-pill bg-white/15 text-white ring-1 ring-white/30 ring-inset backdrop-blur-md transition-colors duration-fast hover:bg-white/25"
        >
          {playing ? <Pause aria-hidden className="size-5" /> : <Play aria-hidden className="size-5" />}
        </button>
      )}
    </section>
  );
}

const PHONE = '(max-width: 767px)';

/** The portrait cut on phones; the desktop files elsewhere. Each falls back to the other. */
function videoSources(video: Hero['video'], phone: boolean) {
  const mobile = video.mobile ? [{ src: video.mobile.src, type: 'video/mp4' }] : [];
  const desktop = [
    ...(video.webm ? [{ src: video.webm.src, type: 'video/webm' }] : []),
    ...(video.mp4 ? [{ src: video.mp4.src, type: 'video/mp4' }] : []),
  ];
  if (phone) return mobile.length ? mobile : desktop;
  return desktop.length ? desktop : mobile;
}

/**
 * The poster is the LCP image, so it loads eagerly at high priority. With a
 * mobile poster, phones download only the portrait still and wider screens
 * only the landscape one.
 */
function Poster({ desktop, mobile, className }: { desktop: Media; mobile: Media | null; className: string }) {
  const common = { alt: '', fill: true, sizes: '100vw', fetchPriority: 'high', loading: 'eager' } as const;
  const { props } = getImageProps({ ...common, src: desktop.src, className });
  if (!mobile) return <Image {...props} alt="" />;
  const {
    props: { srcSet: phone },
  } = getImageProps({ ...common, src: mobile.src });
  return (
    <picture>
      <source media={PHONE} srcSet={phone} sizes="100vw" />
      {/* Art direction per the next/image docs: getImageProps already supplies the optimised srcSet. */}
      <img {...props} alt="" />
    </picture>
  );
}
