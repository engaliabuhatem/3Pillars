from django.db import models
from django.utils import timezone

from apps.core.fields import RichTextField
from apps.core.files import RandomName, document_validators, private_storage
from apps.core.models import Publishable, Seo, Slugged


class Job(Publishable, Slugged, Seo):
    cache_tags = ("jobs",)
    public_path = "/careers/{slug}"

    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship"

    title = models.CharField(max_length=140)
    title_ar = models.CharField("Title (Arabic)", max_length=140, blank=True)
    location = models.CharField(max_length=120)
    location_ar = models.CharField("Location (Arabic)", max_length=120, blank=True)
    employment_type = models.CharField(max_length=12, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    summary = models.CharField(max_length=240)
    summary_ar = models.CharField("Summary (Arabic)", max_length=240, blank=True)
    description = RichTextField()
    description_ar = RichTextField("Description (Arabic)", blank=True)
    is_open = models.BooleanField("Accepting applications", default=True)
    posted_at = models.DateField(default=timezone.localdate)
    closes_at = models.DateField(null=True, blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "job"

    def __str__(self) -> str:
        return self.title

    def slug_source(self) -> str:
        return self.title


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        SHORTLISTED = "shortlisted", "Shortlisted"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Not progressed"

    job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL, related_name="applications",
                            help_text="Empty for an open (speculative) application.")
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    linkedin = models.URLField(blank=True)
    cover_note = models.TextField(blank=True)
    cv = models.FileField("CV", upload_to=RandomName("cvs"), storage=private_storage,
                          validators=document_validators(("pdf", "docx"), 5))
    cv_original_name = models.CharField(max_length=200, blank=True)
    locale = models.CharField(max_length=2, default="en")
    consent = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now, db_index=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW, db_index=True)
    is_handled = models.BooleanField("Handled", default=False, db_index=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self) -> str:
        return f"{self.name} — {self.job or 'Open application'}"
