"""
Public content: what 3 Pillars does, where, for whom, and the proof.

Every model declares `cache_tags`: the Next.js cache tags a save invalidates
(see apps/core/revalidate.py). Children list their parent's tags so an inline
edit refreshes the page that shows it.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.core.fields import RichTextField
from apps.core.files import RandomName, document_validators
from apps.core.images import LOGO_VALIDATORS, PHOTO_HELP, photo_validators
from apps.core.models import Orderable, Publishable, Seo, Slugged, require_alt


class PillarColor(models.TextChoices):
    GREEN = "green", "Green (pillar 1)"
    BLUE = "blue", "Blue (pillar 2)"
    GREY = "grey", "Grey (pillar 3)"


ICON_HELP = "Icon name from lucide.dev, e.g. ClipboardCheck, Ruler, HardHat."


# ── Pillars ──────────────────────────────────────────────────────────────


class Pillar(Publishable):
    cache_tags = ("pillars", "home")

    name = models.CharField(max_length=80)
    name_ar = models.CharField("Name (Arabic)", max_length=80, blank=True)
    color = models.CharField(max_length=8, choices=PillarColor.choices)
    icon = models.CharField(max_length=40, blank=True, help_text=ICON_HELP)
    summary = models.CharField(max_length=200, help_text="One line shown under the name.")
    summary_ar = models.CharField("Summary (Arabic)", max_length=200, blank=True)
    detail = models.TextField(blank=True, help_text="A short paragraph shown when this pillar takes the stage.")
    detail_ar = models.TextField("Detail (Arabic)", blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "pillar"

    def __str__(self) -> str:
        return self.name


# ── Sectors ──────────────────────────────────────────────────────────────


class Sector(Publishable, Slugged, Seo):
    cache_tags = ("sectors", "home", "navigation")
    public_path = "/sectors/{slug}"

    name = models.CharField(max_length=120)
    name_ar = models.CharField("Name (Arabic)", max_length=120, blank=True)
    icon = models.CharField(max_length=40, blank=True, help_text=ICON_HELP)
    summary = models.CharField(max_length=240)
    summary_ar = models.CharField("Summary (Arabic)", max_length=240, blank=True)
    intro = RichTextField(blank=True)
    intro_ar = RichTextField("Intro (Arabic)", blank=True)
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
        require_alt(self, "image")


# ── Services ─────────────────────────────────────────────────────────────


class Service(Publishable, Slugged, Seo):
    cache_tags = ("services", "home", "navigation")
    public_path = "/services/{slug}"

    name = models.CharField(max_length=120)
    name_ar = models.CharField("Name (Arabic)", max_length=120, blank=True)
    icon = models.CharField(max_length=40, blank=True, help_text=ICON_HELP)
    summary = models.CharField(max_length=240, help_text="One or two lines for cards and menus.")
    summary_ar = models.CharField("Summary (Arabic)", max_length=240, blank=True)
    overview = RichTextField(blank=True)
    overview_ar = RichTextField("Overview (Arabic)", blank=True)
    featured = models.BooleanField(default=False, help_text="The flagship service takes the large cell on the home page.")
    sectors = models.ManyToManyField(Sector, blank=True, related_name="services")
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
        require_alt(self, "image")


class ServiceDeliverable(Orderable):
    cache_tags = ("services",)

    service = models.ForeignKey(Service, related_name="deliverables", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    text_ar = models.CharField("Text (Arabic)", max_length=200, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "deliverable"

    def __str__(self) -> str:
        return self.text


class ServiceStep(Orderable):
    cache_tags = ("services",)

    service = models.ForeignKey(Service, related_name="steps", on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    title_ar = models.CharField("Title (Arabic)", max_length=120, blank=True)
    body = models.TextField(blank=True)
    body_ar = models.TextField("Body (Arabic)", blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "delivery step"

    def __str__(self) -> str:
        return self.title


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


class Project(Publishable, Slugged, Seo):
    """A case study: Challenge → Approach → Outcome, with measured results."""

    cache_tags = ("projects", "home")
    public_path = "/projects/{slug}"

    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"

    title = models.CharField(max_length=160)
    title_ar = models.CharField("Title (Arabic)", max_length=160, blank=True)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL, related_name="projects")
    client_public_name = models.CharField(
        max_length=160, blank=True,
        help_text="How the client is named on the site, e.g. “A national utility”. Leave blank to use the client’s name.",
    )
    client_public_name_ar = models.CharField("Client public name (Arabic)", max_length=160, blank=True)
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
    role = models.CharField("Our role", max_length=160, blank=True)
    role_ar = models.CharField("Our role (Arabic)", max_length=160, blank=True)
    challenge = RichTextField(blank=True)
    challenge_ar = RichTextField("Challenge (Arabic)", blank=True)
    approach = RichTextField("Our approach", blank=True)
    approach_ar = RichTextField("Our approach (Arabic)", blank=True)
    outcome = RichTextField(blank=True)
    outcome_ar = RichTextField("Outcome (Arabic)", blank=True)
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

    def clean(self):
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


class LifecycleStage(Publishable):
    cache_tags = ("approach", "home")

    name = models.CharField(max_length=80)
    name_ar = models.CharField("Name (Arabic)", max_length=80, blank=True)
    icon = models.CharField(max_length=40, blank=True, help_text=ICON_HELP)
    summary = models.TextField()
    summary_ar = models.TextField("Summary (Arabic)", blank=True)
    deliverables = models.TextField(blank=True, help_text="Typical outputs of this stage, one per line.")
    deliverables_ar = models.TextField("Deliverables (Arabic)", blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "approach stage"

    def __str__(self) -> str:
        return self.name


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

    name = models.CharField(max_length=60)
    name_ar = models.CharField("Name (Arabic)", max_length=60, blank=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta(Orderable.Meta):
        verbose_name = "insight category"
        verbose_name_plural = "insight categories"

    def __str__(self) -> str:
        return self.name


class Insight(Publishable, Slugged, Seo):
    cache_tags = ("insights", "home")
    public_path = "/insights/{slug}"

    title = models.CharField(max_length=180)
    title_ar = models.CharField("Title (Arabic)", max_length=180, blank=True)
    category = models.ForeignKey(InsightCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="insights")
    excerpt = models.CharField(max_length=280)
    excerpt_ar = models.CharField("Excerpt (Arabic)", max_length=280, blank=True)
    body = RichTextField()
    body_ar = RichTextField("Body (Arabic)", blank=True)
    author = models.CharField(max_length=120, blank=True)
    author_ar = models.CharField("Author (Arabic)", max_length=120, blank=True)
    published_at = models.DateField(default=timezone.localdate)
    image = models.ImageField("Cover image", upload_to="insights/", blank=True, validators=photo_validators(), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)

    class Meta:
        ordering = ["-published_at", "-pk"]
        verbose_name = "insight"

    def __str__(self) -> str:
        return self.title

    def slug_source(self) -> str:
        return self.title

    def clean(self):
        require_alt(self, "image")


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
