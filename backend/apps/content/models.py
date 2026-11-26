"""
Public content: the three pillars, the services and sectors they cover, and
the evidence behind them.

Every model declares `cache_tags`: the Next.js cache tags a save invalidates
(see apps/core/revalidate.py). Children list their parent's tags so an inline
edit refreshes the page that shows it.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.core.fields import RichTextField
from apps.core.files import RandomName, document_validators, private_storage
from apps.core.images import LOGO_VALIDATORS, PHOTO_HELP, photo_validators
from apps.core.models import HeroBackground, Orderable, Publishable, PublishableQuerySet, Seo, Slugged, require_alt


class PillarColor(models.TextChoices):
    GREEN = "green", "Green (pillar 01)"
    BLUE = "blue", "Blue (pillar 02)"
    GREY = "grey", "Grey (pillar 03)"


ICON_HELP = "Icon name from lucide.dev, e.g. ClipboardCheck, ChartGantt, Building2."
NOTE_HELP = "Internal guidance for editors. Never shown on the site."


# ── Pillars ──────────────────────────────────────────────────────────────


class Pillar(Publishable):
    """A service line. The three pillars frame the home page, Our Approach and the services index."""

    cache_tags = ("pillars", "home", "services")

    class Role(models.TextChoices):
        LEAD = "lead", "Lead service line"
        ENABLING = "enabling", "Enabling pillar"

    number = models.PositiveSmallIntegerField(unique=True, help_text="Shown as 01, 02, 03.")
    name = models.CharField(max_length=120)
    name_ar = models.CharField("Name (Arabic)", max_length=120, blank=True)
    role_on_site = models.CharField("Role on the website", max_length=10, choices=Role.choices)
    color = models.CharField(max_length=8, choices=PillarColor.choices)
    core_value = models.CharField(max_length=240, blank=True, help_text="One line: the value this pillar brings.")
    core_value_ar = models.CharField("Core value (Arabic)", max_length=240, blank=True)
    summary = models.TextField(blank=True, help_text="Shown on the home page card.")
    summary_ar = models.TextField("Summary (Arabic)", blank=True)
    detail = models.TextField(blank=True, help_text="Shown on Our Approach.")
    detail_ar = models.TextField("Detail (Arabic)", blank=True)
    core_outcomes = models.TextField(blank=True)
    core_outcomes_ar = models.TextField("Core outcomes (Arabic)", blank=True)
    covers = models.TextField("What it covers", blank=True, help_text="Shown in the service-line table on the services page.")
    covers_ar = models.TextField("What it covers (Arabic)", blank=True)
    is_proposed = models.BooleanField(
        "Proposed", default=False,
        help_text="Not yet confirmed by management. Shows a “Proposed” tag on staging while content awaiting approval is visible.",
    )
    service = models.ForeignKey("Service", null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
                                help_text="The page the pillar card links to.")
    note = models.TextField("Editor note", blank=True, help_text=NOTE_HELP)

    class Meta(Publishable.Meta):
        verbose_name = "pillar"

    def __str__(self) -> str:
        return f"{self.number:02d} · {self.name}"


# ── Sectors ──────────────────────────────────────────────────────────────


class Sector(Publishable, Slugged, Seo, HeroBackground):
    cache_tags = ("sectors", "home", "navigation")
    public_path = "/sectors/{slug}/"

    name = models.CharField(max_length=120)
    name_ar = models.CharField("Name (Arabic)", max_length=120, blank=True)
    icon = models.CharField(max_length=40, blank=True, help_text=ICON_HELP)
    focus_summary = models.TextField("3 Pillars focus", blank=True, help_text="One or two lines for cards and the sectors table.")
    focus_summary_ar = models.TextField("3 Pillars focus (Arabic)", blank=True)
    intro = RichTextField(blank=True)
    intro_ar = RichTextField("Intro (Arabic)", blank=True)
    list_title = models.CharField(max_length=120, blank=True, help_text="Heading above the list, e.g. “Areas of focus”.")
    list_title_ar = models.CharField("List heading (Arabic)", max_length=120, blank=True)
    our_focus = models.TextField("Our focus", blank=True, help_text="Optional call-out shown after the list.")
    our_focus_ar = models.TextField("Our focus (Arabic)", blank=True)
    scope_caveat = models.TextField(blank=True, help_text="Small print under the list.")
    scope_caveat_ar = models.TextField("Scope caveat (Arabic)", blank=True)
    positioning_note = models.TextField(blank=True, help_text=NOTE_HELP)
    image = models.ImageField(upload_to="sectors/", blank=True, validators=photo_validators(), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "sector"

    def __str__(self) -> str:
        return self.name

    def slug_source(self) -> str:
        return self.name

    def clean(self):
        super().clean()
        require_alt(self, "image")

    @property
    def is_thin(self) -> bool:
        """No questions and nothing related to show: allowed, but flagged to editors."""
        return not self.faqs.exists() and not self.projects.exists() and not self.insights.exists()


class SectorListItem(Orderable):
    cache_tags = ("sectors",)

    sector = models.ForeignKey(Sector, related_name="list_items", on_delete=models.CASCADE)
    text = models.CharField(max_length=240)
    text_ar = models.CharField("Text (Arabic)", max_length=240, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "list item"

    def __str__(self) -> str:
        return self.text


class SectorFAQ(Orderable):
    cache_tags = ("sectors",)

    sector = models.ForeignKey(Sector, related_name="faqs", on_delete=models.CASCADE)
    question = models.CharField(max_length=240)
    question_ar = models.CharField("Question (Arabic)", max_length=240, blank=True)
    answer = models.TextField()
    answer_ar = models.TextField("Answer (Arabic)", blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "question"
        verbose_name_plural = "questions & answers"

    def __str__(self) -> str:
        return self.question


# ── Services ─────────────────────────────────────────────────────────────


class Service(Publishable, Slugged, Seo, HeroBackground):
    cache_tags = ("services", "home", "navigation")
    public_path = "/services/{slug}/"

    name = models.CharField(max_length=120)
    name_ar = models.CharField("Name (Arabic)", max_length=120, blank=True)
    pillar = models.ForeignKey(Pillar, null=True, blank=True, on_delete=models.SET_NULL, related_name="services")
    icon = models.CharField(max_length=40, blank=True, help_text=ICON_HELP)
    summary = models.CharField(max_length=240, blank=True, help_text="One or two lines for cards and menus.")
    summary_ar = models.CharField("Summary (Arabic)", max_length=240, blank=True)
    intro = RichTextField(blank=True)
    intro_ar = RichTextField("Intro (Arabic)", blank=True)
    capabilities_title = models.CharField(max_length=120, blank=True)
    capabilities_title_ar = models.CharField("Capabilities heading (Arabic)", max_length=120, blank=True)
    bullets_title = models.CharField(max_length=120, blank=True)
    bullets_title_ar = models.CharField("Bullet list heading (Arabic)", max_length=120, blank=True)
    scope_caveat = models.TextField(blank=True, help_text="Small print under the bullet list.")
    scope_caveat_ar = models.TextField("Scope caveat (Arabic)", blank=True)
    steps_title = models.CharField(max_length=120, blank=True)
    steps_title_ar = models.CharField("Process heading (Arabic)", max_length=120, blank=True)
    context_title = models.CharField("Extra section heading", max_length=120, blank=True)
    context_title_ar = models.CharField("Extra section heading (Arabic)", max_length=120, blank=True)
    context_body = models.TextField("Extra section text", blank=True)
    context_body_ar = models.TextField("Extra section text (Arabic)", blank=True)
    who_we_support = models.TextField(blank=True)
    who_we_support_ar = models.TextField("Who we support (Arabic)", blank=True)
    cta_headline = models.CharField("Call-to-action headline", max_length=160, blank=True)
    cta_headline_ar = models.CharField("Call-to-action headline (Arabic)", max_length=160, blank=True)
    cta_label = models.CharField("Call-to-action button", max_length=60, blank=True)
    cta_label_ar = models.CharField("Call-to-action button (Arabic)", max_length=60, blank=True)
    positioning_note = models.TextField(blank=True, help_text=NOTE_HELP)
    related_sectors = models.ManyToManyField(Sector, blank=True, related_name="related_services")
    image = models.ImageField("Cover image", upload_to="services/", blank=True, validators=photo_validators(), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "service"

    def __str__(self) -> str:
        return self.name

    def slug_source(self) -> str:
        return self.name

    def clean(self):
        super().clean()
        require_alt(self, "image")


class ServiceCapability(Orderable):
    cache_tags = ("services",)

    service = models.ForeignKey(Service, related_name="capabilities", on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    title_ar = models.CharField("Title (Arabic)", max_length=160, blank=True)
    description = models.TextField(blank=True)
    description_ar = models.TextField("Description (Arabic)", blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "capability"
        verbose_name_plural = "capabilities"

    def __str__(self) -> str:
        return self.title


class ServiceBullet(Orderable):
    cache_tags = ("services",)

    service = models.ForeignKey(Service, related_name="bullets", on_delete=models.CASCADE)
    text = models.CharField(max_length=240)
    text_ar = models.CharField("Text (Arabic)", max_length=240, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "bullet"

    def __str__(self) -> str:
        return self.text


class ServiceStep(Orderable):
    cache_tags = ("services",)

    service = models.ForeignKey(Service, related_name="steps", on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=True)
    title_ar = models.CharField("Title (Arabic)", max_length=120, blank=True)
    body = models.TextField(blank=True)
    body_ar = models.TextField("Body (Arabic)", blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "process step"

    def __str__(self) -> str:
        return self.title or self.body[:60]


class ServiceFAQ(Orderable):
    cache_tags = ("services",)

    service = models.ForeignKey(Service, related_name="faqs", on_delete=models.CASCADE)
    question = models.CharField(max_length=240)
    question_ar = models.CharField("Question (Arabic)", max_length=240, blank=True)
    answer = models.TextField()
    answer_ar = models.TextField("Answer (Arabic)", blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "question"
        verbose_name_plural = "questions & answers"

    def __str__(self) -> str:
        return self.question


# ── Clients ──────────────────────────────────────────────────────────────


class Client(Publishable):
    cache_tags = ("clients", "home", "projects")

    name = models.CharField(max_length=160)
    name_ar = models.CharField("Name (Arabic)", max_length=160, blank=True)
    kind = models.CharField(max_length=10, choices=[("client", "Client"), ("partner", "Partner")], default="client")
    logo = models.FileField(upload_to="clients/", blank=True, validators=LOGO_VALIDATORS,
                            help_text="SVG or transparent PNG. Needed to appear in the logo strip.")
    website = models.URLField(blank=True)
    show_in_trust_strip = models.BooleanField(
        "Show in the logo strip", default=False,
        help_text="Only with the client’s written permission to show their logo.",
    )

    class Meta(Publishable.Meta):
        verbose_name = "client or partner"
        verbose_name_plural = "clients & partners"

    def __str__(self) -> str:
        return self.name




# ── Projects ─────────────────────────────────────────────────────────────


class Project(Publishable, Slugged, Seo, HeroBackground):
    """
    A selected project or case study, with exact role attribution.

    The site always names the entity that delivered the work. A project can
    only be approved once someone has checked the evidence for that attribution.
    """

    cache_tags = ("projects", "home", "navigation")
    public_path = "/projects/{slug}/"

    class EntryType(models.TextChoices):
        SELECTED = "selected", "Selected project"
        CASE_STUDY = "case_study", "Case study"

    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"

    class Role(models.TextChoices):
        PROJECT_MANAGER = "project_manager", "Project manager"
        PMO_SUPPORT = "pmo_support", "PMO support"
        ADVISOR = "advisor", "Advisor"
        BD_SUPPORT = "bd_support", "Business development support"
        OTHER = "other", "Other"

    title = models.CharField(max_length=160)
    title_ar = models.CharField("Title (Arabic)", max_length=160, blank=True)
    entry_type = models.CharField("Type", max_length=12, choices=EntryType.choices, default=EntryType.SELECTED, db_index=True)
    delivery_entity = models.CharField(
        max_length=200, help_text="Who actually delivered the project. Always shown as “Delivered by”.",
    )
    delivery_entity_ar = models.CharField("Delivered by (Arabic)", max_length=200, blank=True)
    our_role = models.CharField(max_length=16, choices=Role.choices, db_index=True)
    our_role_detail = models.CharField(max_length=240, blank=True, help_text="The exact role, in a few words.")
    our_role_detail_ar = models.CharField("Role detail (Arabic)", max_length=240, blank=True)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL, related_name="projects")
    client_public_name = models.CharField(
        max_length=160, blank=True,
        help_text="How the client is named on the site, e.g. “A national utility”. Leave blank to use the client’s name.",
    )
    client_public_name_ar = models.CharField("Client public name (Arabic)", max_length=160, blank=True)
    client_name_approved = models.BooleanField(
        "Client agreed to be named", default=False, help_text="Without this, no client name is shown.",
    )
    summary = models.CharField(max_length=260)
    summary_ar = models.CharField("Summary (Arabic)", max_length=260, blank=True)
    location = models.CharField(max_length=120, blank=True)
    location_ar = models.CharField("Location (Arabic)", max_length=120, blank=True)
    country = models.CharField(max_length=60, blank=True, db_index=True)
    country_ar = models.CharField("Country (Arabic)", max_length=60, blank=True)
    sector = models.ForeignKey(Sector, null=True, blank=True, on_delete=models.SET_NULL, related_name="projects")
    services = models.ManyToManyField(Service, blank=True, related_name="projects")
    value = models.DecimalField(max_digits=14, decimal_places=0, null=True, blank=True)
    currency = models.CharField(max_length=3, default="USD")
    show_value = models.BooleanField("Show the value publicly", default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ONGOING, db_index=True)
    challenge = RichTextField("The challenge", blank=True)
    challenge_ar = RichTextField("The challenge (Arabic)", blank=True)
    scope_of_services = RichTextField(blank=True, help_text="Specific activities and deliverables completed by the 3 Pillars team.")
    scope_of_services_ar = RichTextField("Scope of services (Arabic)", blank=True)
    approach = RichTextField("Approach", blank=True)
    approach_ar = RichTextField("Approach (Arabic)", blank=True)
    results = RichTextField(blank=True, help_text="Verified outcomes only: milestones, quantified results or documented decisions.")
    results_ar = RichTextField("Results (Arabic)", blank=True)
    attribution_evidence = models.FileField(
        upload_to=RandomName("attribution"), storage=private_storage, blank=True,
        validators=document_validators(("pdf", "docx", "xlsx", "png", "jpg", "jpeg"), 10),
        help_text="Private: the record that shows who delivered the work and what 3 Pillars did.",
    )
    attribution_notes = models.TextField(blank=True, help_text="Private notes on the evidence.")
    attribution_approved = models.BooleanField(
        "Attribution confirmed", default=False,
        help_text="The delivery entity and 3 Pillars’ role are evidenced. Required before the project can be approved.",
    )
    featured = models.BooleanField(default=False, help_text="Featured projects appear on the home page.")
    image = models.ImageField("Hero image", upload_to="projects/", blank=True, validators=photo_validators(), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "project"

    def __str__(self) -> str:
        return self.title

    def slug_source(self) -> str:
        return self.title

    def approval_blocker(self) -> str | None:
        if not self.attribution_approved:
            return "Confirm the attribution (who delivered it and 3 Pillars’ exact role) before approving."
        return None

    def clean(self):
        super().clean()
        require_alt(self, "image")
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "The end date is before the start date."})

    @property
    def duration_months(self) -> int | None:
        if not self.start_date:
            return None
        end = self.end_date or timezone.localdate()
        return max(1, (end.year - self.start_date.year) * 12 + end.month - self.start_date.month)


class ProjectMetric(Orderable):
    cache_tags = ("projects", "home")

    project = models.ForeignKey(Project, related_name="metrics", on_delete=models.CASCADE)
    label = models.CharField(max_length=120)
    label_ar = models.CharField("Label (Arabic)", max_length=120, blank=True)
    value = models.CharField(max_length=24, help_text="e.g. 18 or 4.2")
    unit = models.CharField(max_length=24, blank=True, help_text="e.g. % or months")
    unit_ar = models.CharField("Unit (Arabic)", max_length=24, blank=True)
    delta = models.CharField(max_length=24, blank=True, help_text="Optional change, e.g. −12% or ahead of schedule.")
    delta_ar = models.CharField("Change (Arabic)", max_length=24, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "result"

    def __str__(self) -> str:
        return f"{self.label}: {self.value}{self.unit}"


class ProjectImage(Orderable):
    cache_tags = ("projects",)

    project = models.ForeignKey(Project, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/", validators=photo_validators(1000, 600), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200)
    caption = models.CharField(max_length=200, blank=True)
    caption_ar = models.CharField("Caption (Arabic)", max_length=200, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "gallery image"

    def __str__(self) -> str:
        return self.image_alt


# ── Proof ────────────────────────────────────────────────────────────────


class Testimonial(Publishable):
    """Real, attributable and approved only — never seeded."""

    cache_tags = ("testimonials", "home")

    quote = models.TextField()
    quote_ar = models.TextField("Quote (Arabic)", blank=True)
    person = models.CharField(max_length=120)
    person_ar = models.CharField("Person (Arabic)", max_length=120, blank=True)
    role = models.CharField(max_length=120, blank=True)
    role_ar = models.CharField("Role (Arabic)", max_length=120, blank=True)
    company = models.CharField(max_length=160, blank=True)
    company_ar = models.CharField("Company (Arabic)", max_length=160, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name="testimonials")
    photo = models.ImageField(upload_to="testimonials/", blank=True, validators=photo_validators(300, 300))
    photo_alt = models.CharField(max_length=200, blank=True)
    photo_alt_ar = models.CharField("Photo description (Arabic)", max_length=200, blank=True)
    permission_note = models.CharField(
        max_length=240, blank=True,
        help_text="Internal: who gave permission to publish this and when. Not shown on the site.",
    )

    class Meta(Publishable.Meta):
        verbose_name = "testimonial"

    def __str__(self) -> str:
        return f"{self.person}, {self.company}"

    def clean(self):
        require_alt(self, "photo")


class KPI(Publishable):
    cache_tags = ("kpis", "home")

    value = models.DecimalField(max_digits=10, decimal_places=1, help_text="The number that counts up, e.g. 25.")
    prefix = models.CharField(max_length=8, blank=True, help_text="e.g. $")
    suffix = models.CharField(max_length=12, blank=True, help_text="e.g. + or % or M")
    suffix_ar = models.CharField("Suffix (Arabic)", max_length=12, blank=True)
    label = models.CharField(max_length=120)
    label_ar = models.CharField("Label (Arabic)", max_length=120, blank=True)
    source = models.CharField(
        "Footnote / source", max_length=200,
        help_text="Where the number comes from and its date, e.g. “Company records, 2025”. Shown as a footnote.",
    )
    source_ar = models.CharField("Footnote (Arabic)", max_length=200, blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "key figure"

    def __str__(self) -> str:
        return f"{self.prefix}{self.value:g}{self.suffix} {self.label}"


class ApproachStep(Publishable):
    cache_tags = ("approach", "pages")

    name = models.CharField(max_length=120)
    name_ar = models.CharField("Name (Arabic)", max_length=120, blank=True)
    summary = models.TextField(blank=True)
    summary_ar = models.TextField("Summary (Arabic)", blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "approach step"

    def __str__(self) -> str:
        return self.name


class CompanyValue(Publishable):
    cache_tags = ("pages",)

    value = models.CharField(max_length=80)
    value_ar = models.CharField("Value (Arabic)", max_length=80, blank=True)
    in_practice = models.TextField("What it means in practice")
    in_practice_ar = models.TextField("What it means in practice (Arabic)", blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "company value"

    def __str__(self) -> str:
        return self.value


class ValuePoint(Publishable):
    """One of the “How we create value” columns on the home page."""

    cache_tags = ("home",)

    title = models.CharField(max_length=60)
    title_ar = models.CharField("Title (Arabic)", max_length=60, blank=True)
    body = models.TextField()
    body_ar = models.TextField("Text (Arabic)", blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "value point"

    def __str__(self) -> str:
        return self.title


# ── People and places ────────────────────────────────────────────────────


class TeamMember(Publishable):
    cache_tags = ("team",)

    name = models.CharField(max_length=120)
    name_ar = models.CharField("Name (Arabic)", max_length=120, blank=True)
    role = models.CharField(max_length=120)
    role_ar = models.CharField("Role (Arabic)", max_length=120, blank=True)
    bio = models.TextField(blank=True)
    bio_ar = models.TextField("Bio (Arabic)", blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, validators=photo_validators(600, 600))
    photo_alt = models.CharField(max_length=200, blank=True)
    photo_alt_ar = models.CharField("Photo description (Arabic)", max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    leadership = models.BooleanField(default=False, help_text="Leadership appears on the About page.")

    class Meta(Publishable.Meta):
        verbose_name = "team member"

    def __str__(self) -> str:
        return self.name

    def clean(self):
        require_alt(self, "photo")


class Office(Publishable):
    cache_tags = ("offices", "settings")

    city = models.CharField(max_length=80)
    city_ar = models.CharField("City (Arabic)", max_length=80, blank=True)
    country = models.CharField(max_length=60)
    country_ar = models.CharField("Country (Arabic)", max_length=60, blank=True)
    address = models.TextField(blank=True)
    address_ar = models.TextField("Address (Arabic)", blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_image = models.ImageField(
        "Static map image", upload_to="offices/", blank=True, validators=photo_validators(800, 400),
        help_text="A screenshot of the map. The live map loads only when a visitor asks for it.",
    )
    map_image_alt = models.CharField(max_length=200, blank=True)
    map_image_alt_ar = models.CharField("Map description (Arabic)", max_length=200, blank=True)
    is_headquarters = models.BooleanField(default=False)

    class Meta(Publishable.Meta):
        verbose_name = "office"

    def __str__(self) -> str:
        return f"{self.city}, {self.country}"

    def clean(self):
        require_alt(self, "map_image")


class Certification(Publishable):
    cache_tags = ("certifications",)

    name = models.CharField(max_length=160)
    name_ar = models.CharField("Name (Arabic)", max_length=160, blank=True)
    issuer = models.CharField(max_length=160)
    issuer_ar = models.CharField("Issuer (Arabic)", max_length=160, blank=True)
    kind = models.CharField(max_length=14, choices=[("certification", "Certification"), ("membership", "Membership")],
                            default="certification")
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    logo = models.FileField(upload_to="certifications/", blank=True, validators=LOGO_VALIDATORS)
    evidence_note = models.CharField(max_length=240, blank=True,
                                     help_text="Internal: certificate number or where the proof is kept.")

    class Meta(Publishable.Meta):
        verbose_name = "certification or membership"
        verbose_name_plural = "certifications & memberships"

    def __str__(self) -> str:
        return self.name


# ── Insights ─────────────────────────────────────────────────────────────


class InsightCategory(Orderable):
    cache_tags = ("insights",)

    name = models.CharField(max_length=80)
    name_ar = models.CharField("Name (Arabic)", max_length=80, blank=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta(Orderable.Meta):
        verbose_name = "insight category"
        verbose_name_plural = "insight categories"

    def __str__(self) -> str:
        return self.name


class InsightQuerySet(PublishableQuerySet):
    """An insight without a body is a planned topic: never public, even on staging."""

    def written(self):
        return self.exclude(body="")

    def approved(self):
        return super().approved().written()

    def visible(self, *, include_pending: bool):
        return self.written() if include_pending else self.approved()


class Insight(Publishable, Slugged, Seo, HeroBackground):
    cache_tags = ("insights", "home", "sectors")
    public_path = "/insights/{slug}/"

    class Kind(models.TextChoices):
        ARTICLE = "article", "Article"
        PERSPECTIVE = "perspective", "Market perspective"
        DELIVERY = "delivery", "Project delivery insight"
        NEWS = "news", "News"

    title = models.CharField(max_length=180)
    title_ar = models.CharField("Title (Arabic)", max_length=180, blank=True)
    kind = models.CharField(max_length=12, choices=Kind.choices, default=Kind.ARTICLE, db_index=True)
    category = models.ForeignKey(InsightCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="insights")
    sectors = models.ManyToManyField(Sector, blank=True, related_name="insights")
    is_draft_topic = models.BooleanField(
        "Planned topic", default=False,
        help_text="A suggested topic still to be written. Hidden everywhere until it has a body.",
    )
    excerpt = models.CharField("Summary", max_length=280, blank=True)
    excerpt_ar = models.CharField("Summary (Arabic)", max_length=280, blank=True)
    our_role_statement = models.TextField(
        "3 Pillars’ role", blank=True,
        help_text="News only: a factual description of 3 Pillars’ role in what is announced.",
    )
    our_role_statement_ar = models.TextField("3 Pillars’ role (Arabic)", blank=True)
    body = RichTextField(blank=True)
    body_ar = RichTextField("Body (Arabic)", blank=True)
    author = models.CharField(max_length=120, blank=True)
    author_ar = models.CharField("Author (Arabic)", max_length=120, blank=True)
    published_at = models.DateField(null=True, blank=True, default=timezone.localdate)
    image = models.ImageField("Cover image", upload_to="insights/", blank=True, validators=photo_validators(), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)

    objects = InsightQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at", "-pk"]
        verbose_name = "insight"

    def __str__(self) -> str:
        return self.title

    def slug_source(self) -> str:
        return self.title

    def approval_blocker(self) -> str | None:
        if not self.body.strip():
            return "Write the article before approving it."
        if self.kind == self.Kind.NEWS:
            missing = [label for label, value in (("publication date", self.published_at), ("summary", self.excerpt),
                                                  ("3 Pillars’ role", self.our_role_statement)) if not value]
            if missing:
                return f"News needs a {', '.join(missing)} before it can be approved."
        return None

    def clean(self):
        super().clean()
        require_alt(self, "image")
        if self.kind == self.Kind.NEWS and self.body.strip():
            errors = {}
            if not self.published_at:
                errors["published_at"] = "News needs a publication date."
            if not self.excerpt:
                errors["excerpt"] = "News needs a concise summary."
            if not self.our_role_statement:
                errors["our_role_statement"] = "Describe 3 Pillars’ role factually."
            if errors:
                raise ValidationError(errors)


# ── Downloads ────────────────────────────────────────────────────────────


class Download(Publishable, Slugged):
    cache_tags = ("downloads",)

    title = models.CharField(max_length=140)
    title_ar = models.CharField("Title (Arabic)", max_length=140, blank=True)
    description = models.CharField(max_length=240, blank=True)
    description_ar = models.CharField("Description (Arabic)", max_length=240, blank=True)
    file = models.FileField("PDF (English)", upload_to=RandomName("downloads"), validators=document_validators(("pdf",), 25))
    file_ar = models.FileField("PDF (Arabic)", upload_to=RandomName("downloads"), blank=True,
                               validators=document_validators(("pdf",), 25))
    gated = models.BooleanField(
        "Ask for contact details first", default=False,
        help_text="Visitors give name, email and company before the download starts. Each one is saved as a download lead.",
    )
    is_capability_statement = models.BooleanField(
        default=False, help_text="The document linked from every “Download capability statement” button.",
    )

    class Meta(Publishable.Meta):
        verbose_name = "download"

    def __str__(self) -> str:
        return self.title

    def slug_source(self) -> str:
        return self.title

    def requires_lead(self) -> bool:
        from apps.core.models import SiteSettings

        return self.gated or (self.is_capability_statement and SiteSettings.load().capability_gate)
