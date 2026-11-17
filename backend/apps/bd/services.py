"""
What happens around a form submission: bot checks, then the emails.

Kept out of the views so every form (enquiry, proposal, application, download
lead) runs the same checks in the same order.
"""

import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers

from apps.core.models import SiteSettings
from apps.core.security import client_ip

log = logging.getLogger(__name__)

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


class SpamCheckMixin(serializers.Serializer):
    """
    `website` is a honeypot: hidden from people, irresistible to bots. A filled
    honeypot is rejected with the same generic error a bad token gets, so a bot
    learns nothing about which check caught it.
    """

    website = serializers.CharField(required=False, allow_blank=True, write_only=True)
    turnstile_token = serializers.CharField(required=False, allow_blank=True, write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        honeypot = attrs.pop("website", "")
        token = attrs.pop("turnstile_token", "")
        if honeypot:
            raise serializers.ValidationError("Submission rejected.")
        site = SiteSettings.load()
        if site.turnstile_enabled and not verify_turnstile(token, client_ip(self.context["request"])):
            raise serializers.ValidationError({"turnstile_token": "Please complete the security check."})
        return attrs


def verify_turnstile(token: str, ip: str) -> bool:
    if not token or not settings.TURNSTILE_SECRET_KEY:
        return False
    payload = urllib.parse.urlencode(
        {"secret": settings.TURNSTILE_SECRET_KEY, "response": token, "remoteip": ip}
    ).encode()
    try:
        with urllib.request.urlopen(TURNSTILE_VERIFY_URL, data=payload, timeout=5) as response:
            return bool(json.loads(response.read()).get("success"))
    except Exception as exc:
        log.warning("turnstile verification failed: %s", exc)
        return False


AUTO_REPLY = {
    "en": (
        "We have received your message",
        "Dear {name},\n\nThank you for contacting {company}. We have received your {what} "
        "and a member of our team will reply within two working days.\n\nKind regards,\n{company}",
    ),
    "ar": (
        "تم استلام رسالتكم",
        "السيد/السيدة {name}،\n\nشكراً لتواصلكم مع {company}. لقد استلمنا {what} وسيتواصل معكم "
        "أحد أعضاء فريقنا خلال يومي عمل.\n\nمع خالص التحية،\n{company}",
    ),
}

WHAT = {
    "enquiry": {"en": "enquiry", "ar": "استفساركم"},
    "proposal": {"en": "proposal request", "ar": "طلب العرض"},
    "application": {"en": "application", "ar": "طلب التوظيف"},
}


def notify(kind: str, record, *, admin_path: str, summary: str) -> None:
    """Email staff, then send the sender a short acknowledgement in their language."""
    site = SiteSettings.load()
    recipients = site.notification_list
    try:
        if recipients:
            send_mail(
                subject=f"[3 Pillars] New {WHAT[kind]['en']}: {summary}",
                message=f"{summary}\n\nOpen in the admin:\n{settings.SITE_URL.rstrip('/')}{admin_path}",
                from_email=None,
                recipient_list=recipients,
            )
        locale = "ar" if getattr(record, "locale", "en") == "ar" else "en"
        subject, body = AUTO_REPLY[locale]
        company = (site.company_name_ar if locale == "ar" else "") or site.company_name
        send_mail(
            subject=subject,
            message=body.format(name=record.name, company=company, what=WHAT[kind][locale]),
            from_email=None,
            recipient_list=[record.email],
        )
    except Exception as exc:  # The record is saved; a mail outage must not lose it.
        log.error("notification email failed for %s %s: %s", kind, record.pk, exc)
