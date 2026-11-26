from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin as OTPTOTPDeviceAdmin
from django_otp.plugins.otp_totp.models import TOTPDevice
from unfold.admin import ModelAdmin

from .admin_base import (
    APPROVE_PERMISSION,
    BaseAdmin,
    MissingSeoFilter,
    BaseStackedInline,
    BaseTabularInline,
    PublishableAdmin,
    media_tab,
    hero_tab,
    publishing_tab,
    seo_tab,
    tab,
)
from .models import (
    FooterColumn,
    HomeSection,
    LaunchReadiness,
    LaunchReadinessItem,
    NavItem,
    Page,
    PageBlock,
    PageBlockItem,
    Redirect,
    SiteSettings,
)

# Django registers User/Group with its own unstyled admin; swap in Unfold's.
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(TOTPDevice)


@admin.register(User)
class UserAdmin(DjangoUserAdmin, ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "is_active", "is_superuser"]


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin, ModelAdmin):
    pass


@admin.register(TOTPDevice)
class TOTPDeviceAdmin(OTPTOTPDeviceAdmin, ModelAdmin):
    pass


# ── Site settings ────────────────────────────────────────────────────────


@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseAdmin):
    preview_fields = ("hero_poster", "hero_poster_mobile", "default_hero_image")
    readonly_fields = ["hero_video_status", "consent_version"]

    class Media:
        js = ["js/seo-counter.js"]
    fieldsets = [
        tab("Switches", "coming_soon", "show_pending_content", "copy_approval",
            description="Both switches take effect on the website within seconds. Turn “Show content awaiting "
                        "approval” OFF before going live."),
        tab("Company", ("company_name", "company_name_ar"), ("short_name", "short_name_ar"),
            ("tagline", "tagline_ar"), ("group_relationship", "group_relationship_ar"),
            "logo_light", "logo_dark", "favicon"),
        tab("Hero", ("home_h1", "home_h1_ar"), ("hero_eyebrow", "hero_eyebrow_ar"),
            ("hero_headline", "hero_headline_ar"), ("hero_subline", "hero_subline_ar"),
            ("hero_primary_label", "hero_primary_label_ar", "hero_primary_link"),
            ("hero_secondary_label", "hero_secondary_label_ar", "hero_secondary_link"),
            description="The full-screen opening of the home page. The page heading (H1) is the small line above "
                        "the display headline; it is the one search engines read."),
        tab("Hero video", "hero_video_status", "hero_video", "hero_video_webm", "hero_video_mobile",
            "hero_poster_preview", "hero_poster", ("hero_poster_alt", "hero_poster_alt_ar"),
            "hero_poster_mobile_preview", "hero_poster_mobile", "default_hero_image_preview", "default_hero_image",
            description="Desktop and mobile each get their own video and poster; phones fall back to the "
                        "desktop ones when theirs are empty. Without a video the poster is shown with a slow zoom."),
        tab("Contact", "contact_verified", "phone", "email", ("whatsapp", "show_whatsapp"), ("address", "address_ar"),
            ("business_hours", "business_hours_ar"), "linkedin", "x_twitter", "facebook", "instagram", "youtube",
            description="Publish only verified corporate details. If 3 Pillars uses HS Group offices or shared "
                        "channels, explain the relationship and obtain approval before displaying them."),
        tab("Forms", "notification_emails", "recipients_project_management", "recipients_pmo_controls",
            "recipients_business_development", "recipients_strategic_advisory", "recipients_other",
            ("consent_text", "consent_text_ar"), "consent_version", "capability_gate", "turnstile_enabled",
            "turnstile_site_key",
            description="Each area of interest goes to its own list, one email per line; an empty list falls back "
                        "to the general one."),
        tab("Home SEO", "home_primary_keyword", "home_supporting_keywords", ("home_seo_title", "home_seo_title_ar"),
            ("home_meta_description", "home_meta_description_ar"), "home_ar_reviewed",
            description="Keywords are guidance only and are never published as a tag."),
        tab("SEO & analytics", "prefer_www", ("seo_title", "seo_title_ar"), ("seo_description", "seo_description_ar"),
            "og_image", "analytics_provider", "analytics_id", ("cookie_notice", "cookie_notice_ar"),
            description="Default title and description for any page without its own."),
    ]

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if not request.user.has_perm(APPROVE_PERMISSION):
            fields.append("copy_approval")
        return fields

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # A singleton has no list: go straight to the one form.
        return redirect(reverse("admin:core_sitesettings_change", args=[SiteSettings.load().pk]))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if "coming_soon" in form.changed_data and not obj.coming_soon:
            still_open = LaunchReadinessItem.objects.filter(status=LaunchReadinessItem.Status.OPEN)
            if still_open:
                self.message_user(
                    request,
                    format_html("The site is open, but {} launch readiness item(s) are still unconfirmed: {}. "
                                "<a href=\"{}\" class=\"ap-link\">Review them</a>.", still_open.count(),
                                "; ".join(still_open.values_list("item", flat=True)),
                                reverse("admin:core_launchreadiness_changelist")),
                    messages.WARNING,
                )

    @admin.display(description="Current video")
    def hero_video_status(self, obj):
        if not obj.hero_video:
            return "No video uploaded — the poster image is used."
        return format_html('<video src="{}" muted loop playsinline controls style="max-width:360px;border-radius:12px">'
                           '</video>', obj.hero_video.url)


# ── Navigation ───────────────────────────────────────────────────────────


class ChildNavInline(BaseTabularInline):
    model = NavItem
    fk_name = "parent"
    fields = ["order", "label", "label_ar", "link", "visible"]
    verbose_name_plural = "dropdown items"


@admin.register(NavItem)
class NavItemAdmin(BaseAdmin):
    list_display = ["label", "label_ar", "menu", "link", "parent", "column", "visible"]
    list_filter = ["menu", "visible"]
    list_editable = ["visible"]
    search_fields = ["label", "label_ar", "link"]
    ordering_field = "order"
    hide_ordering_field = True
    inlines = [ChildNavInline]
    fields = ["menu", ("label", "label_ar"), "link", "mega_menu", "parent", "column", ("visible", "is_cta")]


class FooterLinkInline(BaseTabularInline):
    model = NavItem
    fk_name = "column"
    fields = ["order", "label", "label_ar", "link", "visible"]
    verbose_name_plural = "links"


@admin.register(FooterColumn)
class FooterColumnAdmin(BaseAdmin):
    list_display = ["title", "title_ar"]
    ordering_field = "order"
    hide_ordering_field = True
    fields = [("title", "title_ar")]
    inlines = [FooterLinkInline]

    def save_formset(self, request, form, formset, change):
        for item in formset.save(commit=False):
            item.menu = NavItem.Menu.FOOTER
            item.save()
        for obj in formset.deleted_objects:
            obj.delete()


@admin.register(Redirect)
class RedirectAdmin(BaseAdmin):
    list_display = ["old_path", "new_path", "permanent", "created_at"]
    search_fields = ["old_path", "new_path"]
    list_filter = ["permanent"]
    fields = ["old_path", "new_path", "permanent"]


# ── Home ─────────────────────────────────────────────────────────────────


@admin.register(HomeSection)
class HomeSectionAdmin(PublishableAdmin):
    list_display = ["kind", "title", "visible", "status_badge"]
    list_editable = ["visible"]
    ordering_field = "order"
    hide_ordering_field = True
    preview_fields = ("image",)
    fieldsets = [
        tab("Content", "kind", "visible", ("eyebrow", "eyebrow_ar"), ("title", "title_ar"), ("intro", "intro_ar"),
            description="Drag sections in the list to reorder the home page. Untick “visible” to hide one."),
        tab("Buttons", ("cta_label", "cta_label_ar", "cta_link"), ("secondary_label", "secondary_label_ar", "secondary_link")),
        media_tab(),
        publishing_tab(),
    ]

    def has_delete_permission(self, request, obj=None):
        return False


# ── Pages ────────────────────────────────────────────────────────────────


class PageBlockInline(BaseStackedInline):
    model = PageBlock
    fields = ["order", ("kind", "visible", "navy"), "note", ("eyebrow", "eyebrow_ar"), ("title", "title_ar"),
              "body", "body_ar", ("attribution", "attribution_ar"), "image", ("image_alt", "image_alt_ar"),
              "image_on_end", ("cta_label", "cta_label_ar", "cta_link")]
    readonly_fields = ["note"]
    show_change_link = True
    tab = True


@admin.register(Page)
class PageAdmin(PublishableAdmin):
    list_display = ["title", "public_path", "status_badge", "site_link", "updated_at"]
    list_filter = [MissingSeoFilter]
    search_fields = ["title", "title_ar", "intro"]
    prepopulated_fields = {"slug": ("title",)}
    preview_fields = ("image", "hero_image")
    inlines = [PageBlockInline]
    fieldsets = [
        tab("Content", ("title", "title_ar"), ("slug", "path"), ("eyebrow", "eyebrow_ar"), ("intro", "intro_ar"),
            ("cta_label", "cta_label_ar"), "note"),
        hero_tab(),
        media_tab(),
        seo_tab(),
        publishing_tab(),
    ]

    @admin.display(description="Address")
    def public_path(self, obj):
        return obj.get_public_path()


class PageBlockItemInline(BaseTabularInline):
    model = PageBlockItem
    fields = ["order", "label", "label_ar", "value", "text", "text_ar", "image", "image_alt", "image_alt_ar"]


@admin.register(PageBlock)
class PageBlockAdmin(BaseAdmin):
    """Reached from a page's block list, for blocks with figures, images or questions."""

    list_display = ["__str__", "page", "kind", "visible"]
    list_filter = ["kind", "page"]
    readonly_fields = ["note"]
    inlines = [PageBlockItemInline]
    preview_fields = ("image",)
    # The full block, so following "Change" from a page never hides fields the
    # page's inline can edit.
    fieldsets = [
        tab("Content", "page", ("kind", "visible", "navy"), "note", ("eyebrow", "eyebrow_ar"), ("title", "title_ar"),
            ("body", "body_ar"), ("attribution", "attribution_ar")),
        tab("Media", "image_preview", "image", ("image_alt", "image_alt_ar"), "image_on_end"),
        tab("Button", ("cta_label", "cta_label_ar"), "cta_link"),
    ]

    def has_module_permission(self, request):
        return False


# ── Launch readiness ─────────────────────────────────────────────────────


class LaunchReadinessItemInline(BaseTabularInline):
    model = LaunchReadinessItem
    fields = ["order", "kind", "item", "requirement", "status", "owner", "note", "confirmed_by", "confirmed_at"]
    readonly_fields = ["confirmed_by", "confirmed_at"]
    extra = 0


@admin.register(LaunchReadiness)
class LaunchReadinessAdmin(BaseAdmin):
    inlines = [LaunchReadinessItemInline]
    fields = ["summary"]
    readonly_fields = ["summary"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return redirect(reverse("admin:core_launchreadiness_change", args=[LaunchReadiness.load().pk]))

    @admin.display(description="Status")
    def summary(self, obj):
        items = LaunchReadinessItem.objects.all()
        confirmed = items.filter(status=LaunchReadinessItem.Status.CONFIRMED).count()
        return f"{confirmed} of {items.count()} confirmed. Turning off “Show the coming-soon page” warns while any are open."

    def save_formset(self, request, form, formset, change):
        for item in formset.save(commit=False):
            stamp_confirmation(item, request.user)
            item.save()
        for obj in formset.deleted_objects:
            obj.delete()


def stamp_confirmation(item: LaunchReadinessItem, user) -> None:
    """Who confirmed an item and when; cleared again if it is reopened."""
    if item.status == LaunchReadinessItem.Status.CONFIRMED and not item.confirmed_at:
        item.confirmed_by, item.confirmed_at = user, timezone.now()
    elif item.status == LaunchReadinessItem.Status.OPEN:
        item.confirmed_by, item.confirmed_at = None, None


@admin.register(LaunchReadinessItem)
class LaunchReadinessItemAdmin(BaseAdmin):
    """The same items as a filterable list, for the dashboard cards to link to."""

    list_display = ["item", "kind", "status", "owner", "note", "confirmed_by", "confirmed_at"]
    list_filter = ["status", "kind"]
    list_editable = ["status", "owner", "note"]
    search_fields = ["item", "requirement", "note"]
    readonly_fields = ["readiness", "confirmed_by", "confirmed_at"]
    fields = ["readiness", "kind", "item", "requirement", "status", "owner", "note", "confirmed_by", "confirmed_at"]
    ordering_field = "order"
    hide_ordering_field = True

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        stamp_confirmation(obj, request.user)
        super().save_model(request, obj, form, change)
