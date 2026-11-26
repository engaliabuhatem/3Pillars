"""SEO checks shared by the admin and the dashboard."""

from django.apps import apps
from django.db.models import Q

#: Every model that is a page of its own, as "app_label.Model".
PAGE_MODELS = ("core.Page", "content.Service", "content.Sector", "content.Project", "content.Insight", "careers.Job")

MISSING_SEO = Q(seo_title="") | Q(meta_description="") | Q(h1="")


def page_models():
    return [apps.get_model(label) for label in PAGE_MODELS]


def seo_duplicates(obj) -> list[str]:
    """Other pages using the same SEO title or meta description, as human-readable lines."""
    from .models import SiteSettings

    found = []
    for field, label in (("seo_title", "SEO title"), ("meta_description", "Meta description")):
        value = (getattr(obj, field, "") or "").strip()
        if not value:
            continue
        for model in page_models():
            clashes = model.objects.filter(**{f"{field}__iexact": value})
            if isinstance(obj, model):
                clashes = clashes.exclude(pk=obj.pk)
            found += [f"{label} also used by {model._meta.verbose_name} “{other}”" for other in clashes]
        home = SiteSettings.load()
        if (getattr(home, f"home_{field}", "") or "").strip().casefold() == value.casefold():
            found.append(f"{label} also used by the home page")
    return found
