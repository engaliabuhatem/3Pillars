import re

from rest_framework import serializers

from apps.core.images import file_payload
from apps.core.serializers import LocalizedSerializer, SeoMixin, gated

from .models import (
    KPI,
    Certification,
    Client,
    Download,
    Insight,
    InsightCategory,
    LifecycleStage,
    Office,
    Pillar,
    Project,
    ProjectImage,
    ProjectMetric,
    Sector,
    Service,
    ServiceDeliverable,
    ServiceFAQ,
    ServiceStep,
    TeamMember,
    Testimonial,
)


def lines(value: str) -> list[str]:
    return [line.strip() for line in (value or "").splitlines() if line.strip()]


class RefSerializer(LocalizedSerializer):
    """The minimum needed to link to something: slug + name."""

    class Meta:
        fields = ["slug", "name"]


class SectorRefSerializer(RefSerializer):
    class Meta(RefSerializer.Meta):
        model = Sector


class ServiceRefSerializer(RefSerializer):
    class Meta(RefSerializer.Meta):
        model = Service
        fields = ["slug", "name", "icon"]


class PillarSerializer(LocalizedSerializer):
    class Meta:
        model = Pillar
        fields = ["id", "name", "color", "icon", "summary", "detail"]


class KPISerializer(LocalizedSerializer):
    value = serializers.FloatField()

    class Meta:
        model = KPI
        fields = ["id", "value", "prefix", "suffix", "label", "source"]


class LifecycleStageSerializer(LocalizedSerializer):
    deliverables = serializers.SerializerMethodField()

    class Meta:
        model = LifecycleStage
        fields = ["id", "name", "icon", "summary", "deliverables"]

    def get_deliverables(self, obj):
        return lines(obj.deliverables_ar if self.locale == "ar" and obj.deliverables_ar else obj.deliverables)


class ClientSerializer(LocalizedSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["id", "name", "kind", "website", "logo"]

    def get_logo(self, obj):
        return file_payload(obj, "logo", request=self.context.get("request"))


class TestimonialSerializer(LocalizedSerializer):
    image_fields = ("photo",)
    project = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ["id", "quote", "person", "role", "company", "project"]

    def get_project(self, obj):
        project = obj.project
        if not project or not (project.is_approved or self.context.get("include_pending")):
            return None
        title = (project.title_ar if self.locale == "ar" else "") or project.title
        return {"slug": project.slug, "title": title}


# ── Services and sectors ─────────────────────────────────────────────────


class ServiceDeliverableSerializer(LocalizedSerializer):
    class Meta:
        model = ServiceDeliverable
        fields = ["text"]


class ServiceStepSerializer(LocalizedSerializer):
    class Meta:
        model = ServiceStep
        fields = ["title", "body"]


class ServiceFAQSerializer(LocalizedSerializer):
    class Meta:
        model = ServiceFAQ
        fields = ["question", "answer"]


class ServiceCardSerializer(LocalizedSerializer):
    image_fields = ("image",)

    class Meta:
        model = Service
        fields = ["slug", "name", "icon", "summary", "featured"]


class ServiceSerializer(SeoMixin, ServiceCardSerializer):
    deliverables = ServiceDeliverableSerializer(many=True, read_only=True)
    steps = ServiceStepSerializer(many=True, read_only=True)
    faqs = ServiceFAQSerializer(many=True, read_only=True)
    sectors = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    class Meta(ServiceCardSerializer.Meta):
        fields = [*ServiceCardSerializer.Meta.fields, "overview", "deliverables", "steps", "faqs",
                  "sectors", "projects", "seo", "updated_at"]

    def get_sectors(self, obj):
        return SectorRefSerializer(gated(obj.sectors.all(), self.context), many=True, context=self.context).data

    def get_projects(self, obj):
        projects = gated(obj.projects.all(), self.context)[:3]
        return ProjectCardSerializer(projects, many=True, context=self.context).data


class SectorCardSerializer(LocalizedSerializer):
    image_fields = ("image",)

    class Meta:
        model = Sector
        fields = ["slug", "name", "icon", "summary"]


class SectorSerializer(SeoMixin, SectorCardSerializer):
    services = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    class Meta(SectorCardSerializer.Meta):
        fields = [*SectorCardSerializer.Meta.fields, "intro", "services", "projects", "seo", "updated_at"]

    def get_services(self, obj):
        return ServiceCardSerializer(gated(obj.services.all(), self.context), many=True, context=self.context).data

    def get_projects(self, obj):
        projects = gated(obj.projects.all(), self.context)[:6]
        return ProjectCardSerializer(projects, many=True, context=self.context).data


# ── Projects ─────────────────────────────────────────────────────────────


class ProjectMetricSerializer(LocalizedSerializer):
    class Meta:
        model = ProjectMetric
        fields = ["label", "value", "unit", "delta"]


class ProjectImageSerializer(LocalizedSerializer):
    image_fields = ("image",)

    class Meta:
        model = ProjectImage
        fields = ["caption"]


class ProjectCardSerializer(LocalizedSerializer):
    image_fields = ("image",)
    sector = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["slug", "title", "summary", "location", "country", "status", "sector", "client", "featured"]

    def get_sector(self, obj):
        if obj.sector and (obj.sector.is_approved or self.context.get("include_pending")):
            return SectorRefSerializer(obj.sector, context=self.context).data
        return None

    def get_client(self, obj):
        """The public name wins; a client's own name only once the client row is approved."""
        ar = self.locale == "ar"
        public = (obj.client_public_name_ar if ar else "") or obj.client_public_name
        if public:
            return public
        if obj.client and (obj.client.is_approved or self.context.get("include_pending")):
            return (obj.client.name_ar if ar else "") or obj.client.name
        return None


class ProjectSerializer(SeoMixin, ProjectCardSerializer):
    services = serializers.SerializerMethodField()
    metrics = ProjectMetricSerializer(many=True, read_only=True)
    gallery = ProjectImageSerializer(many=True, read_only=True)
    facts = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()

    class Meta(ProjectCardSerializer.Meta):
        fields = [*ProjectCardSerializer.Meta.fields, "role", "challenge", "approach", "outcome",
                  "services", "metrics", "gallery", "facts", "related", "seo", "updated_at"]

    def get_services(self, obj):
        return ServiceRefSerializer(gated(obj.services.all(), self.context), many=True, context=self.context).data

    def get_facts(self, obj):
        return {
            "value": {"amount": float(obj.value), "currency": obj.currency}
            if obj.show_value and obj.value is not None else None,
            "start": obj.start_date,
            "end": obj.end_date,
            "duration_months": obj.duration_months,
        }

    def get_related(self, obj):
        qs = gated(Project.objects.exclude(pk=obj.pk), self.context)
        if obj.sector_id:
            qs = qs.filter(sector_id=obj.sector_id)
        return ProjectCardSerializer(qs.select_related("sector", "client")[:3], many=True, context=self.context).data


# ── People, places, proof ────────────────────────────────────────────────


class TeamMemberSerializer(LocalizedSerializer):
    image_fields = ("photo",)

    class Meta:
        model = TeamMember
        fields = ["id", "name", "role", "bio", "linkedin", "leadership"]


class OfficeSerializer(LocalizedSerializer):
    image_fields = ("map_image",)
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Office
        fields = ["id", "city", "country", "address", "phone", "email", "is_headquarters", "coordinates"]

    def get_coordinates(self, obj):
        if obj.latitude is None or obj.longitude is None:
            return None
        return {"lat": float(obj.latitude), "lng": float(obj.longitude)}


class CertificationSerializer(LocalizedSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = ["id", "name", "issuer", "kind", "year", "logo"]

    def get_logo(self, obj):
        return file_payload(obj, "logo", request=self.context.get("request"))


# ── Insights and downloads ───────────────────────────────────────────────


class InsightCategorySerializer(LocalizedSerializer):
    class Meta:
        model = InsightCategory
        fields = ["slug", "name"]


class InsightCardSerializer(LocalizedSerializer):
    image_fields = ("image",)
    category = InsightCategorySerializer(read_only=True)
    reading_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Insight
        fields = ["slug", "title", "excerpt", "category", "author", "published_at", "reading_minutes"]

    def get_reading_minutes(self, obj):
        body = obj.body_ar if self.locale == "ar" and obj.body_ar else obj.body
        words = len(re.sub(r"<[^>]+>", " ", body or "").split())
        return max(1, round(words / 220))


class InsightSerializer(SeoMixin, InsightCardSerializer):
    class Meta(InsightCardSerializer.Meta):
        fields = [*InsightCardSerializer.Meta.fields, "body", "seo", "updated_at"]


class DownloadSerializer(LocalizedSerializer):
    file = serializers.SerializerMethodField()
    gated = serializers.SerializerMethodField()

    class Meta:
        model = Download
        fields = ["id", "slug", "title", "description", "gated", "is_capability_statement", "file"]

    def get_gated(self, obj):
        return obj.requires_lead()

    def get_file(self, obj):
        # A gated file's address is only handed out after the lead is captured.
        if obj.requires_lead():
            return None
        field = "file_ar" if self.locale == "ar" and obj.file_ar else "file"
        return file_payload(obj, field, request=self.context.get("request"))
