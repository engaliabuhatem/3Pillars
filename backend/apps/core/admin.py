from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin as OTPTOTPDeviceAdmin
from django_otp.plugins.otp_totp.models import TOTPDevice
from unfold.admin import ModelAdmin

from .admin_base import BaseAdmin, BaseStackedInline, BaseTabularInline, PublishableAdmin, tab
from .models import FooterColumn, HomeSection, NavItem, Page, PageBlock, PageBlockItem, Redirect, SiteSettings

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
    preview_fields = ("hero_poster", "hero_poster_mobile")
    readonly_fields = ["hero_video_status"]
    fieldsets = [
        tab("Switches", "coming_soon", "show_pending_content",
            description="Both switches take effect on the website within seconds. Turn “Show content awaiting "
                        "approval” OFF before going live."),
        tab("Company", ("company_name", "company_name_ar"), ("short_name", "short_name_ar"),
            ("tagline", "tagline_ar"), ("group_relationship", "group_relationship_ar"),
            "logo_light", "logo_dark", "favicon"),
        tab("Hero", ("hero_eyebrow", "hero_eyebrow_ar"), ("hero_headline", "hero_headline_ar"),
            ("hero_subline", "hero_subline_ar"),
            ("hero_primary_label", "hero_primary_label_ar", "hero_primary_link"),
            ("hero_secondary_label", "hero_secondary_label_ar", "hero_secondary_link"),
            description="The full-screen opening of the home page."),
        tab("Hero video", "hero_video_status", "hero_video", "hero_video_webm", "hero_video_mobile",
            "hero_poster_preview", "hero_poster", ("hero_poster_alt", "hero_poster_alt_ar"),
            "hero_poster_mobile_preview", "hero_poster_mobile",
            description="Desktop and mobile each get their own video and poster; phones fall back to the "
                        "desktop ones when theirs are empty. Without a video the poster is shown with a slow zoom."),
        tab("Contact", "phone", "email", ("whatsapp", "show_whatsapp"), ("address", "address_ar"),
            "linkedin", "x_twitter", "facebook", "instagram", "youtube"),
        tab("Forms", "notification_emails", "capability_gate", "turnstile_enabled", "turnstile_site_key"),
        tab("SEO & analytics", ("seo_title", "seo_title_ar"), ("seo_description", "seo_description_ar"), "og_image",
            "analytics_provider", "analytics_id", ("cookie_notice", "cookie_notice_ar")),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # A singleton has no list: go straight to the one form.
        return redirect(reverse("admin:core_sitesettings_change", args=[SiteSettings.load().pk]))

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
    fields = ["menu", ("label", "label_ar"), "link", "mega_menu", "parent", "column", "visible"]


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
class HomeSectionAdmin(BaseAdmin):
    list_display = ["kind", "title", "visible"]
    list_editable = ["visible"]
    ordering_field = "order"
    hide_ordering_field = True
    preview_fields = ("image",)
    fieldsets = [
        tab("Content", "kind", "visible", ("eyebrow", "eyebrow_ar"), ("title", "title_ar"), ("intro", "intro_ar"),
            description="Drag sections in the list to reorder the home page. Untick “visible” to hide one."),
        tab("Buttons", ("cta_label", "cta_label_ar", "cta_link"), ("secondary_label", "secondary_label_ar", "secondary_link")),
        tab("Media", "image_preview", "image", ("image_alt", "image_alt_ar")),
    ]

    def has_delete_permission(self, request, obj=None):
        return False


# ── Pages ────────────────────────────────────────────────────────────────


class PageBlockInline(BaseStackedInline):
    model = PageBlock
    fields = ["order", ("kind", "visible", "navy"), ("eyebrow", "eyebrow_ar"), ("title", "title_ar"),
              "body", "body_ar", ("attribution", "attribution_ar"), "image", ("image_alt", "image_alt_ar"),
              "image_on_end", ("cta_label", "cta_label_ar", "cta_link")]
    show_change_link = True
    tab = True


@admin.register(Page)
class PageAdmin(PublishableAdmin):
    list_display = ["title", "slug", "status_badge", "site_link", "updated_at"]
    search_fields = ["title", "title_ar", "intro"]
    prepopulated_fields = {"slug": ("title",)}
    preview_fields = ("image",)
    inlines = [PageBlockInline]
    fieldsets = [
        tab("Content EN", "title", "slug", "eyebrow", "intro"),
        tab("Content AR", "title_ar", "eyebrow_ar", "intro_ar"),
        tab("Media", "image_preview", "image", ("image_alt", "image_alt_ar")),
        tab("SEO", ("seo_title", "seo_title_ar"), ("seo_description", "seo_description_ar"), "og_image"),
        tab("Publishing", "approval"),
    ]


class PageBlockItemInline(BaseTabularInline):
    model = PageBlockItem
    fields = ["order", "label", "label_ar", "value", "text", "text_ar", "image", "image_alt", "image_alt_ar"]


@admin.register(PageBlock)
class PageBlockAdmin(BaseAdmin):
    """Reached from a page's block list, for blocks with figures, images or questions."""

    list_display = ["__str__", "page", "kind", "visible"]
    list_filter = ["kind", "page"]
    inlines = [PageBlockItemInline]
    fields = ["page", ("kind", "visible", "navy"), ("title", "title_ar")]

    def has_module_permission(self, request):
        return False
