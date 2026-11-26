from unittest import mock

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase
from rest_framework.test import APIClient

from apps.core.admin_base import approve
from apps.core.models import ApprovalStatus, HomeSection, NavItem, Page, SiteSettings
from apps.core.seo import seo_duplicates

from .models import Insight, Project, Sector, SectorFAQ, Service

APPROVED = ApprovalStatus.APPROVED


def gate(open_: bool):
    settings = SiteSettings.load()
    settings.show_pending_content = open_
    settings.save()


def project(**extra):
    return Project.objects.create(**{"title": "Port programme", "summary": "s", "delivery_entity": "Delivery Co",
                                     "our_role": Project.Role.PMO_SUPPORT, **extra})


def admin_request(user):
    request = RequestFactory().post("/")
    request.user = user
    request.session = {}
    request._messages = FallbackStorage(request)
    return request


class AttributionGateTests(TestCase):
    def test_project_cannot_be_approved_without_confirmed_attribution(self):
        row = project(approval=APPROVED)
        with self.assertRaises(ValidationError) as ctx:
            row.full_clean()
        self.assertIn("approval", ctx.exception.message_dict)
        row.attribution_approved = True
        row.full_clean()

    def test_bulk_approve_skips_unconfirmed_projects(self):
        blocked, ready = project(), project(title="Ready", attribution_approved=True)
        user = User.objects.create_superuser("root", "root@example.com", "x" * 14)
        approve(admin.site._registry[Project], admin_request(user), Project.objects.all())
        blocked.refresh_from_db()
        ready.refresh_from_db()
        self.assertEqual((blocked.approval, ready.approval), (ApprovalStatus.PENDING, APPROVED))

    def test_client_named_only_with_agreement(self):
        gate(True)
        project(client_public_name="National Ports Authority")
        self.assertIsNone(APIClient().get("/api/projects/").json()["results"][0]["client"])
        Project.objects.update(client_name_approved=True)
        self.assertEqual(APIClient().get("/api/projects/").json()["results"][0]["client"], "National Ports Authority")


class ArabicIndexingTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        gate(True)

    def indexable(self, slug):
        return self.api.get(f"/api/services/{slug}/").json()["seo"]["indexable"]

    def test_pending_page_is_never_indexable(self):
        Service.objects.create(name="Draft")
        self.assertEqual(self.indexable("draft"), {"en": False, "ar": False})

    def test_arabic_waits_for_review(self):
        service = Service.objects.create(name="Live", approval=APPROVED)
        self.assertEqual(self.indexable("live"), {"en": True, "ar": False})
        service.ar_reviewed = True
        service.save()
        self.assertEqual(self.indexable("live"), {"en": True, "ar": True})

    def test_sitemap_marks_which_arabic_pages_may_be_listed(self):
        Service.objects.create(name="Reviewed", approval=APPROVED, ar_reviewed=True)
        Service.objects.create(name="Unreviewed", approval=APPROVED)
        entries = {e["path"]: e["ar"] for e in self.api.get("/api/sitemap/").json()}
        self.assertTrue(entries["/services/reviewed/"])
        self.assertFalse(entries["/services/unreviewed/"])


class DraftTopicTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        gate(True)
        self.topic = Insight.objects.create(title="Why Project Controls Matter", is_draft_topic=True)
        Insight.objects.create(title="Written", body="<p>Body</p>")

    def test_topic_without_body_is_hidden_even_on_staging(self):
        slugs = [row["slug"] for row in self.api.get("/api/insights/").json()["results"]]
        self.assertEqual(slugs, ["written"])
        self.assertEqual(self.api.get(f"/api/insights/{self.topic.slug}/").status_code, 404)

    def test_topic_cannot_be_approved_or_listed_in_the_sitemap(self):
        self.topic.approval = APPROVED
        with self.assertRaises(ValidationError):
            self.topic.full_clean()
        Insight.objects.filter(pk=self.topic.pk).update(approval=APPROVED)
        paths = [e["path"] for e in self.api.get("/api/sitemap/").json()]
        self.assertNotIn(f"/insights/{self.topic.slug}/", paths)

    def test_news_needs_date_summary_and_role(self):
        news = Insight(title="Appointment", body="<p>b</p>", kind=Insight.Kind.NEWS, published_at=None)
        with self.assertRaises(ValidationError) as ctx:
            news.full_clean()
        self.assertTrue({"published_at", "excerpt", "our_role_statement"} <= set(ctx.exception.message_dict))


class NavigationTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        Service.objects.create(name="Business Development")
        services = NavItem.objects.create(label="Services", link="/services/")
        NavItem.objects.create(label="Business Development", link="/services/business-development/", parent=services)
        NavItem.objects.create(label="Projects", link="/projects/", order=1)
        NavItem.objects.create(label="Home", link="/", order=2)
        Page.objects.create(title="Services", slug="services")
        Page.objects.create(title="Projects", slug="projects")

    def header(self):
        return {item["label"]: [c["label"] for c in item["children"]]
                for item in self.api.get("/api/navigation/").json()["header"]}

    def test_items_without_published_content_are_hidden(self):
        gate(False)
        self.assertEqual(self.header(), {"Home": []})

    def test_staging_shows_pending_pages(self):
        gate(True)
        self.assertEqual(self.header()["Services"], ["Business Development"])

    def test_projects_hidden_until_one_project_is_approved(self):
        gate(True)
        project()
        self.assertNotIn("Projects", self.header())
        project(title="Approved", attribution_approved=True, approval=APPROVED)
        self.assertIn("Projects", self.header())


class SiteCopyGateTests(TestCase):
    def setUp(self):
        settings = SiteSettings.load()
        settings.tagline = "3 Pillars helps public and private sector clients…"
        settings.hero_headline = "Turning Projects into Progress."
        settings.email = "info@example.com"
        settings.save()
        self.api = APIClient()

    def test_unapproved_site_wording_stays_off_the_live_site(self):
        gate(False)
        data = self.api.get("/api/site-settings/").json()
        self.assertEqual((data["tagline"], data["hero"]["headline"]), ("", ""))
        gate(True)
        self.assertEqual(self.api.get("/api/site-settings/").json()["hero"]["headline"], "Turning Projects into Progress.")

    def test_contact_details_only_once_verified(self):
        self.assertEqual(self.api.get("/api/site-settings/").json()["email"], "")
        settings = SiteSettings.load()
        settings.contact_verified = True
        settings.save()
        self.assertEqual(self.api.get("/api/site-settings/").json()["email"], "info@example.com")

    def test_unapproved_home_section_is_dropped(self):
        gate(False)
        HomeSection.objects.create(kind="intro", title="A focused approach")
        self.assertEqual(self.api.get("/api/home/").json()["sections"], [])


class SeoAndDepthTests(TestCase):
    def test_duplicate_titles_and_descriptions_are_reported(self):
        a = Service.objects.create(name="A", seo_title="Our Services", meta_description="Same")
        Sector.objects.create(name="B", seo_title="our services")
        self.assertEqual(len(seo_duplicates(a)), 1)

    def test_sector_without_questions_or_related_work_is_thin(self):
        sector = Sector.objects.create(name="Research & Studies")
        self.assertTrue(sector.is_thin)
        SectorFAQ.objects.create(sector=sector, question="q", answer="a")
        self.assertFalse(sector.is_thin)

    def test_service_and_sector_links_are_one_relation(self):
        service = Service.objects.create(name="PMO")
        sector = Sector.objects.create(name="Infrastructure")
        sector.related_services.add(service)
        self.assertEqual(list(service.related_sectors.all()), [sector])

    @mock.patch("apps.core.revalidate.queue")
    def test_sector_form_saves_related_services(self, _queue):
        from .admin import SectorForm

        service = Service.objects.create(name="PMO")
        sector = Sector.objects.create(name="Infrastructure")
        form = SectorForm(instance=sector)
        self.assertEqual(list(form.fields["related_services"].initial), [])
        sector.related_services.set([service])
        self.assertEqual(list(SectorForm(instance=sector).fields["related_services"].initial), [service])


class SeedContentTests(TestCase):
    """The content document loads cleanly, stays pending, and passes every content check."""

    @classmethod
    def setUpTestData(cls):
        from io import StringIO

        from django.core.management import call_command

        Service.objects.create(name="Construction Supervision", approval=APPROVED)
        Sector.objects.create(name="Energy", approval=APPROVED)
        with mock.patch("apps.core.revalidate.queue"):
            call_command("seed_content", stdout=StringIO())
            cls.second_run = StringIO()
            call_command("seed_content", stdout=cls.second_run)

    def test_exactly_the_documented_services_and_sectors(self):
        self.assertEqual(sorted(Service.objects.values_list("slug", flat=True)), [
            "business-development", "pmo-project-controls", "project-programme-management",
            "strategic-advisory-market-intelligence"])
        self.assertEqual(sorted(Sector.objects.values_list("slug", flat=True)), [
            "built-environment", "infrastructure", "research-studies", "urban-development-planning"])

    def test_everything_seeded_awaits_approval_with_arabic_unreviewed(self):
        from .models import ApproachStep, CompanyValue, Pillar, ValuePoint

        for model in (Service, Sector, Pillar, ApproachStep, CompanyValue, ValuePoint, Insight, HomeSection):
            with self.subTest(model=model.__name__):
                self.assertFalse(model.objects.filter(approval=APPROVED).exists())
                self.assertFalse(model.objects.filter(ar_reviewed=True).exists())
        self.assertFalse(Page.objects.filter(approval=APPROVED, slug__in=["about-us", "services", "contact"]).exists())
        self.assertEqual(SiteSettings.load().copy_approval, ApprovalStatus.PENDING)
        self.assertFalse(Project.objects.exists())

    def test_second_run_changes_nothing(self):
        rows = [line.split() for line in self.second_run.getvalue().splitlines()]
        table = [row for row in rows if len(row) > 5 and all(cell.isdigit() for cell in row[-5:])]
        self.assertTrue(table)
        self.assertEqual([row for row in table if row[-5:-2] != ["0", "0", "0"]], [])

    def test_pillar_three_is_proposed_and_services_link_both_ways(self):
        from .models import Pillar

        self.assertTrue(Pillar.objects.get(number=3).is_proposed)
        self.assertIn(Service.objects.get(slug="pmo-project-controls"),
                      Sector.objects.get(slug="infrastructure").related_services.all())

    def test_draft_topics_stay_hidden_with_pending_shown(self):
        gate(True)
        self.assertEqual(Insight.objects.filter(is_draft_topic=True).count(), 8)
        self.assertEqual(APIClient().get("/api/insights/").json()["count"], 0)

    def test_content_checks_pass(self):
        from . import quality

        self.assertEqual(quality.copy_mismatches(), [])
        self.assertEqual(quality.banned_terms(), [])
        self.assertEqual(quality.near_duplicates(), [])

    def test_near_duplicate_pages_are_caught(self):
        from . import quality

        text = "<p>" + " ".join(f"word{i}" for i in range(60)) + "</p>"
        Sector.objects.create(name="Copy A", intro=text)
        Sector.objects.create(name="Copy B", intro=text)
        self.assertEqual(len(quality.near_duplicates()), 1)

    def test_nothing_leaks_with_pending_hidden(self):
        gate(False)
        api = APIClient()
        self.assertEqual(api.get("/api/home/").json()["sections"], [])
        self.assertEqual(api.get("/api/services/").json(), [])
        self.assertEqual(api.get("/api/pillars/").json(), [])
        self.assertEqual(api.get("/api/site-settings/").json()["tagline"], "")
        header = api.get("/api/navigation/").json()["header"]
        self.assertEqual([item["label"] for item in header], ["Home"])
        paths = {entry["path"] for entry in api.get("/api/sitemap/").json()}
        self.assertTrue(paths <= {"/privacy/", "/terms/", "/cookies/", "/capability-statement/"}, paths)
