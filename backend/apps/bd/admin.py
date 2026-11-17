from django.contrib import admin, messages
from django.http import FileResponse, Http404
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from apps.core.admin_base import BaseAdmin, BaseStackedInline

from .models import OPEN_STAGES, DownloadLead, Enquiry, EnquiryNote, ProposalAttachment, ProposalNote, ProposalRequest, Stage

STAGE_COLORS = {
    Stage.NEW: ("#F1F7FF", "#014888"),
    Stage.QUALIFIED: ("#FFF8EB", "#8A5300"),
    Stage.PROPOSAL_SENT: ("#DEE0ED", "#191747"),
    Stage.WON: ("#F0FAF2", "#044B22"),
    Stage.LOST: ("#E5E6E6", "#454648"),
}

SUBMITTED = ["name", "organisation", "role", "email", "phone", "country", "locale", "source_page",
             "utm_source", "utm_medium", "utm_campaign", "consent", "submitted_at"]


class OverdueFilter(admin.SimpleListFilter):
    title = "follow-up"
    parameter_name = "follow_up"

    def lookups(self, request, model_admin):
        return [("overdue", "Overdue"), ("today", "Due today"), ("none", "No date set")]

    def queryset(self, request, queryset):
        today = timezone.localdate()
        if self.value() == "overdue":
            return queryset.filter(next_follow_up__lt=today, stage__in=OPEN_STAGES)
        if self.value() == "today":
            return queryset.filter(next_follow_up=today)
        if self.value() == "none":
            return queryset.filter(next_follow_up__isnull=True, stage__in=OPEN_STAGES)
        return queryset


def stage_action(stage):
    @admin.action(description=f"Move to “{stage.label}”")
    def action(modeladmin, request, queryset):
        updated = queryset.update(stage=stage)
        modeladmin.message_user(request, f"{updated} moved to {stage.label}.", messages.SUCCESS)

    action.__name__ = f"move_to_{stage.value}"
    return action


@admin.action(description="Assign to me")
def assign_to_me(modeladmin, request, queryset):
    updated = queryset.update(owner=request.user)
    modeladmin.message_user(request, f"{updated} assigned to you.")


@admin.action(description="Mark as handled")
def mark_handled(modeladmin, request, queryset):
    updated = queryset.update(is_handled=True)
    modeladmin.message_user(request, f"{updated} marked as handled.")


class NoteInline(BaseStackedInline):
    fields = ["body", "author", "created_at"]
    readonly_fields = ["author", "created_at"]
    extra = 1
    ordering_field = None
    hide_ordering_field = False
    verbose_name_plural = "internal notes (never shown to the sender)"

    def has_change_permission(self, request, obj=None):
        return False


class LeadAdmin(BaseAdmin):
    """Submitted fields are a record and stay read-only; the pipeline is editable."""

    list_filter = ["stage", "is_handled", OverdueFilter, "owner", "locale", "submitted_at"]
    date_hierarchy = "submitted_at"
    list_editable = []
    actions = [assign_to_me, mark_handled, *(stage_action(s) for s in Stage)]
    pipeline = ("Pipeline", {"fields": [("stage", "owner"), ("next_follow_up", "is_handled")]})

    def has_add_permission(self, request):
        return False

    def save_formset(self, request, form, formset, change):
        for note in formset.save(commit=False):
            if not note.author_id:
                note.author = request.user
            note.save()

    @admin.display(description="Stage", ordering="stage")
    def stage_badge(self, obj):
        bg, fg = STAGE_COLORS[obj.stage]
        return format_html('<span style="padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600;'
                           'background:{};color:{}">{}</span>', bg, fg, obj.get_stage_display())

    @admin.display(description="Follow up", ordering="next_follow_up")
    def follow_up(self, obj):
        if not obj.next_follow_up:
            return "—"
        overdue = obj.next_follow_up < timezone.localdate() and obj.stage in OPEN_STAGES
        return format_html('<span style="color:{};font-weight:{}">{}</span>', "#B42318" if overdue else "inherit",
                           600 if overdue else 400, obj.next_follow_up.strftime("%d %b %Y"))

    @admin.display(description="Handled", boolean=True, ordering="is_handled")
    def handled(self, obj):
        return obj.is_handled


class EnquiryNoteInline(NoteInline):
    model = EnquiryNote


@admin.register(Enquiry)
class EnquiryAdmin(LeadAdmin):
    list_display = ["submitted_at", "who", "topic", "email", "stage_badge", "owner", "follow_up", "handled"]
    list_filter = ["topic", *LeadAdmin.list_filter]
    search_fields = ["name", "organisation", "email", "subject", "message"]
    readonly_fields = [*SUBMITTED, "topic", "subject", "message"]
    inlines = [EnquiryNoteInline]
    fieldsets = [
        LeadAdmin.pipeline,
        ("Message", {"fields": ["topic", "subject", "message"]}),
        ("From", {"fields": [("name", "organisation"), ("role", "country"), ("email", "phone")]}),
        ("Source", {"classes": ["collapse"], "fields": ["submitted_at", "locale", "source_page",
                                                         ("utm_source", "utm_medium", "utm_campaign"), "consent"]}),
    ]


class ProposalNoteInline(NoteInline):
    model = ProposalNote


class AttachmentInline(BaseStackedInline):
    model = ProposalAttachment
    fields = ["original_name", "download"]
    readonly_fields = ["original_name", "download"]
    ordering_field = None
    hide_ordering_field = False
    verbose_name_plural = "attachments (private)"

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description="File")
    def download(self, obj):
        url = reverse("admin:bd_proposalrequest_attachment", args=[obj.request_id, obj.pk])
        return format_html('<a href="{}" class="text-primary-600 font-semibold">Download</a>', url)


@admin.register(ProposalRequest)
class ProposalRequestAdmin(LeadAdmin):
    list_display = ["submitted_at", "who", "project_type", "sector", "budget", "stage_badge", "owner", "follow_up",
                    "handled"]
    list_filter = ["sector", "project_stage", "budget", *LeadAdmin.list_filter]
    search_fields = ["name", "organisation", "email", "project_type", "location", "scope"]
    readonly_fields = [*SUBMITTED, "organisation_type", "project_type", "sector", "services_list", "location",
                       "project_stage", "budget", "timeline", "scope"]
    inlines = [AttachmentInline, ProposalNoteInline]
    fieldsets = [
        LeadAdmin.pipeline,
        ("Project", {"fields": ["project_type", ("sector", "services_list"), "location",
                                ("project_stage", "budget", "timeline"), "scope"]}),
        ("From", {"fields": [("name", "organisation", "organisation_type"), ("role", "country"), ("email", "phone")]}),
        ("Source", {"classes": ["collapse"], "fields": ["submitted_at", "locale", "source_page",
                                                         ("utm_source", "utm_medium", "utm_campaign"), "consent"]}),
    ]

    def get_urls(self):
        return [
            path("<int:request_id>/attachment/<int:pk>/", self.admin_site.admin_view(self.attachment),
                 name="bd_proposalrequest_attachment"),
            *super().get_urls(),
        ]

    def attachment(self, request, request_id, pk):
        attachment = ProposalAttachment.objects.filter(pk=pk, request_id=request_id).first()
        if not attachment or not self.has_view_permission(request, attachment.request):
            raise Http404
        return FileResponse(attachment.file.open("rb"), as_attachment=True, filename=attachment.original_name)

    @admin.display(description="Services")
    def services_list(self, obj):
        return ", ".join(s.name for s in obj.services.all()) or "—"


@admin.register(DownloadLead)
class DownloadLeadAdmin(BaseAdmin):
    list_display = ["submitted_at", "name", "company", "email", "download", "is_handled"]
    list_filter = ["download", "is_handled", "submitted_at"]
    list_editable = ["is_handled"]
    search_fields = ["name", "email", "company"]
    readonly_fields = ["download", "name", "email", "company", "locale", "source_page", "submitted_at"]
    fields = [*readonly_fields, "is_handled"]

    def has_add_permission(self, request):
        return False
