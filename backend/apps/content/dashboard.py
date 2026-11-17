"""
The admin landing page, declared through adminkit.

Three questions on login: what is waiting for a human, where the pipeline
stands, and how much content exists. Every card links to the changelist
filtered to exactly the rows it counts.
"""

from dataclasses import dataclass, field
from typing import Callable

from django.db.models import Q

from adminkit.dashboard import TONES, Attention, Dashboard, Recent, Tile, changelist_url
from apps.bd.models import Enquiry, ProposalRequest, Stage
from apps.careers.models import Application, Job
from apps.core.models import ApprovalStatus

from .models import KPI, Client, Insight, Pillar, Project, Sector, Service, TeamMember, Testimonial

PENDING = {"approval": ApprovalStatus.PENDING}


@dataclass
class FilterAttention(Attention):
    """
    A card counted by a queryset function and linked to a custom list filter
    (one an ORM `where` dict cannot express, like "overdue").
    """

    count: Callable = field(default=lambda qs: qs)
    query: str = ""

    def render(self, index):
        url = changelist_url(self.model)
        return {
            "label": self.label,
            "value": self.count(self.model._default_manager.all()).count(),
            "total": self.model._default_manager.count(),
            "url": f"{url}?{self.query}" if url else None,
            "tone": self.tone or TONES[index % len(TONES)],
        }


def overdue(model, label):
    return FilterAttention(model, label, count=lambda qs: qs.overdue(), query="follow_up=overdue")


MISSING_ALT = Q(image_alt="") | Q(image_alt_ar="")

dashboard_callback = Dashboard(
    attention=[
        Attention(ProposalRequest, "New proposal requests", where={"stage": Stage.NEW}),
        Attention(Enquiry, "Unhandled enquiries", where={"is_handled": False}),
        overdue(ProposalRequest, "Proposals past follow-up"),
        overdue(Enquiry, "Enquiries past follow-up"),
        Attention(Application, "Unhandled applications", where={"is_handled": False}),
        Attention(Project, "Projects without a hero image", where={"image": ""}),
        FilterAttention(Project, "Project images missing a description",
                        count=lambda qs: qs.exclude(image="").filter(MISSING_ALT), query="media=missing_alt"),
        *[
            Attention(model, f"{str(model._meta.verbose_name_plural).capitalize()} awaiting approval", where=PENDING)
            for model in (Service, Sector, Project, Pillar, KPI, Insight, Client, Testimonial, TeamMember)
        ],
    ],
    tiles=[
        Tile(ProposalRequest, "Pipeline · New", where={"stage": Stage.NEW}),
        Tile(ProposalRequest, "Pipeline · Qualified", where={"stage": Stage.QUALIFIED}),
        Tile(ProposalRequest, "Pipeline · Proposal sent", where={"stage": Stage.PROPOSAL_SENT}),
        Tile(ProposalRequest, "Pipeline · Won", where={"stage": Stage.WON}),
        Tile(Service, "Services"),
        Tile(Project, "Projects"),
        Tile(Insight, "Insights"),
        Tile(Job, "Open jobs", where={"is_open": True}),
    ],
    recent=Recent(
        ProposalRequest,
        order_by="-submitted_at",
        title="Latest proposal requests",
        label_field="__str__",
        meta_field="organisation",
        date_field="submitted_at",
        unread_field="is_handled",
    ),
    greeting="Welcome back, {name}.",
    tiles_title="Pipeline & content",
    attention_title="Needs attention",
).as_callback()
