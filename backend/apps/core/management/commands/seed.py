"""
`manage.py seed` — create the placeholder structure of a fresh site.

Safe to run again: it only creates what is missing and never touches a row an
editor has already changed or approved.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.content.models import InsightCategory, LifecycleStage, Office, Pillar, Sector, Service, ServiceDeliverable, ServiceStep
from apps.core import seed_data as d
from apps.core.models import FooterColumn, HomeSection, NavItem, Page, PageBlock, SiteSettings


class Command(BaseCommand):
    help = "Create placeholder site structure (everything pending approval)."

    @transaction.atomic
    def handle(self, *args, **options):
        settings = SiteSettings.load()
        for field, value in d.SETTINGS.items():
            if not getattr(settings, field):
                setattr(settings, field, value)
        settings.save()

        for order, (kind, eyebrow, eyebrow_ar, title, title_ar) in enumerate(d.HOME_SECTIONS):
            HomeSection.objects.get_or_create(kind=kind, defaults={
                "order": order, "eyebrow": eyebrow, "eyebrow_ar": eyebrow_ar, "title": title, "title_ar": title_ar,
                "cta_label": "Request a proposal" if kind == "cta" else "",
                "cta_label_ar": "اطلب عرضاً" if kind == "cta" else "",
                "cta_link": "/request-a-proposal" if kind == "cta" else "",
                "secondary_label": "Download capability statement" if kind == "cta" else "",
                "secondary_label_ar": "حمّل ملف القدرات" if kind == "cta" else "",
                "secondary_link": "/capability-statement" if kind == "cta" else "",
            })

        for order, (color, name, name_ar, icon, summary, summary_ar) in enumerate(d.PILLARS):
            Pillar.objects.get_or_create(color=color, defaults={
                "order": order, "name": name, "name_ar": name_ar, "icon": icon,
                "summary": summary, "summary_ar": summary_ar,
                "detail": f"{d.P}the client defines what this pillar means for 3 Pillars.",
                "detail_ar": f"{d.P_AR}يحدد العميل معنى هذه الركيزة.",
            })

        sectors = []
        for order, (name, name_ar, icon, summary, summary_ar) in enumerate(d.SECTORS):
            sector, _ = Sector.objects.get_or_create(name=name, defaults={
                "order": order, "name_ar": name_ar, "icon": icon, "summary": summary, "summary_ar": summary_ar,
                "intro": f"<p>{d.P}describe this sector and 3 Pillars’ role in it.</p>",
                "intro_ar": f"<p>{d.P_AR}وصف القطاع ودور الشركة فيه.</p>",
            })
            sectors.append(sector)

        for order, (name, name_ar, icon, featured, summary, summary_ar) in enumerate(d.SERVICES):
            service, created = Service.objects.get_or_create(name=name, defaults={
                "order": order, "name_ar": name_ar, "icon": icon, "featured": featured,
                "summary": summary, "summary_ar": summary_ar,
                "overview": f"<p>{d.P}an overview of this service, written with the client.</p>",
                "overview_ar": f"<p>{d.P_AR}نبذة عن الخدمة تُكتب مع العميل.</p>",
            })
            if created and featured:
                service.sectors.set(sectors)
                for i, (text, text_ar) in enumerate(d.PMC_DELIVERABLES):
                    ServiceDeliverable.objects.create(service=service, order=i, text=text, text_ar=text_ar)
                for i, (title, title_ar, body, body_ar) in enumerate(d.PMC_STEPS):
                    ServiceStep.objects.create(service=service, order=i, title=title, title_ar=title_ar,
                                               body=body, body_ar=body_ar)

        for order, (name, name_ar, icon, summary, summary_ar, deliverables, deliverables_ar) in enumerate(d.LIFECYCLE):
            LifecycleStage.objects.get_or_create(name=name, defaults={
                "order": order, "name_ar": name_ar, "icon": icon, "summary": summary, "summary_ar": summary_ar,
                "deliverables": deliverables, "deliverables_ar": deliverables_ar,
            })

        for order, (slug, title, title_ar, eyebrow, eyebrow_ar) in enumerate(d.PAGES):
            page, created = Page.objects.get_or_create(slug=slug, defaults={
                "order": order, "title": title, "title_ar": title_ar, "eyebrow": eyebrow, "eyebrow_ar": eyebrow_ar,
                "intro": f"{d.P}introduction for the {title.lower()} page.",
                "intro_ar": f"{d.P_AR}مقدمة صفحة {title_ar}.",
            })
            if created:
                PageBlock.objects.create(page=page, kind=PageBlock.Kind.RICH_TEXT,
                                         body=f"<p>{d.P}content to be supplied and approved by the client.</p>",
                                         body_ar=f"<p>{d.P_AR}محتوى يزوده العميل ويعتمده.</p>")

        Office.objects.get_or_create(city="Aden", defaults={
            "city_ar": "عدن", "country": "Yemen", "country_ar": "اليمن", "is_headquarters": True,
            "address": f"{d.P}street address to be confirmed.", "address_ar": f"{d.P_AR}العنوان قيد التأكيد.",
        })

        if not NavItem.objects.exists():
            for order, (label, label_ar, link, mega) in enumerate(d.HEADER_NAV):
                NavItem.objects.create(menu=NavItem.Menu.HEADER, order=order, label=label, label_ar=label_ar,
                                       link=link, mega_menu=mega)
            for col_order, (title, title_ar, links) in enumerate(d.FOOTER):
                column = FooterColumn.objects.create(order=col_order, title=title, title_ar=title_ar)
                for order, (label, label_ar, link) in enumerate(links):
                    NavItem.objects.create(menu=NavItem.Menu.FOOTER, column=column, order=order,
                                           label=label, label_ar=label_ar, link=link)
            for order, (label, label_ar, link) in enumerate(d.LEGAL):
                NavItem.objects.create(menu=NavItem.Menu.LEGAL, order=order, label=label, label_ar=label_ar, link=link)

        for order, (name, name_ar, slug) in enumerate(d.INSIGHT_CATEGORIES):
            InsightCategory.objects.get_or_create(slug=slug, defaults={"order": order, "name": name, "name_ar": name_ar})

        self.stdout.write(self.style.SUCCESS(
            "Placeholder structure ready. Everything is awaiting approval; nothing is public until approved."
        ))
