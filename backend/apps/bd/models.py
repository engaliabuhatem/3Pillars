"""
Inbound leads and the lightweight BD pipeline around them.

A submission is a record of what someone sent, so its submitted fields are
read-only in the admin. What staff change is the pipeline layer: stage, owner,
follow-up date, handled flag and internal notes.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.files import RandomName, document_validators, private_storage


class Stage(models.TextChoices):
    NEW = "new", "New"
    QUALIFIED = "qualified", "Qualified"
    PROPOSAL_SENT = "proposal_sent", "Proposal sent"
    WON = "won", "Won"
    LOST = "lost", "Lost"


OPEN_STAGES = (Stage.NEW, Stage.QUALIFIED, Stage.PROPOSAL_SENT)


class LeadQuerySet(models.QuerySet):
    def overdue(self):
        return self.filter(next_follow_up__lt=timezone.localdate(), stage__in=OPEN_STAGES)


class Lead(models.Model):
    """Who sent it, where from, and where it is in the pipeline."""

    name = models.CharField(max_length=160)
    organisation = models.CharField(max_length=200, blank=True)
    role = models.CharField("Job title", max_length=120, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=80, blank=True)

    locale = models.CharField(max_length=2, default="en", choices=[("en", "English"), ("ar", "Arabic")])
    source_page = models.CharField(max_length=300, blank=True)
    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=120, blank=True)
    consent = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now, db_index=True)

    stage = models.CharField(max_length=16, choices=Stage.choices, default=Stage.NEW, db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
        limit_choices_to={"is_staff": True},
    )
    next_follow_up = models.DateField(null=True, blank=True, db_index=True)
    is_handled = models.BooleanField("Handled", default=False, db_index=True)

    objects = LeadQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ["-submitted_at"]

    @property
    def who(self) -> str:
        return self.organisation or self.name


class Enquiry(Lead):
    class Topic(models.TextChoices):
        GENERAL = "general", "General enquiry"
        CONSULTATION = "consultation", "Book a consultation"
        PARTNERSHIP = "partnership", "Partnership"
        MEDIA = "media", "Media"

    topic = models.CharField(max_length=16, choices=Topic.choices, default=Topic.GENERAL)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    class Meta(Lead.Meta):
        verbose_name = "enquiry"
        verbose_name_plural = "enquiries"

    def __str__(self) -> str:
        return f"{self.get_topic_display()}: {self.who}"


class ProposalRequest(Lead):
    class ProjectStage(models.TextChoices):
        CONCEPT = "concept", "Concept / idea"
        FEASIBILITY = "feasibility", "Feasibility"
        DESIGN = "design", "Design"
        TENDER = "tender", "Tender / procurement"
        CONSTRUCTION = "construction", "Construction"
        OPERATION = "operation", "Operation / closeout"

    class Budget(models.TextChoices):
        UNDISCLOSED = "undisclosed", "Prefer not to say"
        UNDER_1M = "lt1m", "Under $1M"
        M1_10 = "1-10m", "$1M – $10M"
        M10_50 = "10-50m", "$10M – $50M"
        M50_250 = "50-250m", "$50M – $250M"
        OVER_250M = "gt250m", "Over $250M"

    class Timeline(models.TextChoices):
        NOW = "now", "Immediately"
        QUARTER = "3m", "Within 3 months"
        HALF = "6m", "Within 6 months"
        LATER = "later", "Later / exploring"

    organisation_type = models.CharField(max_length=60, blank=True)
    project_type = models.CharField(max_length=120)
    sector = models.ForeignKey("content.Sector", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    services = models.ManyToManyField("content.Service", blank=True, related_name="+")
    location = models.CharField(max_length=160)
    project_stage = models.CharField(max_length=16, choices=ProjectStage.choices)
    budget = models.CharField(max_length=12, choices=Budget.choices, default=Budget.UNDISCLOSED)
    timeline = models.CharField(max_length=8, choices=Timeline.choices)
    scope = models.TextField("Scope description")

    class Meta(Lead.Meta):
        verbose_name = "proposal request"

    def __str__(self) -> str:
        return f"{self.project_type}: {self.who}"


class ProposalAttachment(models.Model):
    request = models.ForeignKey(ProposalRequest, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=RandomName("proposals"), storage=private_storage,
        validators=document_validators(("pdf", "docx", "xlsx", "png", "jpg", "jpeg", "zip"), 10),
    )
    original_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.original_name


class DownloadLead(models.Model):
    download = models.ForeignKey("content.Download", on_delete=models.CASCADE, related_name="leads")
    name = models.CharField(max_length=160)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    locale = models.CharField(max_length=2, default="en")
    source_page = models.CharField(max_length=300, blank=True)
    submitted_at = models.DateTimeField(default=timezone.now, db_index=True)
    is_handled = models.BooleanField("Followed up", default=False)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "download lead"

    def __str__(self) -> str:
        return f"{self.name} — {self.download}"


class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.body[:60]


class EnquiryNote(Note):
    enquiry = models.ForeignKey(Enquiry, related_name="notes", on_delete=models.CASCADE)

    class Meta(Note.Meta):
        verbose_name = "internal note"


class ProposalNote(Note):
    request = models.ForeignKey(ProposalRequest, related_name="notes", on_delete=models.CASCADE)

    class Meta(Note.Meta):
        verbose_name = "internal note"
