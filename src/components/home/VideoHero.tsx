'use client';

import { Pause, Play } from 'lucide-react';
import Image from 'next/image';
import { useEffect, useRef, useState } from 'react';
import { ButtonLink } from '@/components/ui/Button';
import { Eyebrow } from '@/components/ui/Heading';
import { LineReveal } from '@/components/motion/LineReveal';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import { track } from '@/lib/analytics';
import type { Hero } from '@/lib/cms/types';
import { cn } from '@/lib/utils';

/**
 * Full-viewport hero with an admin-uploaded background video.
 *
 * - The poster is the LCP element and is shown until the video can play.
 * - Playback pauses off-screen and in hidden tabs, and a visible button lets
 *   anyone stop it (WCAG 2.2.2).
 * - Reduced motion: poster only, no video download at all.
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

  const hasVideo = Boolean(hero.video.mp4 || hero.video.webm || hero.video.mobile);
  const showVideo = hasVideo && !reduced;

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
  }, [showVideo, userPaused]);

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
          <Image
            src={hero.poster.src}
            alt=""
            fill
            priority
            sizes="100vw"
            className={cn('object-cover', !hasVideo && !reduced && 'animate-ken-burns')}
          />
        )}
        {showVideo && (
          <video
            ref={video}
            muted
            loop
            playsInline
            preload="metadata"
            poster={hero.poster?.src}
            aria-hidden
            onCanPlay={() => setReady(true)}
            onPlay={() => setPlaying(true)}
            onPause={() => setPlaying(false)}
            className={cn('absolute inset-0 size-full object-cover transition-opacity duration-slow', ready ? 'opacity-100' : 'opacity-0')}
          >
            {hero.video.mobile && <source src={hero.video.mobile.src} type="video/mp4" media="(max-width: 767px)" />}
            {hero.video.webm && <source src={hero.video.webm.src} type="video/webm" />}
            {hero.video.mp4 && <source src={hero.video.mp4.src} type="video/mp4" />}
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
          <h1 id="hero-title" className="text-display font-semibold text-balance">
            <LineReveal text={hero.headline} delay={0.2} />
          </h1>
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
