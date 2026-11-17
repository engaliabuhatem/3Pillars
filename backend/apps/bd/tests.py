import shutil
import tempfile
from datetime import timedelta
from unittest import mock
from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.throttling import ScopedRateThrottle

from apps.content.dashboard import dashboard_callback
from apps.content.models import Download, Project
from apps.core.models import ApprovalStatus, SiteSettings

from .models import Enquiry, ProposalRequest, Stage

TMP = tempfile.mkdtemp()
PDF = b"%PDF-1.7\n%test\n"

ENQUIRY = {"name": "Sara", "email": "sara@example.com", "message": "We need a PMC for a hospital.", "consent": True,
           "locale": "ar", "sourcePage": "/ar/contact"}

PROPOSAL = {
    "name": "Omar", "email": "omar@example.com", "organisation": "Port Authority", "projectType": "Terminal expansion",
    "location": "Aden", "projectStage": "feasibility", "budget": "10-50m", "timeline": "3m",
    "scope": "Project management consultancy for a two-phase container terminal expansion.", "consent": "true",
}


@override_settings(PRIVATE_MEDIA_ROOT=TMP, MEDIA_ROOT=TMP)
class FormTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TMP, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.api = APIClient()
        settings = SiteSettings.load()
        settings.notification_emails = "bd@3pillars.test\nnot-an-email"
        settings.save()

    def test_enquiry_saved_and_both_emails_sent(self):
        response = self.api.post("/api/enquiries/", ENQUIRY, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"ok": True})
        enquiry = Enquiry.objects.get()
        self.assertEqual((enquiry.locale, enquiry.source_page, enquiry.stage), ("ar", "/ar/contact", Stage.NEW))
        self.assertEqual([m.to for m in mail.outbox], [["bd@3pillars.test"], ["sara@example.com"]])
        self.assertIn("شكراً", mail.outbox[1].body)

    def test_consent_required(self):
        response = self.api.post("/api/enquiries/", {**ENQUIRY, "consent": False}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("consent", response.json())

    def test_honeypot_rejected_without_saving(self):
        response = self.api.post("/api/enquiries/", {**ENQUIRY, "website": "http://spam"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Enquiry.objects.exists())

    def test_turnstile_enforced_when_enabled(self):
        settings = SiteSettings.load()
        settings.turnstile_enabled = True
        settings.save()
        response = self.api.post("/api/enquiries/", ENQUIRY, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("turnstileToken", response.json())

    def test_rate_limited(self):
        # Pin the production rate: a local .env may lift it for e2e runs.
        with mock.patch.object(ScopedRateThrottle, "THROTTLE_RATES", {"forms": "10/hour"}):
            for _ in range(10):
                self.api.post("/api/enquiries/", ENQUIRY, format="json")
            self.assertEqual(self.api.post("/api/enquiries/", ENQUIRY, format="json").status_code, 429)

    def test_proposal_with_private_attachment(self):
        files = {"attachments": SimpleUploadedFile("brief.pdf", PDF, content_type="application/pdf")}
        response = self.api.post("/api/proposal-requests/", {**PROPOSAL, **files}, format="multipart")
        self.assertEqual(response.status_code, 201, response.content)
        attachment = ProposalRequest.objects.get().attachments.get()
        self.assertEqual(attachment.original_name, "brief.pdf")
        self.assertNotIn("brief", attachment.file.name)
        with self.assertRaises(ValueError):
            attachment.file.url  # noqa: B018 — private storage has no public URL

    def test_attachment_contents_are_sniffed(self):
        fake = SimpleUploadedFile("brief.pdf", b"MZ\x90\x00 not a pdf", content_type="application/pdf")
        response = self.api.post("/api/proposal-requests/", {**PROPOSAL, "attachments": fake}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(ProposalRequest.objects.exists())

    def test_short_scope_rejected(self):
        response = self.api.post("/api/proposal-requests/", {**PROPOSAL, "scope": "help"}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn("scope", response.json())

    def test_application_cv(self):
        cv = SimpleUploadedFile("cv.pdf", PDF, content_type="application/pdf")
        data = {"name": "Huda", "email": "huda@example.com", "cv": cv, "consent": "true"}
        response = self.api.post("/api/applications/", data, format="multipart")
        self.assertEqual(response.status_code, 201, response.content)

    def test_oversized_cv_rejected(self):
        cv = SimpleUploadedFile("cv.pdf", PDF + b"0" * (5 * 1024 * 1024), content_type="application/pdf")
        data = {"name": "Huda", "email": "huda@example.com", "cv": cv, "consent": "true"}
        self.assertEqual(self.api.post("/api/applications/", data, format="multipart").status_code, 400)

    def test_gated_download_hands_out_file_only_after_lead(self):
        doc = Download.objects.create(title="Capability statement", gated=True, approval=ApprovalStatus.APPROVED,
                                      file=SimpleUploadedFile("cap.pdf", PDF))
        listed = self.api.get("/api/downloads/").json()[0]
        self.assertIsNone(listed["file"])
        response = self.api.post(f"/api/downloads/{doc.pk}/lead/",
                                 {"name": "Ali", "email": "ali@example.com", "company": "X"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["url"].endswith(".pdf"))
        self.assertEqual(doc.leads.count(), 1)


class DashboardTests(TestCase):
    """Every card's number equals the row count of the changelist it links to."""

    def setUp(self):
        self.user = User.objects.create_superuser("root", "root@example.com", "x" * 14)
        self.client.force_login(self.user)
        past = timezone.localdate() - timedelta(days=3)
        common = {"name": "n", "email": "e@example.com", "project_type": "t", "location": "l",
                  "project_stage": "design", "timeline": "3m", "scope": "s" * 40}
        ProposalRequest.objects.create(**common)
        ProposalRequest.objects.create(**common, stage=Stage.QUALIFIED, next_follow_up=past)
        ProposalRequest.objects.create(**common, stage=Stage.WON, next_follow_up=past)
        Enquiry.objects.create(name="a", email="a@example.com", message="m")
        Enquiry.objects.create(name="b", email="b@example.com", message="m", is_handled=True)
        Project.objects.create(title="With image", summary="s", image="projects/a.png", image_alt="a")
        Project.objects.create(title="Without", summary="s")

    def test_counts_match_changelists(self):
        request = self.client.get("/admin/").wsgi_request
        context = dashboard_callback(request, {})
        cards = [*context["ak_attention"], *context["ak_tiles"]]
        self.assertTrue(cards)
        for card in cards:
            if not card["url"]:
                continue
            with self.subTest(card=card["label"]):
                url = urlparse(card["url"])
                response = self.client.get(url.path, {k: v for k, v in
                                                      (p.split("=", 1) for p in url.query.split("&") if p)})
                self.assertEqual(response.status_code, 200)
                self.assertNotIn("e=1", response.request.get("QUERY_STRING", ""))
                self.assertEqual(response.context["cl"].result_count, card["value"], card["url"])

    def test_overdue_excludes_closed_stages(self):
        cards = {c["label"]: c for c in dashboard_callback(self.client.get("/admin/").wsgi_request, {})["ak_attention"]}
        self.assertEqual(cards["Proposals past follow-up"]["value"], 1)
        self.assertEqual(cards["Unhandled enquiries"]["value"], 1)
        self.assertEqual(cards["Project images missing a description"]["value"], 1)
