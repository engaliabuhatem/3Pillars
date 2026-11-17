"""
Tell the Next.js site which cache tags a content change invalidates.

The request body is JSON `{"tags": [...], "ts": <unix seconds>}`, signed with
HMAC-SHA256 over the raw body using REVALIDATE_SECRET, in the
`X-Revalidate-Signature` header. Next rejects unsigned or stale bodies.

Sending happens after the transaction commits and on a short-lived thread, so
a slow or unreachable site never slows down or breaks an editor's save. The
site also revalidates on a timer, so a missed webhook heals itself.
"""

import hashlib
import hmac
import json
import logging
import threading
import time
import urllib.request

from django.conf import settings
from django.db import transaction

log = logging.getLogger(__name__)

_pending = threading.local()


def sign(body: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def _send(tags: list[str]) -> None:
    url, secret = settings.REVALIDATE_URL, settings.REVALIDATE_SECRET
    if not url or not secret:
        return
    body = json.dumps({"tags": tags, "ts": int(time.time())}).encode()
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "X-Revalidate-Signature": sign(body, secret)},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            response.read()
    except Exception as exc:  # The timed fallback covers a missed webhook.
        log.warning("revalidate webhook failed for %s: %s", tags, exc)


def _flush() -> None:
    tags = sorted(getattr(_pending, "tags", set()))
    _pending.tags = set()
    if tags:
        # Not a daemon: short-lived processes (manage.py seed, shell) must still
        # get the webhook out before exiting. _send is bounded by its timeout.
        threading.Thread(target=_send, args=(tags,), daemon=False).start()


def queue(tags) -> None:
    """
    Collect tags and flush them once the transaction commits.

    Every call registers a flush; the first to run sends the whole batch and
    the rest find it empty. Tags from a rolled-back transaction ride along with
    the next commit, which costs one harmless extra invalidation, never a
    missed one.
    """
    if not tags:
        return
    _pending.tags = getattr(_pending, "tags", set()) | set(tags)
    transaction.on_commit(_flush)
