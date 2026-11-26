"""
Behaviour every admin screen shares.

All classes build on `unfold.admin`; importing ModelAdmin from
django.contrib.admin anywhere in this project leaves that screen unstyled.
"""

from django.contrib import admin, messages
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from .fields import RichTextField
from .images import image_payload
from .models import ApprovalStatus
from .seo import MISSING_SEO, seo_duplicates

APPROVE_PERMISSION = "core.approve_content"


def tab(title: str, *fields, description: str = "") -> tuple:
    options = {"classes": ["tab"], "fields": list(fields)}
    if description:
        options["description"] = description
    return (title, options)


# Every content form uses the same tabs, in the same order:
#   Content (English | Arabic side by side) → Facts/Details → Media → SEO → Publishing
# Side by side lets an editor see at a glance which translations are missing.

def seo_tab() -> tuple:
    """Keyword guidance first, then the fields it should shape. Counters come from js/seo-counter.js."""
    return tab("SEO", "primary_keyword", "supporting_keywords", ("seo_title", "seo_title_ar"),
               ("meta_description", "meta_description_ar"), ("h1", "h1_ar"), "seo_check", "og_image",
               description="Keywords are guidance for writing the title, description and heading. They are never "
                           "published as a tag. Aim for a title of 60 characters or fewer and a description of 160 "
                           "or fewer, each unique across the site.")


class MissingSeoFilter(admin.SimpleListFilter):
    title = "SEO"
    parameter_name = "seo"

    def lookups(self, request, model_admin):
        return [("missing", "Missing SEO title, description or heading")]

    def queryset(self, request, queryset):
        if self.value() == "missing":
            return queryset.filter(MISSING_SEO)
        return queryset


def hero_tab() -> tuple:
    """The photograph behind the page title. Admins using it list "hero_image" in `preview_fields`."""
    return tab("Hero background", "hero_image_preview", "hero_image",
               description="Shown darkened behind the page title. Without one, the default from Site settings → "
                           "Hero video is used.")


def media_tab(field: str = "image", title: str = "Media", description: str = "") -> tuple:
    return tab(title, f"{field}_preview", field, (f"{field}_alt", f"{field}_alt_ar"), description=description)


def publishing_tab(*extra):
    """Approval plus any "where it appears" switches (featured, leadership…)."""
    return tab("Publishing", "approval", "ar_reviewed", *extra,
               description="Only approved items appear on the live site. Only Approvers can change the status. "
                           "An Arabic page is offered to search engines only once its Arabic is reviewed.")


def badge(label: str, tone: str):
    """A tinted status pill; tones are defined in static/css/admin-apple.css."""
    return format_html('<span class="ap-badge ap-badge--{}">{}</span>', tone, label)


class BilingualFormMixin:
    """Arabic inputs render right-to-left; rich text uses the Trix editor."""

    formfield_overrides = {RichTextField: {"widget": WysiwygWidget}}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if field is not None and db_field.name.endswith("_ar"):
            field.widget.attrs.update({"dir": "rtl", "lang": "ar"})
        return field


class PreviewMixin:
    """Read-only thumbnails for the image fields named in `preview_fields`."""

    preview_fields: tuple[str, ...] = ()

    def get_readonly_fields(self, request, obj=None):
        names = [f"{field}_preview" for field in self.preview_fields]
        return [*super().get_readonly_fields(request, obj), *names]

    def __getattr__(self, name):
        if name.endswith("_preview") and name[: -len("_preview")] in type(self).preview_fields:
            field = name[: -len("_preview")]

            def preview(obj):
                return render_thumbnail(obj, field)

            preview.short_description = "Preview"
            return preview
        raise AttributeError(name)


def render_thumbnail(obj, field: str, size: int = 160):
    payload = image_payload(obj, field) if obj and obj.pk else None
    if not payload:
        return format_html('<span class="ap-muted">No image yet</span>')
    return format_html('<img src="{}" alt="" class="ap-thumb" style="max-height:{}px;max-width:{}px">',
                       payload["src"], size * 3 // 4, size * 3 // 2)


class BaseAdmin(BilingualFormMixin, PreviewMixin, ModelAdmin):
    warn_unsaved_form = True
    list_filter_submit = True
    list_fullwidth = True


class BaseTabularInline(BilingualFormMixin, PreviewMixin, TabularInline):
    extra = 0
    ordering_field = "order"
    hide_ordering_field = True


class BaseStackedInline(BilingualFormMixin, PreviewMixin, StackedInline):
    extra = 0
    ordering_field = "order"
    hide_ordering_field = True


# ── Approval ─────────────────────────────────────────────────────────────


def approval_fields(obj) -> list[str]:
    return ["approval", "updated_at"] if hasattr(obj, "updated_at") else ["approval"]


@admin.action(description="Approve for publication", permissions=["approve"])
def approve(modeladmin, request, queryset):
    count, blocked = 0, []
    for obj in queryset:
        if reason := obj.approval_blocker():
            blocked.append(f"“{obj}”: {reason}")
            continue
        obj.approval = ApprovalStatus.APPROVED
        obj.save(update_fields=approval_fields(obj))
        count += 1
    if count:
        modeladmin.message_user(request, f"{count} item(s) approved and live within seconds.", messages.SUCCESS)
    for line in blocked:
        modeladmin.message_user(request, f"Not approved — {line}", messages.ERROR)


@admin.action(description="Unpublish (back to awaiting approval)", permissions=["approve"])
def unpublish(modeladmin, request, queryset):
    count = 0
    for obj in queryset:
        obj.approval = ApprovalStatus.PENDING
        obj.save(update_fields=approval_fields(obj))
        count += 1
    modeladmin.message_user(request, f"{count} item(s) taken off the live site.", messages.WARNING)


class PublishableAdmin(BaseAdmin):
    """
    Everything behind the approval gate. Only the Approver role (or a
    superuser) can change `approval`; editors see it read-only.

    The actions save row by row rather than `queryset.update()` so the
    revalidation signal fires and the site updates immediately.
    """

    actions = [approve, unpublish]
    ordering_field = "order"
    hide_ordering_field = True

    class Media:
        js = ["js/seo-counter.js"]

    def has_approve_permission(self, request):
        return request.user.has_perm(APPROVE_PERMISSION)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if not self.has_approve_permission(request):
            fields.append("approval")
        if hasattr(self.model, "meta_description"):
            fields.append("seo_check")
        return fields

    @admin.display(description="Duplicates")
    def seo_check(self, obj):
        clashes = seo_duplicates(obj) if obj and obj.pk else []
        if not clashes:
            return format_html('<span class="ap-muted">No other page uses this title or description.</span>')
        return format_html('<span class="ap-overdue">{}</span>', "; ".join(clashes))

    def get_list_filter(self, request):
        return ["approval", *super().get_list_filter(request)]

    @admin.display(description="Status", ordering="approval")
    def status_badge(self, obj):
        if obj.approval == ApprovalStatus.APPROVED:
            return badge("Live", "green")
        return badge("Awaiting approval", "orange")

    @admin.display(description="On site")
    def site_link(self, obj):
        if not hasattr(obj, "get_absolute_url") or not obj.public_path:
            return "—"
        label = "View" if obj.is_approved else "Preview"
        return format_html('<a href="{}" target="_blank" rel="noopener" class="ap-link">{} ↗</a>',
                           obj.get_absolute_url(), label)


# ── Private files ────────────────────────────────────────────────────────


class PrivateFileAdminMixin:
    """
    Serves a private FileField to staff with view permission, as a download.
    Files have no public URL; this view is the only way to fetch one.
    """

    private_file_fields: tuple[str, ...] = ()

    def get_urls(self):
        meta = self.model._meta
        return [
            path("<path:object_id>/file/<str:field>/", self.admin_site.admin_view(self.download_file),
                 name=f"{meta.app_label}_{meta.model_name}_file"),
            *super().get_urls(),
        ]

    def download_file(self, request, object_id, field):
        if field not in self.private_file_fields:
            raise Http404
        obj = get_object_or_404(self.model, pk=object_id)
        if not self.has_view_permission(request, obj):
            raise Http404
        fieldfile = getattr(obj, field)
        if not fieldfile:
            raise Http404
        name = getattr(obj, f"{field}_original_name", "") or getattr(obj, "original_name", "") or fieldfile.name
        return FileResponse(fieldfile.open("rb"), as_attachment=True, filename=name.rsplit("/", 1)[-1])

    def file_link(self, obj, field: str, label: str = "Download"):
        if not obj or not obj.pk or not getattr(obj, field):
            return "—"
        meta = self.model._meta
        url = reverse(f"admin:{meta.app_label}_{meta.model_name}_file", args=[obj.pk, field])
        return format_html('<a href="{}" class="ap-link">{}</a>', url, label)

