from django.contrib import admin

from apps.core.admin_base import BaseAdmin, PrivateFileAdminMixin, PublishableAdmin, publishing_tab, seo_tab, tab

from .models import Application, Job


@admin.register(Job)
class JobAdmin(PublishableAdmin):
    list_display = ["title", "location", "employment_type", "is_open", "application_count", "status_badge", "site_link"]
    list_filter = ["is_open", "employment_type"]
    list_editable = ["is_open"]
    search_fields = ["title", "title_ar", "location"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        tab("Content", ("title", "title_ar"), ("slug", "employment_type"), ("location", "location_ar"),
            ("summary", "summary_ar"), ("description", "description_ar")),
        tab("Dates", "is_open", ("posted_at", "closes_at")),
        seo_tab(),
        publishing_tab(),
    ]

    @admin.display(description="Applications")
    def application_count(self, obj):
        return obj.applications.count()


@admin.register(Application)
class ApplicationAdmin(PrivateFileAdminMixin, BaseAdmin):
    private_file_fields = ("cv",)
    list_display = ["submitted_at", "name", "job", "status", "is_handled"]
    list_filter = ["status", "is_handled", "job", "submitted_at"]
    list_editable = ["status", "is_handled"]
    search_fields = ["name", "email", "cover_note"]
    readonly_fields = ["job", "name", "email", "phone", "linkedin", "cover_note", "cv_download", "locale",
                       "consent", "submitted_at"]
    fieldsets = [
        ("Review", {"fields": [("status", "is_handled")]}),
        ("Applicant", {"fields": ["job", ("name", "email"), ("phone", "linkedin"), "cover_note", "cv_download"]}),
        ("Record", {"classes": ["collapse"], "fields": ["submitted_at", "locale", "consent"]}),
    ]

    def has_add_permission(self, request):
        return False

    @admin.display(description="CV")
    def cv_download(self, obj):
        return self.file_link(obj, "cv", f"Download {obj.cv_original_name or 'CV'}")
