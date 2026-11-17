'use client';

import Script from 'next/script';
import { useEffect } from 'react';
import { track } from '@/lib/analytics';
import type { SiteSettings } from '@/lib/cms/types';
import { useConsent } from '@/hooks/useConsent';

/**
 * Loads the analytics provider only after consent, and turns every click on
 * an element with `data-track="event_name"` into an event — so components
 * declare what they track without importing anything.
 */
export function Analytics({ config }: { config: NonNullable<SiteSettings['analytics']> }) {
  const consent = useConsent();

  useEffect(() => {
    const onClick = (event: MouseEvent) => {
      const target = (event.target as Element | null)?.closest<HTMLElement>('[data-track]');
      if (target?.dataset.track) track(target.dataset.track, { path: location.pathname });
    };
    document.addEventListener('click', onClick);
    return () => document.removeEventListener('click', onClick);
  }, []);

  if (consent !== 'all') return null;

  if (config.provider === 'plausible') {
    return <Script defer data-domain={config.id} src="https://plausible.io/js/script.js" strategy="afterInteractive" />;
  }
  return (
    <>
      <Script src={`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(config.id)}`} strategy="afterInteractive" />
      <Script id="ga4" strategy="afterInteractive">
        {`window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}window.gtag=gtag;gtag('js',new Date());gtag('config',${JSON.stringify(config.id)},{anonymize_ip:true});`}
      </Script>
    </>
  );
}
