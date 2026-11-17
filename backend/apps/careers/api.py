from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.response import Response

from apps.bd.services import SpamCheckMixin, notify
from apps.bd.views import FormView
from apps.core.api import GatedReadOnlyViewSet
from apps.core.serializers import LocalizedSerializer, SeoMixin

from .models import Application, Job


class JobCardSerializer(LocalizedSerializer):
    employment_type = serializers.CharField(source="get_employment_type_display")

    class Meta:
        model = Job
        fields = ["slug", "title", "location", "employment_type", "summary", "is_open", "posted_at", "closes_at"]


class JobSerializer(SeoMixin, JobCardSerializer):
    class Meta(JobCardSerializer.Meta):
        fields = [*JobCardSerializer.Meta.fields, "description", "seo", "updated_at"]


class JobViewSet(GatedReadOnlyViewSet):
    model = Job
    pagination_class = None

    def get_serializer_class(self):
        return JobSerializer if self.action == "retrieve" else JobCardSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs if self.action == "retrieve" else qs.filter(is_open=True)


class ApplicationSerializer(SpamCheckMixin, serializers.ModelSerializer):
    job = serializers.SlugRelatedField(slug_field="slug", queryset=Job.objects.approved().filter(is_open=True),
                                       required=False, allow_null=True)
    consent = serializers.BooleanField()

    class Meta:
        model = Application
        fields = ["job", "name", "email", "phone", "linkedin", "cover_note", "cv", "consent", "locale",
                  "website", "turnstile_token"]

    def validate_consent(self, value):
        if not value:
            raise serializers.ValidationError("Please agree to the privacy notice so we can review your application.")
        return value

    def create(self, validated):
        validated["cv_original_name"] = validated["cv"].name[:200]
        return super().create(validated)


class ApplicationCreateView(FormView):
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        notify("application", application, admin_path=reverse("admin:careers_application_change", args=[application.pk]),
               summary=f"{application.name} — {application.job or 'open application'}")
        return Response({"ok": True}, status=status.HTTP_201_CREATED)
