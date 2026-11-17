'use client';

import { useSyncExternalStore } from 'react';

export type Consent = 'all' | 'essential';

const KEY = '3p-consent';
const EVENT = 'consent-change';

function read(): Consent | null {
  try {
    const value = localStorage.getItem(KEY);
    return value === 'all' || value === 'essential' ? value : null;
  } catch {
    return null;
  }
}

function subscribe(onChange: () => void) {
  window.addEventListener(EVENT, onChange);
  window.addEventListener('storage', onChange);
  return () => {
    window.removeEventListener(EVENT, onChange);
    window.removeEventListener('storage', onChange);
  };
}

/**
 * The visitor's cookie choice, shared by the banner and the analytics loader.
 * The server snapshot is "essential", so nothing renders or loads before the
 * real choice is read in the browser.
 */
export function useConsent(): Consent | null {
  return useSyncExternalStore(subscribe, read, () => 'essential');
}

export function setConsent(value: Consent): void {
  try {
    localStorage.setItem(KEY, value);
  } catch {
    // Private mode: the choice lasts for this page view only.
  }
  window.dispatchEvent(new Event(EVENT));
}
