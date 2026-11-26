from django import forms
from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html
from unfold.widgets import UnfoldAdminCheckboxSelectMultipleWidget

from apps.core.admin_base import (
    BaseAdmin,
    BaseStackedInline,
    BaseTabularInline,
    MissingSeoFilter,
    PrivateFileAdminMixin,
    PublishableAdmin,
    badge,
    hero_tab,
    media_tab,
    publishing_tab,
    render_thumbnail,
    seo_tab,
    tab,
)

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


class ThumbnailListMixin:
    @admin.display(description="")
    def thumb(self, obj):
        return render_thumbnail(obj, "image", size=64)


# ── Home and About building blocks ───────────────────────────────────────


@admin.register(Pillar)
class PillarAdmin(PublishableAdmin):
    list_display = ["__str__", "role_on_site", "is_proposed", "service", "status_badge"]
    search_fields = ["name", "name_ar", "summary"]
    autocomplete_fields = ["service"]
    fieldsets = [
        tab("Content", ("number", "color"), ("name", "name_ar"), ("role_on_site", "is_proposed"),
            ("core_value", "core_value_ar"), ("summary", "summary_ar"), ("detail", "detail_ar"),
            ("core_outcomes", "core_outcomes_ar"), ("covers", "covers_ar"), "service",
            description="Summary: the home page card. Detail and core outcomes: Our Approach. "
                        "What it covers: the table on the services page."),
        publishing_tab("note"),
    ]


@admin.register(ValuePoint)
class ValuePointAdmin(PublishableAdmin):
    list_display = ["title", "body", "status_badge"]
    fieldsets = [tab("Content", ("title", "title_ar"), ("body", "body_ar")), publishing_tab()]


@admin.register(CompanyValue)
class CompanyValueAdmin(PublishableAdmin):
    list_display = ["value", "in_practice", "status_badge"]
    fieldsets = [tab("Content", ("value", "value_ar"), ("in_practice", "in_practice_ar")), publishing_tab()]


@admin.register(ApproachStep)
class ApproachStepAdmin(PublishableAdmin):
    list_display = ["name", "summary", "status_badge"]
    fieldsets = [tab("Content", ("name", "name_ar"), ("summary", "summary_ar")), publishing_tab()]


@admin.register(KPI)
class KPIAdmin(PublishableAdmin):
    list_display = ["__str__", "source", "status_badge"]
    search_fields = ["label", "label_ar", "source"]
    fieldsets = [
        tab("Content", ("prefix", "value"), ("suffix", "suffix_ar"), ("label", "label_ar"), ("source", "source_ar"),
            description="Figures are published only with a source. Use numbers 3 Pillars can evidence from its own records."),
        publishing_tab(),
    ]


@admin.register(Testimonial)
class TestimonialAdmin(PublishableAdmin):
    list_display = ["person", "company", "project", "status_badge"]
    search_fields = ["person", "company", "quote"]
    autocomplete_fields = ["project"]
    preview_fields = ("photo",)
    fieldsets = [
        tab("Content", ("quote", "quote_ar"), ("person", "person_ar"), ("role", "role_ar"), ("company", "company_ar"),
            "project", description="Publish only real, attributable quotes with written permission."),
        media_tab("photo", "Photo"),
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
        tab("Content", ("name", "name_ar"), ("kind", "website")),
        tab("Logo", "logo"),
        publishing_tab("show_in_trust_strip"),
    ]

    @admin.display(description="")
    def logo_thumb(self, obj):
        if not obj.logo:
            return "—"
        return format_html('<img src="{}" alt="" style="height:28px;max-width:96px;object-fit:contain">', obj.logo.url)


# ── Services ─────────────────────────────────────────────────────────────


class ServiceCapabilityInline(BaseStackedInline):
    model = ServiceCapability
    fields = ["order", ("title", "title_ar"), ("description", "description_ar")]
    tab = True
    verbose_name_plural = "List · capabilities"


class ServiceBulletInline(BaseTabularInline):
    model = ServiceBullet
    fields = ["order", "text", "text_ar"]
    tab = True
    verbose_name_plural = "List · bullets"


class ServiceStepInline(BaseStackedInline):
    model = ServiceStep
    fields = ["order", ("title", "title_ar"), ("body", "body_ar")]
    tab = True
    verbose_name_plural = "List · process steps"


class ServiceFAQInline(BaseStackedInline):
    model = ServiceFAQ
    fields = ["order", ("question", "question_ar"), ("answer", "answer_ar")]
    tab = True
    verbose_name_plural = "List · questions"


@admin.register(Service)
class ServiceAdmin(ThumbnailListMixin, PublishableAdmin):
    list_display = ["thumb", "name", "pillar", "status_badge", "site_link"]
    list_display_links = ["name"]
    list_filter = ["pillar", "related_sectors", MissingSeoFilter]
    search_fields = ["name", "name_ar", "summary"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["related_sectors"]
    autocomplete_fields = ["pillar"]
    preview_fields = ("image", "hero_image")
    inlines = [ServiceCapabilityInline, ServiceBulletInline, ServiceStepInline, ServiceFAQInline]
    fieldsets = [
        tab("Content EN", "name", ("slug", "icon"), "summary", "intro", "who_we_support", "context_title",
            "context_body", "cta_headline", "cta_label"),
        tab("Content AR", "name_ar", "summary_ar", "intro_ar", "who_we_support_ar", "context_title_ar",
            "context_body_ar", "cta_headline_ar", "cta_label_ar"),
        tab("Lists", ("capabilities_title", "capabilities_title_ar"), ("bullets_title", "bullets_title_ar"),
            ("scope_caveat", "scope_caveat_ar"), ("steps_title", "steps_title_ar"),
            description="Headings for the lists. The items themselves are in the “List ·” tabs. Empty lists are hidden."),
        tab("Related", "pillar", "related_sectors",
            description="Each linked sector also links back to this service."),
        hero_tab(),
        media_tab(),
        seo_tab(),
        publishing_tab("positioning_note"),
    ]


class SectorListItemInline(BaseTabularInline):
    model = SectorListItem
    fields = ["order", "text", "text_ar"]
    tab = True
    verbose_name_plural = "List · items"


class SectorFAQInline(BaseStackedInline):
    model = SectorFAQ
    fields = ["order", ("question", "question_ar"), ("answer", "answer_ar")]
    tab = True
    verbose_name_plural = "List · questions"


class SectorForm(forms.ModelForm):
    """The service ↔ sector link is one relation, editable from either side."""

    related_services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(), required=False, widget=UnfoldAdminCheckboxSelectMultipleWidget,
        help_text="Each linked service also links back to this sector.",
    )

    class Meta:
        model = Sector
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["related_services"].initial = self.instance.related_services.all()


class ThinFilter(admin.SimpleListFilter):
    title = "content depth"
    parameter_name = "depth"

    def lookups(self, request, model_admin):
        return [("thin", "Thin: no questions, projects or insights")]

    def queryset(self, request, queryset):
        if self.value() == "thin":
            return queryset.filter(faqs__isnull=True, projects__isnull=True, insights__isnull=True).distinct()
        return queryset


@admin.register(Sector)
class SectorAdmin(ThumbnailListMixin, PublishableAdmin):
    form = SectorForm
    list_display = ["thumb", "name", "depth", "status_badge", "site_link"]
    list_display_links = ["name"]
    list_filter = [ThinFilter, MissingSeoFilter]
    search_fields = ["name", "name_ar", "focus_summary"]
    prepopulated_fields = {"slug": ("name",)}
    preview_fields = ("image", "hero_image")
    inlines = [SectorListItemInline, SectorFAQInline]
    fieldsets = [
        tab("Content EN", "name", ("slug", "icon"), "focus_summary", "intro", "our_focus"),
        tab("Content AR", "name_ar", "focus_summary_ar", "intro_ar", "our_focus_ar"),
        tab("Lists", ("list_title", "list_title_ar"), ("scope_caveat", "scope_caveat_ar"),
            description="The heading for the list. The items are in the “List ·” tabs."),
        tab("Related", "related_services"),
        hero_tab(),
        media_tab(),
        seo_tab(),
        publishing_tab("positioning_note"),
    ]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.related_services.set(form.cleaned_data["related_services"])

    @admin.display(description="Depth")
    def depth(self, obj):
        return badge("Thin", "orange") if obj.is_thin else badge("OK", "green")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and obj.is_thin and request.method == "GET":
            self.message_user(
                request,
                "This sector has no questions and no related projects or insights. That is allowed, but the page "
                "is thin: add sector-specific questions or link related work when you can.",
                level="warning",
            )
        return super().change_view(request, object_id, form_url, extra_context)


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
class ProjectAdmin(PrivateFileAdminMixin, ThumbnailListMixin, PublishableAdmin):
    private_file_fields = ("attribution_evidence",)
    list_display = ["thumb", "title", "entry_type", "our_role", "delivery_entity", "attribution", "status_badge",
                    "site_link"]
    list_display_links = ["title"]
    list_filter = ["entry_type", "our_role", "attribution_approved", "status", "featured", "sector", "services",
                   MissingMediaFilter]
    search_fields = ["title", "title_ar", "summary", "location", "delivery_entity", "client__name"]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["client", "sector"]
    filter_horizontal = ["services"]
    preview_fields = ("image", "hero_image")
    readonly_fields = ["evidence_link"]
    inlines = [ProjectMetricInline, ProjectImageInline]
    fieldsets = [
        tab("Content", ("title", "title_ar"), ("slug", "entry_type"), ("summary", "summary_ar"),
            ("challenge", "challenge_ar"), ("scope_of_services", "scope_of_services_ar"),
            ("approach", "approach_ar"), ("results", "results_ar")),
        tab("Role & attribution", ("delivery_entity", "delivery_entity_ar"), "our_role",
            ("our_role_detail", "our_role_detail_ar"), "attribution_evidence", "evidence_link", "attribution_notes",
            "attribution_approved",
            description="Credit the entity that delivered the work and 3 Pillars’ exact role. Never attribute HS Group, "
                        "affiliate or joint-venture work to 3 Pillars without evidence and approval."),
        tab("Facts", ("client", "client_name_approved"), ("client_public_name", "client_public_name_ar"),
            ("location", "location_ar"), ("country", "country_ar"), ("sector", "status"), "services",
            ("value", "currency", "show_value"), ("start_date", "end_date"),
            description="The client is named only when “Client agreed to be named” is ticked. "
                        "The value stays private unless “Show the value publicly” is ticked."),
        hero_tab(),
        media_tab(),
        seo_tab(),
        publishing_tab("featured"),
    ]

    @admin.display(description="Attribution")
    def attribution(self, obj):
        return badge("Confirmed", "green") if obj.attribution_approved else badge("Unconfirmed", "orange")

    @admin.display(description="Current evidence")
    def evidence_link(self, obj):
        return self.file_link(obj, "attribution_evidence")


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
        tab("Content", ("name", "name_ar"), ("role", "role_ar"), ("bio", "bio_ar"), "linkedin",
            description="Publish names, titles, biographies and photographs only with each person’s approval."),
        media_tab("photo", "Photo"),
        publishing_tab("leadership"),
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
        tab("Content", ("city", "city_ar"), ("country", "country_ar"), ("address", "address_ar"), ("phone", "email"),
            "is_headquarters", description="Only offices 3 Pillars itself operates, once verified."),
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
        tab("Content", ("name", "name_ar"), ("issuer", "issuer_ar"), ("kind", "year"), "logo"),
        publishing_tab("evidence_note"),
    ]


# ── Insights and downloads ───────────────────────────────────────────────


@admin.register(InsightCategory)
class InsightCategoryAdmin(BaseAdmin):
    list_display = ["name", "name_ar", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "name_ar"]
    ordering_field = "order"
    hide_ordering_field = True
    fields = [("name", "name_ar"), "slug"]


class DraftTopicFilter(admin.SimpleListFilter):
    title = "writing"
    parameter_name = "writing"

    def lookups(self, request, model_admin):
        return [("unwritten", "Planned topics without a body")]

    def queryset(self, request, queryset):
        if self.value() == "unwritten":
            return queryset.filter(is_draft_topic=True, body="")
        return queryset


@admin.register(Insight)
class InsightAdmin(ThumbnailListMixin, PublishableAdmin):
    list_display = ["thumb", "title", "kind", "category", "written", "published_at", "status_badge", "site_link"]
    list_display_links = ["title"]
    list_filter = [DraftTopicFilter, "kind", "category", MissingSeoFilter]
    date_hierarchy = "published_at"
    search_fields = ["title", "title_ar", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["sectors"]
    preview_fields = ("image", "hero_image")
    ordering_field = None
    fieldsets = [
        tab("Content", ("title", "title_ar"), ("slug", "kind"), ("category", "is_draft_topic"),
            ("excerpt", "excerpt_ar"), ("body", "body_ar"), ("our_role_statement", "our_role_statement_ar"),
            ("author", "author_ar"), "published_at", "sectors",
            description="Nothing without a body is ever shown, even on staging. News also needs a date, a summary "
                        "and a factual statement of 3 Pillars’ role."),
        hero_tab(),
        media_tab(),
        seo_tab(),
        publishing_tab(),
    ]

    @admin.display(description="Written", boolean=True)
    def written(self, obj):
        return bool(obj.body.strip())


@admin.register(Download)
class DownloadAdmin(PublishableAdmin):
    list_display = ["title", "gated", "is_capability_statement", "lead_count", "status_badge"]
    list_editable = ["gated"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        tab("Content", ("title", "title_ar"), "slug", ("description", "description_ar"), ("file", "file_ar")),
        publishing_tab("gated", "is_capability_statement"),
    ]

    @admin.display(description="Leads")
    def lead_count(self, obj):
        return obj.leads.count()
