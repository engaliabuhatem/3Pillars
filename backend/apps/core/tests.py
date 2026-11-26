import hashlib
import hmac
import json
import shutil
import tempfile
from io import BytesIO
from unittest import mock

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
from rest_framework.test import APIClient

from apps.content.models import Insight, InsightCategory, Project, Sector, Service
from apps.core import revalidate
from apps.core.models import ApprovalStatus, HomeSection, Page, Redirect, SiteSettings

TMP_MEDIA = tempfile.mkdtemp()


def png_bytes(width=1600, height=900) -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (width, height), (25, 23, 71)).save(buffer, format="PNG")
    return buffer.getvalue()


def gate(open_: bool):
    settings = SiteSettings.load()
    settings.show_pending_content = open_
    settings.save()


@override_settings(MEDIA_ROOT=TMP_MEDIA, PRIVATE_MEDIA_ROOT=TMP_MEDIA)
class ApprovalGateTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TMP_MEDIA, ignore_errors=True)

    def setUp(self):
        self.api = APIClient()
        self.live = Service.objects.create(name="Live", summary="s", approval=ApprovalStatus.APPROVED)
        self.draft = Service.objects.create(name="Draft", summary="s")

    def slugs(self, url):
        return [row["slug"] for row in self.api.get(url).json()]

    def test_pending_hidden_when_gate_closed(self):
        gate(False)
        self.assertEqual(self.slugs("/api/services/"), ["live"])
        self.assertEqual(self.api.get("/api/services/draft/").status_code, 404)

    def test_pending_served_with_marker_when_gate_open(self):
        gate(True)
        rows = {r["slug"]: r for r in self.api.get("/api/services/").json()}
        self.assertTrue(rows["draft"]["pending"])
        self.assertFalse(rows["live"]["pending"])

    def test_related_rows_obey_gate(self):
        gate(False)
        hidden = Sector.objects.create(name="Hidden")
        self.live.related_sectors.add(hidden)
        self.assertEqual(self.api.get("/api/services/live/").json()["relatedSectors"], [])

    def test_home_drops_sections_with_nothing_approved(self):
        gate(False)
        Sector.objects.create(name="Infrastructure", approval=ApprovalStatus.APPROVED)
        HomeSection.objects.create(kind="testimonial", approval=ApprovalStatus.APPROVED)
        HomeSection.objects.create(kind="sectors", order=1, approval=ApprovalStatus.APPROVED)
        HomeSection.objects.create(kind="intro", order=2)
        kinds = [s["kind"] for s in self.api.get("/api/home/").json()["sections"]]
        self.assertEqual(kinds, ["sectors"])

    def test_sitemap_lists_only_approved_even_on_staging(self):
        gate(True)
        paths = [e["path"] for e in self.api.get("/api/sitemap/").json()]
        self.assertIn("/services/live/", paths)
        self.assertNotIn("/services/draft/", paths)


class SingletonTests(TestCase):
    def test_second_create_updates_the_one_row(self):
        SiteSettings.objects.create(company_name="A")
        SiteSettings.objects.create(company_name="B")
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(SiteSettings.load().company_name, "B")

    def test_cannot_delete(self):
        with self.assertRaises(ValidationError):
            SiteSettings.load().delete()

    def test_poster_required_with_video(self):
        settings = SiteSettings.load()
        settings.hero_video = "hero/loop.mp4"
        with self.assertRaises(ValidationError) as ctx:
            settings.clean()
        self.assertIn("hero_poster", ctx.exception.message_dict)


class ArabicFallbackTests(TestCase):
    def setUp(self):
        gate(True)
        Service.objects.create(name="PMO & Project Controls", name_ar="مكتب إدارة المشاريع وضبط المشاريع",
                               summary="Stronger project governance")

    def test_arabic_replaces_english_and_reports_fallbacks(self):
        row = APIClient().get("/api/services/?locale=ar").json()[0]
        self.assertEqual(row["name"], "مكتب إدارة المشاريع وضبط المشاريع")
        self.assertEqual(row["summary"], "Stronger project governance")
        self.assertIn("summary", row["fallbacks"])
        self.assertNotIn("nameAr", row)

    def test_english_has_no_fallbacks(self):
        row = APIClient().get("/api/services/").json()[0]
        self.assertEqual(row["name"], "PMO & Project Controls")
        self.assertNotIn("fallbacks", row)

    def test_payload_is_camel_case(self):
        data = APIClient().get("/api/site-settings/").json()
        self.assertIn("showPendingContent", data)
        self.assertIn("companyName", data)


class SlugRedirectTests(TestCase):
    def test_slug_change_records_redirect_and_collapses_chains(self):
        service = Service.objects.create(name="Project Controls", summary="s")
        service.slug = "controls"
        service.save()
        service.slug = "pmo-project-controls"
        service.save()
        self.assertEqual(Redirect.objects.get(old_path="/services/project-controls/").new_path,
                         "/services/pmo-project-controls/")
        self.assertEqual(Redirect.objects.get(old_path="/services/controls/").new_path, "/services/pmo-project-controls/")

    def test_slug_made_unique(self):
        a = Sector.objects.create(name="Infrastructure")
        b = Sector.objects.create(name="Infrastructure")
        self.assertNotEqual(a.slug, b.slug)


class RichTextTests(TestCase):
    def test_script_and_handlers_stripped(self):
        page = Page.objects.create(title="About")
        block = page.blocks.create(body='<p onclick="x()">Hi<script>alert(1)</script><a href="javascript:x">l</a></p>')
        block.refresh_from_db()
        self.assertNotIn("script", block.body)
        self.assertNotIn("onclick", block.body)
        self.assertNotIn("javascript", block.body)


class RevalidationTests(TestCase):
    @override_settings(REVALIDATE_URL="http://site.test/api/revalidate", REVALIDATE_SECRET="s3cret")
    def test_one_signed_webhook_per_commit_with_model_tags(self):
        sent = []
        with mock.patch.object(revalidate.threading, "Thread") as thread:
            thread.side_effect = lambda target, args, daemon: mock.Mock(start=lambda: sent.append(args[0]))
            with self.captureOnCommitCallbacks(execute=True):
                Service.objects.create(name="A", summary="s")
                Sector.objects.create(name="B")
        self.assertEqual(len(sent), 1)
        self.assertTrue({"services", "sectors", "home", "navigation"} <= set(sent[0]))

    @override_settings(REVALIDATE_URL="http://site.test/api/revalidate", REVALIDATE_SECRET="s3cret")
    def test_body_is_hmac_signed(self):
        with mock.patch.object(revalidate.urllib.request, "urlopen") as urlopen:
            revalidate._send(["services"])
        request = urlopen.call_args.args[0]
        expected = hmac.new(b"s3cret", request.data, hashlib.sha256).hexdigest()
        self.assertEqual(request.headers["X-revalidate-signature"], expected)
        self.assertEqual(json.loads(request.data)["tags"], ["services"])

    @override_settings(REVALIDATE_URL="", REVALIDATE_SECRET="")
    def test_unconfigured_webhook_is_a_no_op(self):
        with mock.patch.object(revalidate.urllib.request, "urlopen") as urlopen:
            revalidate._send(["services"])
        urlopen.assert_not_called()


@override_settings(MEDIA_ROOT=TMP_MEDIA)
class ImageTests(TestCase):
    def test_renditions_written_on_save(self):
        sector = Sector(name="Infrastructure", image_alt="Harbour cranes at dusk", image_alt_ar="رافعات الميناء عند الغروب")
        sector.image = SimpleUploadedFile("port.png", png_bytes(), content_type="image/png")
        sector.full_clean()
        sector.save()
        storage = sector.image.storage
        self.assertTrue(storage.exists(f"{sector.image.name}.webp"))
        self.assertTrue(storage.exists(f"{sector.image.name}.avif"))

    def test_small_image_rejected(self):
        sector = Sector(name="Infrastructure", image_alt="x", image_alt_ar="x")
        sector.image = SimpleUploadedFile("tiny.png", png_bytes(200, 100), content_type="image/png")
        with self.assertRaises(ValidationError) as ctx:
            sector.full_clean()
        self.assertIn("image", ctx.exception.message_dict)

    def test_alt_text_required_in_both_languages(self):
        sector = Sector(name="Infrastructure", image="sectors/x.png")
        with self.assertRaises(ValidationError) as ctx:
            sector.clean()
        self.assertEqual(set(ctx.exception.message_dict), {"image_alt", "image_alt_ar"})

    def test_alt_text_cannot_be_the_keyword(self):
        sector = Sector(name="Infrastructure", image="sectors/x.png", primary_keyword="Infrastructure project management",
                        image_alt="infrastructure project management", image_alt_ar="وصف")
        with self.assertRaises(ValidationError) as ctx:
            sector.clean()
        self.assertEqual(set(ctx.exception.message_dict), {"image_alt"})


class RoleTests(TestCase):
    def test_editor_cannot_change_approval_but_approver_can(self):
        editor = User.objects.create_user("ed", password="x" * 12, is_staff=True)
        editor.groups.add(Group.objects.get(name="Editor"))
        approver = User.objects.create_user("ap", password="x" * 12, is_staff=True)
        approver.groups.add(Group.objects.get(name="Editor"), Group.objects.get(name="Approver"))
        model_admin = admin.site._registry[Service]
        request = mock.Mock()

        request.user = User.objects.get(pk=editor.pk)
        self.assertIn("approval", model_admin.get_readonly_fields(request))
        request.user = User.objects.get(pk=approver.pk)
        self.assertNotIn("approval", model_admin.get_readonly_fields(request))


class AdminSmokeTests(TestCase):
    """Every admin list and add form renders for a superuser (the 'click every sidebar item' check)."""

    def setUp(self):
        self.client.force_login(User.objects.create_superuser("root", "root@example.com", "x" * 14))
        category = InsightCategory.objects.create(name="News", slug="news")
        Insight.objects.create(title="Hello", excerpt="e", body="<p>b</p>", category=category)
        Project.objects.create(title="P", summary="s", delivery_entity="Delivery Co", our_role="advisor")

    def test_every_registered_model_renders(self):
        for model, model_admin in admin.site._registry.items():
            meta = model._meta
            with self.subTest(model=meta.label):
                url = reverse(f"admin:{meta.app_label}_{meta.model_name}_changelist")
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                if model_admin.has_add_permission(mock.Mock(user=response.wsgi_request.user)):
                    add = self.client.get(reverse(f"admin:{meta.app_label}_{meta.model_name}_add"))
                    self.assertEqual(add.status_code, 200)

    def test_change_forms_render(self):
        for obj in (Insight.objects.first(), Project.objects.first(), SiteSettings.load()):
            meta = obj._meta
            url = reverse(f"admin:{meta.app_label}_{meta.model_name}_change", args=[obj.pk])
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_dashboard_renders(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Needs attention")


class AdminLoginThrottleTests(TestCase):
    def test_lockout_after_repeated_failures(self):
        url = reverse("admin:login")
        for _ in range(5):
            self.client.post(url, {"username": "x", "password": "wrong"})
        self.assertEqual(self.client.post(url, {"username": "x", "password": "wrong"}).status_code, 429)


class ClientIpTests(TestCase):
    def test_spoofed_header_ignored_without_a_proxy(self):
        from django.test import RequestFactory

        from apps.core.security import client_ip

        request = RequestFactory().get("/", HTTP_X_REAL_IP="6.6.6.6", REMOTE_ADDR="10.0.0.1")
        self.assertEqual(client_ip(request), "10.0.0.1")
