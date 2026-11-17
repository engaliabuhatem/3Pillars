from rest_framework import serializers

from apps.content.models import Download, Sector, Service

from .models import DownloadLead, Enquiry, ProposalAttachment, ProposalRequest
from .services import SpamCheckMixin

TRACKING = ["locale", "source_page", "utm_source", "utm_medium", "utm_campaign"]


class EnquirySerializer(SpamCheckMixin, serializers.ModelSerializer):
    consent = serializers.BooleanField()

    class Meta:
        model = Enquiry
        fields = ["topic", "name", "organisation", "role", "email", "phone", "country", "subject", "message",
                  "consent", *TRACKING, "website", "turnstile_token"]

    def validate_consent(self, value):
        if not value:
            raise serializers.ValidationError("Please agree to the privacy notice so we can reply.")
        return value


class ProposalRequestSerializer(SpamCheckMixin, serializers.ModelSerializer):
    MAX_ATTACHMENTS = 5

    consent = serializers.BooleanField()
    sector = serializers.SlugRelatedField(slug_field="slug", queryset=Sector.objects.all(), required=False, allow_null=True)
    services = serializers.SlugRelatedField(slug_field="slug", queryset=Service.objects.all(), many=True, required=False)
    attachments = serializers.ListField(
        child=serializers.FileField(validators=ProposalAttachment._meta.get_field("file").validators),
        required=False, write_only=True,
    )

    class Meta:
        model = ProposalRequest
        fields = ["name", "organisation", "organisation_type", "role", "email", "phone", "country",
                  "project_type", "sector", "services", "location", "project_stage", "budget", "timeline", "scope",
                  "attachments", "consent", *TRACKING, "website", "turnstile_token"]

    def validate_consent(self, value):
        if not value:
            raise serializers.ValidationError("Please agree to the privacy notice so we can reply.")
        return value

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

