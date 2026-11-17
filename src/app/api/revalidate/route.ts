import { createHmac, timingSafeEqual } from 'node:crypto';
import { revalidateTag } from 'next/cache';
import type { NextRequest } from 'next/server';

/**
 * Django's content webhook (backend/apps/core/revalidate.py).
 *
 * The body is `{"tags": [...], "ts": <unix seconds>}`, HMAC-SHA256 signed with
 * REVALIDATE_SECRET. Bodies older than five minutes are refused so a captured
 * request cannot be replayed indefinitely.
 */

const MAX_AGE_SECONDS = 300;
const TAG = /^[a-z][a-z-]{0,39}$/;

function verify(body: string, signature: string | null, secret: string): boolean {
  if (!signature) return false;
  const expected = createHmac('sha256', secret).update(body).digest();
  const given = Buffer.from(signature, 'hex');
  return given.length === expected.length && timingSafeEqual(given, expected);
}

export async function POST(request: NextRequest) {
  const secret = process.env.REVALIDATE_SECRET;
  if (!secret) return Response.json({ error: 'not configured' }, { status: 503 });

  const body = await request.text();
  if (!verify(body, request.headers.get('x-revalidate-signature'), secret)) {
    return Response.json({ error: 'bad signature' }, { status: 401 });
  }

  let payload: { tags?: unknown; ts?: unknown };
  try {
    payload = JSON.parse(body) as typeof payload;
  } catch {
    return Response.json({ error: 'bad body' }, { status: 400 });
  }

  const age = Date.now() / 1000 - Number(payload.ts);
  if (!Number.isFinite(age) || age > MAX_AGE_SECONDS || age < -60) {
    return Response.json({ error: 'stale' }, { status: 401 });
  }

  const tags = Array.isArray(payload.tags) ? payload.tags.filter((t): t is string => typeof t === 'string' && TAG.test(t)) : [];
  // A webhook is not a Server Action, so updateTag is unavailable; expire:0
  // makes the next request render fresh content rather than a stale copy.
  for (const tag of tags) revalidateTag(tag, { expire: 0 });

  return Response.json({ revalidated: tags });
}
