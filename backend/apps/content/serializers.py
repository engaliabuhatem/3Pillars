import re

from rest_framework import serializers

from apps.core.images import file_payload
from apps.core.serializers import LocalizedSerializer, SeoMixin, gated

from .models import (
    KPI,
    ApproachStep,
    Certification,
    Client,
    CompanyValue,
    Download,
    Insight,
    InsightCategory,
    Office,
    Pillar,
    Project,
    ProjectImage,
    ProjectMetric,
    Sector,
    SectorFAQ,
    SectorListItem,
    Service,
    ServiceBullet,
    ServiceCapability,
    ServiceFAQ,
    ServiceStep,
    TeamMember,
    Testimonial,
    ValuePoint,
)


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
    service = serializers.SerializerMethodField()

    class Meta:
        model = Pillar
        fields = ["id", "number", "name", "role_on_site", "color", "core_value", "summary", "detail",
                  "core_outcomes", "covers", "is_proposed", "service"]

    def get_service(self, obj):
        service = obj.service
        if not service or not (service.is_approved or self.context.get("include_pending")):
            return None
        return ServiceRefSerializer(service, context=self.context).data


class ValuePointSerializer(LocalizedSerializer):
    class Meta:
        model = ValuePoint
        fields = ["id", "title", "body"]


class CompanyValueSerializer(LocalizedSerializer):
    class Meta:
        model = CompanyValue
        fields = ["id", "value", "in_practice"]


class ApproachStepSerializer(LocalizedSerializer):
    class Meta:
        model = ApproachStep
        fields = ["id", "name", "summary"]


class KPISerializer(LocalizedSerializer):
    value = serializers.FloatField()

    class Meta:
        model = KPI
        fields = ["id", "value", "prefix", "suffix", "label", "source"]


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


class ServiceCapabilitySerializer(LocalizedSerializer):
    class Meta:
        model = ServiceCapability
        fields = ["title", "description"]


class ServiceBulletSerializer(LocalizedSerializer):
    class Meta:
        model = ServiceBullet
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
    pillar = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ["slug", "name", "icon", "summary", "pillar"]

    def get_pillar(self, obj):
        pillar = obj.pillar
        if not pillar or not (pillar.is_approved or self.context.get("include_pending")):
            return None
        return {"number": pillar.number, "color": pillar.color, "is_proposed": pillar.is_proposed}


class SectorCardSerializer(LocalizedSerializer):
    image_fields = ("image",)

    class Meta:
        model = Sector
        fields = ["slug", "name", "icon", "focus_summary"]


class ServiceSerializer(SeoMixin, ServiceCardSerializer):
    capabilities = ServiceCapabilitySerializer(many=True, read_only=True)
    bullets = ServiceBulletSerializer(many=True, read_only=True)
    steps = ServiceStepSerializer(many=True, read_only=True)
    faqs = ServiceFAQSerializer(many=True, read_only=True)
    related_sectors = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    class Meta(ServiceCardSerializer.Meta):
        fields = [*ServiceCardSerializer.Meta.fields, "intro", "capabilities_title", "capabilities", "bullets_title",
                  "bullets", "scope_caveat", "steps_title", "steps", "context_title", "context_body",
                  "who_we_support", "faqs", "related_sectors", "projects", "cta_headline", "cta_label", "seo",
                  "updated_at"]

    def get_related_sectors(self, obj):
        sectors = gated(obj.related_sectors.all(), self.context)
        return SectorCardSerializer(sectors, many=True, context=self.context).data

    def get_projects(self, obj):
        projects = gated(obj.projects.all(), self.context)[:3]
        return ProjectCardSerializer(projects, many=True, context=self.context).data


class SectorListItemSerializer(LocalizedSerializer):
    class Meta:
        model = SectorListItem
        fields = ["text"]


class SectorFAQSerializer(LocalizedSerializer):
    class Meta:
        model = SectorFAQ
        fields = ["question", "answer"]


class SectorSerializer(SeoMixin, SectorCardSerializer):
    list_items = SectorListItemSerializer(many=True, read_only=True)
    faqs = SectorFAQSerializer(many=True, read_only=True)
    related_services = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    insights = serializers.SerializerMethodField()

    class Meta(SectorCardSerializer.Meta):
        fields = [*SectorCardSerializer.Meta.fields, "intro", "list_title", "list_items", "scope_caveat", "our_focus",
                  "related_services", "projects", "insights", "faqs", "seo", "updated_at"]

    def get_related_services(self, obj):
        services = gated(obj.related_services.select_related("pillar"), self.context)
        return ServiceCardSerializer(services, many=True, context=self.context).data

    def get_projects(self, obj):
        projects = gated(obj.projects.all(), self.context)[:6]
        return ProjectCardSerializer(projects, many=True, context=self.context).data

    def get_insights(self, obj):
        insights = Insight.objects.filter(sectors=obj).visible(include_pending=self.context.get("include_pending"))
        return InsightCardSerializer(insights.select_related("category")[:3], many=True, context=self.context).data


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
    our_role = serializers.CharField(source="get_our_role_display")

    class Meta:
        model = Project
        fields = ["slug", "title", "entry_type", "summary", "location", "country", "status", "sector", "client",
                  "delivery_entity", "our_role", "featured"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["role_key"] = instance.our_role
        return data

    def get_sector(self, obj):
        if obj.sector and (obj.sector.is_approved or self.context.get("include_pending")):
            return SectorRefSerializer(obj.sector, context=self.context).data
        return None

    def get_client(self, obj):
        """A client is named only with their agreement; the public name wins over the record's name."""
        if not obj.client_name_approved:
            return None
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
        fields = [*ProjectCardSerializer.Meta.fields, "our_role_detail", "challenge", "scope_of_services", "approach",
                  "results", "services", "metrics", "gallery", "facts", "related", "seo", "updated_at"]

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
        fields = ["slug", "title", "kind", "excerpt", "category", "author", "published_at", "reading_minutes"]

    def get_reading_minutes(self, obj):
        body = obj.body_ar if self.locale == "ar" and obj.body_ar else obj.body
        words = len(re.sub(r"<[^>]+>", " ", body or "").split())
        return max(1, round(words / 220))


class InsightSerializer(SeoMixin, InsightCardSerializer):
    class Meta(InsightCardSerializer.Meta):
        fields = [*InsightCardSerializer.Meta.fields, "body", "our_role_statement", "seo", "updated_at"]


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
