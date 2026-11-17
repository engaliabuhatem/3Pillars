from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from apps.core.admin_base import BaseAdmin, BaseStackedInline, BaseTabularInline, PublishableAdmin, render_thumbnail, tab

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

SEO_TAB = tab("SEO", ("seo_title", "seo_title_ar"), ("seo_description", "seo_description_ar"), "og_image",
              description="Optional. Blank fields fall back to the title and summary.")


def publishing_tab(*extra):
    return tab("Publishing", "approval", *extra,
               description="Only approved items appear on the live site. Only Approvers can change this.")


class ThumbnailListMixin:
    @admin.display(description="")
    def thumb(self, obj):
        return render_thumbnail(obj, "image", size=64)


# ── Home building blocks ─────────────────────────────────────────────────


@admin.register(Pillar)
class PillarAdmin(PublishableAdmin):
    list_display = ["name", "color", "summary", "status_badge"]
    search_fields = ["name", "name_ar", "summary"]
    fieldsets = [
        tab("Content EN", "name", "color", "icon", "summary", "detail"),
        tab("Content AR", "name_ar", "summary_ar", "detail_ar"),
        publishing_tab(),
    ]


@admin.register(KPI)
class KPIAdmin(PublishableAdmin):
    list_display = ["__str__", "source", "status_badge"]
    search_fields = ["label", "label_ar", "source"]
    fieldsets = [
        tab("Content EN", ("prefix", "value", "suffix"), "label", "source",
            description="Figures are published only with a source. Use numbers the company can evidence."),
        tab("Content AR", "suffix_ar", "label_ar", "source_ar"),
        publishing_tab(),
    ]


@admin.register(LifecycleStage)
class LifecycleStageAdmin(PublishableAdmin):
    list_display = ["name", "name_ar", "status_badge"]
    fieldsets = [
        tab("Content EN", "name", "icon", "summary", "deliverables"),
        tab("Content AR", "name_ar", "summary_ar", "deliverables_ar"),
        publishing_tab(),
    ]


@admin.register(Testimonial)
class TestimonialAdmin(PublishableAdmin):
    list_display = ["person", "company", "project", "status_badge"]
    search_fields = ["person", "company", "quote"]
    autocomplete_fields = ["project"]
    preview_fields = ("photo",)
    fieldsets = [
        tab("Content EN", "quote", "person", "role", "company", "project",
            description="Publish only real, attributable quotes with written permission."),
        tab("Content AR", "quote_ar", "person_ar", "role_ar", "company_ar"),
        tab("Media", "photo_preview", "photo", ("photo_alt", "photo_alt_ar")),
        publishing_tab("permission_note"),
    ]


@admin.register(Client)
class ClientAdmin(PublishableAdmin):
    list_display = ["logo_thumb", "name", "kind", "show_in_trust_strip", "status_badge"]
    list_display_links = ["name"]
    list_filter = ["kind", "show_in_trust_strip"]
    list_editable = ["show_in_trust_strip"]
    search_fields = ["name", "name_ar"]
    fieldsets = [
        tab("Details", ("name", "name_ar"), "kind", "website"),
        tab("Logo", "logo", "show_in_trust_strip"),
        publishing_tab(),
    ]

    @admin.display(description="")
    def logo_thumb(self, obj):
        if not obj.logo:
            return "—"
        return format_html('<img src="{}" alt="" style="height:28px;max-width:96px;object-fit:contain">', obj.logo.url)


# ── Services ─────────────────────────────────────────────────────────────


class ServiceDeliverableInline(BaseTabularInline):
    model = ServiceDeliverable
    fields = ["order", "text", "text_ar"]
    tab = True


class ServiceStepInline(BaseStackedInline):
    model = ServiceStep
    fields = ["order", ("title", "title_ar"), ("body", "body_ar")]
    tab = True


class ServiceFAQInline(BaseStackedInline):
    model = ServiceFAQ
    fields = ["order", ("question", "question_ar"), ("answer", "answer_ar")]
    tab = True


@admin.register(Service)
class ServiceAdmin(ThumbnailListMixin, PublishableAdmin):
    list_display = ["thumb", "name", "featured", "status_badge", "site_link"]
    list_display_links = ["name"]
    list_filter = ["featured", "sectors"]
    list_editable = ["featured"]
    search_fields = ["name", "name_ar", "summary"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["sectors"]
    preview_fields = ("image",)
    inlines = [ServiceDeliverableInline, ServiceStepInline, ServiceFAQInline]
    fieldsets = [
        tab("Content EN", "name", "slug", "icon", "summary", "overview", "featured", "sectors"),
        tab("Content AR", "name_ar", "summary_ar", "overview_ar"),
        tab("Media", "image_preview", "image", ("image_alt", "image_alt_ar")),
        SEO_TAB,
        publishing_tab(),
    ]


@admin.register(Sector)
class SectorAdmin(ThumbnailListMixin, PublishableAdmin):
    list_display = ["thumb", "name", "status_badge", "site_link"]
    list_display_links = ["name"]
    search_fields = ["name", "name_ar", "summary"]
    prepopulated_fields = {"slug": ("name",)}
    preview_fields = ("image",)
    fieldsets = [
        tab("Content EN", "name", "slug", "icon", "summary", "intro"),
        tab("Content AR", "name_ar", "summary_ar", "intro_ar"),
        tab("Media", "image_preview", "image", ("image_alt", "image_alt_ar")),
        SEO_TAB,
        publishing_tab(),
    ]


# ── Projects ─────────────────────────────────────────────────────────────


class ProjectMetricInline(BaseTabularInline):
    model = ProjectMetric
    fields = ["order", "label", "label_ar", "value", "unit", "unit_ar", "delta", "delta_ar"]
    tab = True
    verbose_name_plural = "results (KPIs)"


class ProjectImageInline(BaseTabularInline):
    model = ProjectImage
    fields = ["order", "image_preview", "image", "image_alt", "image_alt_ar", "caption", "caption_ar"]
    preview_fields = ("image",)
    tab = True


class MissingMediaFilter(admin.SimpleListFilter):
    title = "media"
    parameter_name = "media"

    def lookups(self, request, model_admin):
        return [("missing_image", "No hero image"), ("missing_alt", "Image without Arabic or English description")]

    def queryset(self, request, queryset):
        if self.value() == "missing_image":
            return queryset.filter(image="")
        if self.value() == "missing_alt":
            return queryset.exclude(image="").filter(Q(image_alt="") | Q(image_alt_ar=""))
        return queryset


@admin.register(Project)
class ProjectAdmin(ThumbnailListMixin, PublishableAdmin):
    list_display = ["thumb", "title", "sector", "country", "status", "featured", "status_badge", "site_link"]
    list_display_links = ["title"]
    list_filter = ["status", "featured", "sector", "services", "country", MissingMediaFilter]
    list_editable = ["featured"]
    search_fields = ["title", "title_ar", "summary", "location", "client__name"]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["client", "sector"]
    filter_horizontal = ["services"]
    preview_fields = ("image",)
    inlines = [ProjectMetricInline, ProjectImageInline]
    fieldsets = [
        tab("Content EN", "title", "slug", "summary", "challenge", "approach", "outcome"),
        tab("Content AR", "title_ar", "summary_ar", "challenge_ar", "approach_ar", "outcome_ar"),
        tab("Facts", ("client", "client_public_name", "client_public_name_ar"), ("location", "location_ar"),
            ("country", "country_ar"), ("sector", "status"), "services", ("role", "role_ar"),
            ("value", "currency", "show_value"), ("start_date", "end_date"),
            description="Facts shown in the project sidebar. The value stays private unless “Show the value publicly” is ticked."),
        tab("Media", "image_preview", "image", ("image_alt", "image_alt_ar")),
        SEO_TAB,
        publishing_tab("featured"),
    ]


# ── People and places ────────────────────────────────────────────────────


@admin.register(TeamMember)
class TeamMemberAdmin(PublishableAdmin):
    list_display = ["photo_thumb", "name", "role", "leadership", "status_badge"]
    list_display_links = ["name"]
    list_filter = ["leadership"]
    list_editable = ["leadership"]
    search_fields = ["name", "name_ar", "role"]
    preview_fields = ("photo",)
    fieldsets = [
        tab("Content EN", "name", "role", "bio", "linkedin", "leadership"),
        tab("Content AR", "name_ar", "role_ar", "bio_ar"),
        tab("Media", "photo_preview", "photo", ("photo_alt", "photo_alt_ar")),
        publishing_tab(),
    ]

    @admin.display(description="")
    def photo_thumb(self, obj):
        return render_thumbnail(obj, "photo", size=48)


@admin.register(Office)
class OfficeAdmin(PublishableAdmin):
    list_display = ["city", "country", "is_headquarters", "phone", "email", "status_badge"]
    search_fields = ["city", "country"]
    preview_fields = ("map_image",)
    fieldsets = [
        tab("Content EN", "city", "country", "address", "phone", "email", "is_headquarters"),
        tab("Content AR", "city_ar", "country_ar", "address_ar"),
        tab("Map", ("latitude", "longitude"), "map_image_preview", "map_image", ("map_image_alt", "map_image_alt_ar"),
            description="Right-click the location in Google Maps to copy its latitude and longitude."),
        publishing_tab(),
    ]


@admin.register(Certification)
class CertificationAdmin(PublishableAdmin):
    list_display = ["name", "issuer", "kind", "year", "status_badge"]
    list_filter = ["kind"]
    search_fields = ["name", "issuer"]
    fieldsets = [
        tab("Content EN", "name", "issuer", "kind", "year", "logo"),
        tab("Content AR", "name_ar", "issuer_ar"),
        publishing_tab("evidence_note"),
    ]


# ── Insights and downloads ───────────────────────────────────────────────


@admin.register(InsightCategory)
class InsightCategoryAdmin(BaseAdmin):
    list_display = ["name", "name_ar", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering_field = "order"
    hide_ordering_field = True

    def has_module_permission(self, request):
        return False


@admin.register(Insight)
class InsightAdmin(ThumbnailListMixin, PublishableAdmin):
    list_display = ["thumb", "title", "category", "published_at", "status_badge", "site_link"]
    list_display_links = ["title"]
    list_filter = ["category"]
    date_hierarchy = "published_at"
    search_fields = ["title", "title_ar", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    preview_fields = ("image",)
    ordering_field = None
    fieldsets = [
        tab("Content EN", "title", "slug", "category", "excerpt", "body", "author", "published_at"),
        tab("Content AR", "title_ar", "excerpt_ar", "body_ar", "author_ar"),
        tab("Media", "image_preview", "image", ("image_alt", "image_alt_ar")),
        SEO_TAB,
        publishing_tab(),
    ]


@admin.register(Download)
class DownloadAdmin(PublishableAdmin):
    list_display = ["title", "gated", "is_capability_statement", "lead_count", "status_badge"]
    list_editable = ["gated"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        tab("Content", ("title", "title_ar"), "slug", ("description", "description_ar"), "file", "file_ar"),
        publishing_tab("gated", "is_capability_statement"),
    ]

    @admin.display(description="Leads")
    def lead_count(self, obj):
        return obj.leads.count()
