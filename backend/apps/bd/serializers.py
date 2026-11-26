from django.utils import timezone
from rest_framework import serializers

from apps.content.models import Download, Sector, Service
from apps.core.models import SiteSettings

from .models import AreaOfInterest, DownloadLead, Enquiry, ProposalAttachment, ProposalRequest
from .services import SpamCheckMixin

TRACKING = ["locale", "source_page", "utm_source", "utm_medium", "utm_campaign"]


class ConsentMixin(serializers.Serializer):
    """Records exactly which consent wording the sender agreed to, and when."""

    consent = serializers.BooleanField()

    def validate_consent(self, value):
        if not value:
            raise serializers.ValidationError("Please agree to be contacted so we can reply.")
        return value

    def create(self, validated):
        site = SiteSettings.load()
        arabic = validated.get("locale") == "ar"
        validated["consent_text"] = (site.consent_text_ar if arabic else "") or site.consent_text
        validated["consent_version"] = site.consent_version
        validated["consent_at"] = timezone.now()
        return super().create(validated)


class EnquirySerializer(ConsentMixin, SpamCheckMixin, serializers.ModelSerializer):
    """Contact Us: the fields named in the content document, in its order."""

    organisation = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=80)
    area_of_interest = serializers.ChoiceField(choices=AreaOfInterest.choices)

    class Meta:
        model = Enquiry
        fields = ["name", "organisation", "email", "phone", "country", "area_of_interest", "message",
                  "consent", *TRACKING, "website", "turnstile_token"]


class ConsultationRequestSerializer(ConsentMixin, SpamCheckMixin, serializers.ModelSerializer):
    MAX_ATTACHMENTS = 5

    consent = serializers.BooleanField()
    sector = serializers.SlugRelatedField(slug_field="slug", queryset=Sector.objects.all(), required=False, allow_null=True)
    services = serializers.SlugRelatedField(slug_field="slug", queryset=Service.objects.all(), many=True, required=False)
    attachments = serializers.ListField(
        child=serializers.FileField(validators=ProposalAttachment._meta.get_field("file").validators),
        required=False, write_only=True,
    )

    area_of_interest = serializers.ChoiceField(choices=AreaOfInterest.choices)

    class Meta:
        model = ProposalRequest
        fields = ["name", "organisation", "organisation_type", "role", "email", "phone", "country",
                  "area_of_interest", "project_type", "sector", "services", "location", "project_stage", "budget",
                  "timeline", "scope", "attachments", "consent", *TRACKING, "website", "turnstile_token"]

    def validate_attachments(self, files):
        if len(files) > self.MAX_ATTACHMENTS:
            raise serializers.ValidationError(f"Attach up to {self.MAX_ATTACHMENTS} files.")
        return files

    def validate_scope(self, value):
        if len(value.strip()) < 30:
            raise serializers.ValidationError("Please describe the scope in a little more detail (30 characters or more).")
        return value

    def create(self, validated):
        files = validated.pop("attachments", [])
        request = super().create(validated)
        for upload in files:
            ProposalAttachment.objects.create(request=request, file=upload, original_name=upload.name[:200])
        return request


class DownloadLeadSerializer(SpamCheckMixin, serializers.ModelSerializer):
    class Meta:
        model = DownloadLead
        fields = ["name", "email", "company", "locale", "source_page", "website", "turnstile_token"]


def download_target(download: Download, locale: str, request) -> str:
    field = download.file_ar if locale == "ar" and download.file_ar else download.file
    return request.build_absolute_uri(field.url)

