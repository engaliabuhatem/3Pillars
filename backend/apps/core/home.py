"""
The whole home page in one response: visible sections in the editor's order,
each with the content it shows.

A section with nothing approved to show (no logos, no testimonial) is dropped
here, so the site never renders an empty band.
"""

from .models import HomeSection, SiteSettings
from .serializers import HomeSectionSerializer, SiteSettingsSerializer


def _section_data(kind: str, context: dict):
    from apps.content import serializers as s
    from apps.content.models import KPI, Client, Insight, LifecycleStage, Pillar, Project, Sector, Service, Testimonial

    pending = context["include_pending"]
    visible = lambda model: model.objects.visible(include_pending=pending)  # noqa: E731

    match kind:
        case HomeSection.Kind.HERO:
            return SiteSettingsSerializer(SiteSettings.load(), context=context).data["hero"]
        case HomeSection.Kind.TRUST:
            logos = visible(Client).filter(show_in_trust_strip=True).exclude(logo="")
            return s.ClientSerializer(logos, many=True, context=context).data
        case HomeSection.Kind.PILLARS:
            return s.PillarSerializer(visible(Pillar)[:3], many=True, context=context).data
        case HomeSection.Kind.SERVICES:
            return s.ServiceCardSerializer(visible(Service).order_by("-featured", "order"), many=True, context=context).data
        case HomeSection.Kind.KPIS:
            return s.KPISerializer(visible(KPI), many=True, context=context).data
        case HomeSection.Kind.PROJECTS:
            featured = visible(Project).filter(featured=True).select_related("sector", "client")[:8]
            return s.ProjectCardSerializer(featured, many=True, context=context).data
        case HomeSection.Kind.APPROACH:
            return s.LifecycleStageSerializer(visible(LifecycleStage), many=True, context=context).data
        case HomeSection.Kind.SECTORS:
            return s.SectorCardSerializer(visible(Sector), many=True, context=context).data
        case HomeSection.Kind.TESTIMONIAL:
            quote = visible(Testimonial).select_related("project").first()
            return s.TestimonialSerializer(quote, context=context).data if quote else None
        case HomeSection.Kind.INSIGHTS:
            latest = visible(Insight).select_related("category")[:3]
            return s.InsightCardSerializer(latest, many=True, context=context).data
        case HomeSection.Kind.CTA:
            return SiteSettingsSerializer(SiteSettings.load(), context=context).data["capability_statement"] or {}
    return None


def build_home(context: dict) -> dict:
    sections = []
    for section in HomeSection.objects.filter(visible=True):
        data = _section_data(section.kind, context)
        if data in (None, []):
            continue
        sections.append({**HomeSectionSerializer(section, context=context).data, "data": data})
    return {"sections": sections}
