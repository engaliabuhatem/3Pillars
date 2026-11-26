"""
`manage.py seed_content` — load the website content from the content document.

Idempotent and safe on a live database: rows are matched on a natural key
(slug, number, kind…) and updated in place. Any row whose content this command
changes goes back to "awaiting approval" with its Arabic marked unreviewed, so
nothing reaches the public site without an Approver. Rows from the earlier
placeholder content that this content replaces are deleted.
"""

import html
from collections import Counter, defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.content.models import (
    ApproachStep,
    CompanyValue,
    Insight,
    InsightCategory,
    Office,
    Pillar,
    Sector,
    SectorListItem,
    Service,
    ServiceBullet,
    ServiceCapability,
    ServiceStep,
    ValuePoint,
)
from apps.content.seed_data import content as c
from apps.core.fields import sanitize_html
from apps.core.models import (
    ApprovalStatus,
    FooterColumn,
    HomeSection,
    LaunchReadiness,
    LaunchReadinessItem,
    NavItem,
    Page,
    PageBlock,
    SiteSettings,
)

PENDING = ApprovalStatus.PENDING

#: English fields an editor would expect filled, per model; blanks are reported, never invented.
EXPECTED = {
    "Site settings": ("tagline", "home_h1", "hero_headline", "home_seo_title",
                      "home_meta_description", "consent_text"),
    "Home section": ("title", "intro"),
    "Pillar": ("name", "core_value", "summary", "detail", "core_outcomes", "covers"),
    "Service": ("name", "summary", "intro", "seo_title", "meta_description", "h1", "cta_headline", "cta_label"),
    "Sector": ("name", "focus_summary", "intro", "list_title", "seo_title", "meta_description", "h1"),
    "Page": ("title", "intro", "seo_title", "meta_description", "h1"),
}


def paragraphs(items: list[str]) -> str:
    return sanitize_html("".join(f"<p>{html.escape(text, quote=False)}</p>" for text in items))


class Tally:
    def __init__(self):
        self.counts: dict[str, Counter] = defaultdict(Counter)
        self.empty: dict[str, list[str]] = defaultdict(list)

    def add(self, label: str, outcome: str, n: int = 1):
        if n:
            self.counts[label][outcome] += n

    def check_empty(self, label: str, name: str, obj):
        for field in EXPECTED.get(label, ()):
            if not str(getattr(obj, field, "") or "").strip():
                self.empty[label].append(f"{name}.{field}")


def upsert(tally: Tally, label: str, model, lookup: dict, data: dict, *, gate: str | None = "approval"):
    """
    Create or update one row. A changed or new row goes back to pending with
    its Arabic unreviewed; an unchanged row keeps its approval.
    """
    obj = model.objects.filter(**lookup).first()
    created = obj is None
    if created:
        obj = model(**lookup)
    changed = created
    for field, value in data.items():
        if getattr(obj, field) != value:
            setattr(obj, field, value)
            changed = True
    if changed:
        if gate:
            setattr(obj, gate, PENDING)
        if hasattr(obj, "ar_reviewed"):
            obj.ar_reviewed = False
        obj.save()
    tally.add(label, "created" if created else "updated" if changed else "unchanged")
    return obj, changed


def replace_children(tally: Tally, label: str, manager, rows: list[dict]) -> bool:
    """Replace a parent's list rows when they differ; returns whether anything changed."""
    fields = list(rows[0]) if rows else []
    current = [{f: getattr(row, f) for f in fields} for row in manager.all()]
    if current == rows and manager.count() == len(rows):
        return False
    tally.add(label, "deleted", manager.all().delete()[0])
    for order, row in enumerate(rows):
        manager.create(order=order, **row)
    tally.add(label, "created", len(rows))
    return True


def delete(tally: Tally, label: str, queryset):
    tally.add(label, "deleted", queryset.delete()[1].get(queryset.model._meta.label, 0))


class Command(BaseCommand):
    help = "Load the website content from docs/content/3pillars-content.md (everything awaiting approval)."

    @transaction.atomic
    def handle(self, *args, **options):
        tally = Tally()
        self.site(tally)
        self.home(tally)
        services = self.services(tally)
        self.pillars(tally, services)
        self.sectors(tally, services)
        self.about(tally)
        self.pages(tally)
        self.navigation(tally)
        self.insights(tally)
        self.readiness(tally)
        delete(tally, "Office", Office.objects.filter(address__startswith="Placeholder"))
        self.report(tally)

    # ── Sections ─────────────────────────────────────────────────────────

    def site(self, tally):
        site = SiteSettings.load()
        data = {**c.SITE, **{field: "" for field in c.SITE_CLEARED}}
        changed = any(getattr(site, f) != v for f, v in data.items())
        if changed:
            for field, value in data.items():
                setattr(site, field, value)
            site.copy_approval = PENDING
            site.home_ar_reviewed = False
            site.save()
        tally.add("Site settings", "updated" if changed else "unchanged")
        tally.check_empty("Site settings", "site", site)

    def home(self, tally):
        kinds = []
        for order, row in enumerate(c.HOME_SECTIONS):
            data = {"order": order, "visible": row.get("visible", True), "eyebrow": "", "eyebrow_ar": "",
                    "title": "", "title_ar": "", "intro": "", "intro_ar": "", "cta_label": "", "cta_label_ar": "",
                    "cta_link": "", "secondary_label": "", "secondary_label_ar": "", "secondary_link": ""}
            data.update({k: v for k, v in row.items() if k not in ("kind", "visible")})
            section, _ = upsert(tally, "Home section", HomeSection, {"kind": row["kind"]}, data)
            if section.visible and section.kind not in ("hero", "pillars", "value"):
                tally.check_empty("Home section", section.kind, section)
            kinds.append(row["kind"])
        delete(tally, "Home section", HomeSection.objects.exclude(kind__in=kinds))

    def services(self, tally) -> dict[str, Service]:
        slugs = [row["slug"] for row in c.SERVICES]
        delete(tally, "Service", Service.objects.exclude(slug__in=slugs))
        result = {}
        for order, row in enumerate(c.SERVICES):
            lists = {"capabilities", "bullets", "steps", "intro", "intro_ar", "pillar"}
            data = {k: v for k, v in row.items() if k not in lists | {"slug"}}
            data.update(order=order, intro=paragraphs(row["intro"]), intro_ar=paragraphs(row["intro_ar"]))
            service, changed = upsert(tally, "Service", Service, {"slug": row["slug"]}, data)
            children = [
                replace_children(tally, "Service capability", service.capabilities, [
                    {"title": t, "title_ar": t_ar, "description": d, "description_ar": d_ar}
                    for t, t_ar, d, d_ar in row.get("capabilities", [])]),
                replace_children(tally, "Service bullet", service.bullets, [
                    {"text": t, "text_ar": t_ar} for t, t_ar in row.get("bullets", [])]),
                replace_children(tally, "Service step", service.steps, [
                    {"title": "", "title_ar": "", "body": b, "body_ar": b_ar} for b, b_ar in row.get("steps", [])]),
            ]
            if any(children) and not changed:
                Service.objects.filter(pk=service.pk).update(approval=PENDING, ar_reviewed=False)
            tally.check_empty("Service", row["slug"], service)
            result[row["slug"]] = service
        return result

    def pillars(self, tally, services):
        delete(tally, "Pillar", Pillar.objects.exclude(number__in=[p["number"] for p in c.PILLARS]))
        for row in c.PILLARS:
            data = {k: v for k, v in row.items() if k not in ("number", "service")}
            data.update(order=row["number"], service=services[row["service"]], note=row.get("note", ""))
            pillar, _ = upsert(tally, "Pillar", Pillar, {"number": row["number"]}, data)
            tally.check_empty("Pillar", str(row["number"]), pillar)
        for row in c.SERVICES:
            Service.objects.filter(slug=row["slug"]).update(pillar=Pillar.objects.get(number=row["pillar"]))

    def sectors(self, tally, services):
        slugs = [row["slug"] for row in c.SECTORS]
        delete(tally, "Sector", Sector.objects.exclude(slug__in=slugs))
        for order, row in enumerate(c.SECTORS):
            data = {k: v for k, v in row.items() if k not in ("slug", "list_items", "related_services", "intro", "intro_ar")}
            data.update(order=order, intro=paragraphs(row["intro"]), intro_ar=paragraphs(row["intro_ar"]))
            sector, changed = upsert(tally, "Sector", Sector, {"slug": row["slug"]}, data)
            items = replace_children(tally, "Sector list item", sector.list_items,
                                     [{"text": t, "text_ar": t_ar} for t, t_ar in row["list_items"]])
            wanted = {services[slug].pk for slug in row["related_services"]}
            relinked = set(sector.related_services.values_list("pk", flat=True)) != wanted
            if relinked:
                sector.related_services.set(wanted)
            if (items or relinked) and not changed:
                Sector.objects.filter(pk=sector.pk).update(approval=PENDING, ar_reviewed=False)
            tally.check_empty("Sector", row["slug"], sector)

    def about(self, tally):
        for model, label, key, rows in (
            (CompanyValue, "Company value", "value",
             [{"value": v, "value_ar": v_ar, "in_practice": p, "in_practice_ar": p_ar}
              for v, v_ar, p, p_ar in c.COMPANY_VALUES]),
            (ApproachStep, "Approach step", "name",
             [{"name": n, "name_ar": n_ar, "summary": s, "summary_ar": s_ar} for n, n_ar, s, s_ar in c.APPROACH_STEPS]),
            (ValuePoint, "Value point", "title", c.VALUE_POINTS),
        ):
            delete(tally, label, model.objects.exclude(**{f"{key}__in": [row[key] for row in rows]}))
            for order, row in enumerate(rows):
                upsert(tally, label, model, {key: row[key]}, {**row, "order": order})

    def pages(self, tally):
        delete(tally, "Page", Page.objects.filter(slug__in=c.RETIRED_PAGES))
        for row in c.PAGES:
            blocks = row.get("blocks", [])
            data = {"title": "", "title_ar": "", "intro": "", "intro_ar": "", "eyebrow": "", "eyebrow_ar": "",
                    "seo_title": "", "seo_title_ar": "", "meta_description": "", "meta_description_ar": "", "h1": "",
                    "h1_ar": "", "primary_keyword": "", "supporting_keywords": "", "cta_label": "", "cta_label_ar": "",
                    "note": "", "path": None}
            data.update({k: v for k, v in row.items() if k not in ("slug", "blocks")})
            page, changed = upsert(tally, "Page", Page, {"slug": row["slug"]}, data)
            wanted = [{
                "kind": b["kind"], "visible": b.get("visible", True), "title": b.get("title", ""),
                "title_ar": b.get("title_ar", ""), "body": paragraphs(b.get("body", [])),
                "body_ar": paragraphs(b.get("body_ar", [])), "note": b.get("note", ""),
            } for b in blocks]
            if replace_children(tally, "Page block", page.blocks, wanted) and not changed:
                Page.objects.filter(pk=page.pk).update(approval=PENDING, ar_reviewed=False)
            tally.check_empty("Page", row["slug"], page)

    def navigation(self, tally):
        keep = []
        for order, row in enumerate(c.HEADER_NAV):
            parent, _ = upsert(tally, "Navigation item", NavItem, {"menu": NavItem.Menu.HEADER, "parent": None,
                                                                   "link": row["link"]},
                               self.nav_data(row, order), gate=None)
            keep.append(parent.pk)
            for child_order, child in enumerate(row.get("children", [])):
                item, _ = upsert(tally, "Navigation item", NavItem, {"menu": NavItem.Menu.HEADER, "parent": parent,
                                                                     "link": child["link"]},
                                 self.nav_data(child, child_order), gate=None)
                keep.append(item.pk)
        for col_order, (title, title_ar, links) in enumerate(c.FOOTER):
            column, _ = upsert(tally, "Footer column", FooterColumn, {"title": title},
                               {"title_ar": title_ar, "order": col_order}, gate=None)
            for order, (label, label_ar, link) in enumerate(links):
                item, _ = upsert(tally, "Navigation item", NavItem,
                                 {"menu": NavItem.Menu.FOOTER, "column": column, "link": link},
                                 {"label": label, "label_ar": label_ar, "order": order}, gate=None)
                keep.append(item.pk)
        for old, new in c.LEGAL_LINKS.items():
            NavItem.objects.filter(menu=NavItem.Menu.LEGAL, link=old).update(link=new)
        keep += NavItem.objects.filter(menu=NavItem.Menu.LEGAL).values_list("pk", flat=True)
        delete(tally, "Navigation item", NavItem.objects.exclude(pk__in=keep))
        delete(tally, "Footer column", FooterColumn.objects.exclude(title__in=[col[0] for col in c.FOOTER]))

    @staticmethod
    def nav_data(row: dict, order: int) -> dict:
        return {"label": row["label"], "label_ar": row["label_ar"], "order": order,
                "mega_menu": row.get("mega_menu", ""), "visible": row.get("visible", True),
                "is_cta": row.get("is_cta", False)}

    def insights(self, tally):
        slugs = [slug for slug, *_ in c.INSIGHT_CATEGORIES]
        delete(tally, "Insight category", InsightCategory.objects.exclude(slug__in=slugs))
        for order, (slug, name, name_ar) in enumerate(c.INSIGHT_CATEGORIES):
            upsert(tally, "Insight category", InsightCategory, {"slug": slug},
                   {"name": name, "name_ar": name_ar, "order": order}, gate=None)
        for title, title_ar in c.DRAFT_TOPICS:
            upsert(tally, "Draft article topic", Insight, {"title": title, "is_draft_topic": True},
                   {"title_ar": title_ar, "kind": Insight.Kind.ARTICLE, "published_at": None})

    def readiness(self, tally):
        readiness = LaunchReadiness.load()
        rows = [(LaunchReadinessItem.Kind.CLAIM, item, req) for item, req in c.CLAIMS_TO_VERIFY]
        rows += [(LaunchReadinessItem.Kind.CHECKLIST, item, "") for item in c.PRE_LAUNCH_CHECKLIST]
        for order, (kind, item, requirement) in enumerate(rows):
            # Status, owner and notes belong to the team: only the wording is loaded.
            upsert(tally, "Launch readiness item", LaunchReadinessItem,
                   {"readiness": readiness, "kind": kind, "item": item},
                   {"requirement": requirement, "order": order}, gate=None)

    # ── Output ───────────────────────────────────────────────────────────

    def report(self, tally):
        header = f"{'Model':<24}{'Created':>9}{'Updated':>9}{'Deleted':>9}{'Unchanged':>11}{'Empty':>7}"
        self.stdout.write(header)
        self.stdout.write("-" * len(header))
        for label in sorted(set(tally.counts) | set(tally.empty)):
            n = tally.counts[label]
            self.stdout.write(f"{label:<24}{n['created']:>9}{n['updated']:>9}{n['deleted']:>9}{n['unchanged']:>11}"
                              f"{len(tally.empty[label]):>7}")
        if any(tally.empty.values()):
            self.stdout.write("\nFields left empty because the content document does not provide them:")
            for label, fields in sorted(tally.empty.items()):
                for field in fields:
                    self.stdout.write(f"  {label}: {field}")
        self.stdout.write(self.style.SUCCESS(
            "\nContent loaded. Everything new or changed is awaiting approval, with its Arabic marked unreviewed."
        ))
