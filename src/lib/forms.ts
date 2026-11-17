'use client';

/**
 * Posts a form to the CMS API from the browser. Field errors come back from
 * DRF as `{fieldName: ["message"]}` (camelCase, like everything on the wire)
 * and are flattened to one message per field for the inputs to show.
 */

export type FieldErrors = Record<string, string>;

export type SubmitResult<T = unknown> =
  | { ok: true; data: T }
  | { ok: false; errors: FieldErrors; status: number };

function apiBase(): string {
  const base = process.env.NEXT_PUBLIC_CMS_API_URL;
  if (!base) throw new Error('NEXT_PUBLIC_CMS_API_URL is not set');
  return base.replace(/\/$/, '');
}

function flatten(body: unknown): FieldErrors {
  if (!body || typeof body !== 'object') return {};
  const errors: FieldErrors = {};
  for (const [key, value] of Object.entries(body as Record<string, unknown>)) {
    const message = Array.isArray(value) ? value[0] : value;
    if (typeof message === 'string') errors[key === 'nonFieldErrors' || key === 'detail' ? 'form' : key] = message;
  }
  return errors;
}

export async function submitForm<T = unknown>(path: string, body: Record<string, unknown> | FormData): Promise<SubmitResult<T>> {
  const isMultipart = body instanceof FormData;
  try {
    const response = await fetch(`${apiBase()}/${path.replace(/^\//, '')}`, {
      method: 'POST',
      body: isMultipart ? body : JSON.stringify(body),
      headers: isMultipart ? undefined : { 'Content-Type': 'application/json' },
    });
    const data = (await response.json().catch(() => ({}))) as T;
    if (response.ok) return { ok: true, data };
    return { ok: false, errors: flatten(data), status: response.status };
  } catch {
    return { ok: false, errors: {}, status: 0 };
  }
}

/** Where the visitor came from, attached to every lead. */
export function trackingFields(locale: string): Record<string, string> {
  const params = new URLSearchParams(window.location.search);
  return {
    locale,
    sourcePage: window.location.pathname,
    utmSource: params.get('utm_source') ?? '',
    utmMedium: params.get('utm_medium') ?? '',
    utmCampaign: params.get('utm_campaign') ?? '',
  };
}

export const isEmail = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
