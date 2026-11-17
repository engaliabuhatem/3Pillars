import django_filters
from django.db.models import Prefetch
from rest_framework.response import Response

from apps.core.api import GatedReadOnlyViewSet

from . import serializers as s
from .models import (
    Certification,
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
    TeamMember,
)


class ServiceViewSet(GatedReadOnlyViewSet):
    model = Service
    pagination_class = None

    def get_serializer_class(self):
        return s.ServiceSerializer if self.action == "retrieve" else s.ServiceCardSerializer

    def base_queryset(self):
        qs = Service.objects.all()
        if self.action == "retrieve":
            qs = qs.prefetch_related("deliverables", "steps", "faqs", "sectors", "projects__sector", "projects__client")
        return qs


class SectorViewSet(GatedReadOnlyViewSet):
    model = Sector
    pagination_class = None

    def get_serializer_class(self):
        return s.SectorSerializer if self.action == "retrieve" else s.SectorCardSerializer

    def base_queryset(self):
        qs = Sector.objects.all()
        if self.action == "retrieve":
            qs = qs.prefetch_related("services", "projects__sector", "projects__client")
        return qs


class ProjectFilter(django_filters.FilterSet):
    sector = django_filters.CharFilter(field_name="sector__slug")
    service = django_filters.CharFilter(field_name="services__slug")
    country = django_filters.CharFilter(field_name="country", lookup_expr="iexact")
    status = django_filters.ChoiceFilter(choices=Project.Status.choices)
    featured = django_filters.BooleanFilter()

    class Meta:
        model = Project
        fields = ["sector", "service", "country", "status", "featured"]


class ProjectViewSet(GatedReadOnlyViewSet):
    model = Project
    filterset_class = ProjectFilter

    def get_serializer_class(self):
        return s.ProjectSerializer if self.action == "retrieve" else s.ProjectCardSerializer

    def base_queryset(self):
        qs = Project.objects.select_related("sector", "client")
        if self.action == "retrieve":
            qs = qs.prefetch_related(
                "services",
                Prefetch("metrics", queryset=ProjectMetric.objects.all()),
                Prefetch("gallery", queryset=ProjectImage.objects.all()),
            )
        return qs.distinct()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # The filter bar needs every option that has at least one visible project.
        visible = self.get_queryset()
        response.data["facets"] = {
            "countries": sorted({c for c in visible.values_list("country", flat=True) if c}),
            "sectors": s.SectorRefSerializer(
                Sector.objects.filter(projects__in=visible).distinct().visible(include_pending=self.include_pending),
                many=True, context=self.get_serializer_context(),
            ).data,
            "services": s.ServiceRefSerializer(
                Service.objects.filter(projects__in=visible).distinct().visible(include_pending=self.include_pending),
                many=True, context=self.get_serializer_context(),
            ).data,
        }
        return response


class InsightViewSet(GatedReadOnlyViewSet):
    model = Insight
    filterset_fields = {"category__slug": ["exact"]}

    def get_serializer_class(self):
        return s.InsightSerializer if self.action == "retrieve" else s.InsightCardSerializer

    def base_queryset(self):
        return Insight.objects.select_related("category")

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["categories"] = s.InsightCategorySerializer(
            InsightCategory.objects.all(), many=True, context=self.get_serializer_context()
        ).data
        return response


class TeamViewSet(GatedReadOnlyViewSet):
    model = TeamMember
    serializer_class = s.TeamMemberSerializer
    pagination_class = None
    lookup_field = "pk"


class OfficeViewSet(GatedReadOnlyViewSet):
    model = Office
    serializer_class = s.OfficeSerializer
    pagination_class = None
    lookup_field = "pk"


class CertificationViewSet(GatedReadOnlyViewSet):
    model = Certification
    serializer_class = s.CertificationSerializer
    pagination_class = None
    lookup_field = "pk"


class DownloadViewSet(GatedReadOnlyViewSet):
    model = Download
    serializer_class = s.DownloadSerializer
    pagination_class = None
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_object()).data)


class PillarViewSet(GatedReadOnlyViewSet):
    model = Pillar
    serializer_class = s.PillarSerializer
    pagination_class = None
    lookup_field = "pk"


class LifecycleStageViewSet(GatedReadOnlyViewSet):
    model = LifecycleStage
    serializer_class = s.LifecycleStageSerializer
    pagination_class = None
    lookup_field = "pk"
