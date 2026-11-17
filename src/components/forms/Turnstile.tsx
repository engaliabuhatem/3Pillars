'use client';

import Script from 'next/script';
import { useEffect, useRef } from 'react';
import { useLocale } from '@/i18n/LocaleProvider';

interface TurnstileApi {
  render: (el: HTMLElement, options: Record<string, unknown>) => string;
  remove: (id: string) => void;
}

/** Cloudflare Turnstile, rendered only when enabled in Site settings. */
export function Turnstile({ siteKey, onToken }: { siteKey: string; onToken: (token: string) => void }) {
  const locale = useLocale();
  const host = useRef<HTMLDivElement>(null);
  const widget = useRef<string | null>(null);
  const callback = useRef(onToken);

  useEffect(() => {
    callback.current = onToken;
  }, [onToken]);

  const mount = () => {
    const api = (window as unknown as { turnstile?: TurnstileApi }).turnstile;
    if (!api || !host.current || widget.current) return;
    widget.current = api.render(host.current, {
      sitekey: siteKey,
      language: locale,
      callback: (token: string) => callback.current(token),
      'expired-callback': () => callback.current(''),
    });
  };

  useEffect(() => {
    mount();
    return () => {
      const api = (window as unknown as { turnstile?: TurnstileApi }).turnstile;
      if (api && widget.current) api.remove(widget.current);
      widget.current = null;
    };
  });

  return (
    <>
      <Script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" strategy="afterInteractive" onLoad={mount} />
      <div ref={host} />
    </>
  );
}
