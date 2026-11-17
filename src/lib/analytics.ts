/**
 * Analytics events: CTA clicks, form steps and submits, downloads, video
 * play/pause. Calls are no-ops until the visitor accepts cookies and the
 * provider script (Plausible or GA4, chosen in Site settings) has loaded.
 */

type Props = Record<string, string | number | boolean>;

interface AnalyticsWindow {
  plausible?: (event: string, options?: { props?: Props }) => void;
  gtag?: (command: 'event', event: string, params?: Props) => void;
}

export function track(event: string, props: Props = {}): void {
  if (typeof window === 'undefined') return;
  const w = window as unknown as AnalyticsWindow;
  w.plausible?.(event, { props });
  w.gtag?.('event', event, props);
}
