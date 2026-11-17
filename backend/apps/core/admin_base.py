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

APPROVE_PERMISSION = "core.approve_content"


def tab(title: str, *fields, description: str = "") -> tuple:
    options = {"classes": ["tab"], "fields": list(fields)}
    if description:
        options["description"] = description
    return (title, options)


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
        return format_html('<span class="text-base-400">No image yet</span>')
    return format_html(
        '<img src="{}" alt="" style="max-height:{}px;max-width:{}px;object-fit:cover;border-radius:10px;'
        'border:1px solid rgb(25 23 71 / .1)">',
        payload["src"], size * 3 // 4, size * 3 // 2,
    )


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


@admin.action(description="Approve for publication", permissions=["approve"])
def approve(modeladmin, request, queryset):
    count = 0
    for obj in queryset:
        obj.approval = ApprovalStatus.APPROVED
        obj.save(update_fields=["approval", "updated_at"])
        count += 1
    modeladmin.message_user(request, f"{count} item(s) approved and live within seconds.", messages.SUCCESS)


@admin.action(description="Unpublish (back to awaiting approval)", permissions=["approve"])
def unpublish(modeladmin, request, queryset):
    count = 0
    for obj in queryset:
        obj.approval = ApprovalStatus.PENDING
        obj.save(update_fields=["approval", "updated_at"])
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

    def has_approve_permission(self, request):
        return request.user.has_perm(APPROVE_PERMISSION)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if not self.has_approve_permission(request):
            fields.append("approval")
        return fields

    def get_list_filter(self, request):
        return ["approval", *super().get_list_filter(request)]

    @admin.display(description="Status", ordering="approval")
    def status_badge(self, obj):
        live = obj.approval == ApprovalStatus.APPROVED
        return format_html(
            '<span style="display:inline-block;padding:2px 10px;border-radius:999px;font-size:11px;'
            'font-weight:600;background:{};color:{}">{}</span>',
            "#F0FAF2" if live else "#FFF8EB",
            "#044B22" if live else "#8A5300",
            "Live" if live else "Awaiting approval",
        )

    @admin.display(description="On site")
    def site_link(self, obj):
        if not hasattr(obj, "get_absolute_url") or not obj.public_path:
            return "—"
        label = "View" if obj.is_approved else "Preview"
        return format_html('<a href="{}" target="_blank" rel="noopener" class="text-primary-600">{} ↗</a>',
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
        return format_html('<a href="{}" class="text-primary-600 font-semibold">{}</a>', url, label)

