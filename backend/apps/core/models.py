"""
Site-wide models and the abstract bases every content app builds on.

Two rules are enforced here rather than left to each view:

1. **The approval gate.** Every publishable row carries `approval`. The API
   serves approved rows only, unless Site settings → "Show content awaiting
   approval" is on (staging). Seed and placeholder content is always pending.

2. **Bilingual content.** Every editor-facing text field `x` has a twin
   `x_ar`. Arabic is optional so content entry is never blocked; the API falls
   back to English and reports which fields fell back.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from .fields import RichTextField
from .files import video_validators
from .images import LOGO_VALIDATORS, PHOTO_HELP, photo_validators


class ApprovalStatus(models.TextChoices):
    PENDING = "pending", "Awaiting approval"
    APPROVED = "approved", "Approved for publication"


# ── Abstract bases ───────────────────────────────────────────────────────


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Orderable(models.Model):
    order = models.PositiveIntegerField(default=0, db_index=True, help_text="Drag rows in the list to reorder.")

    class Meta:
        abstract = True
        ordering = ["order", "pk"]


class PublishableQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(approval=ApprovalStatus.APPROVED)

    def visible(self, *, include_pending: bool):
        return self if include_pending else self.approved()

    def arabic_indexable(self):
        """Approved and with a reviewed translation: the only Arabic pages search engines may see."""
        return self.approved().filter(ar_reviewed=True)


class Publishable(TimeStamped, Orderable):
    approval = models.CharField(
        max_length=16,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
        db_index=True,
        help_text=(
            "Only approved items appear on the live site. Items awaiting approval "
            "are visible on staging when 'Show content awaiting approval' is on."
        ),
    )
    ar_reviewed = models.BooleanField(
        "Arabic reviewed", default=False,
        help_text="Tick once a fluent reviewer has checked the Arabic. Until then the Arabic page is hidden from search engines.",
    )

    objects = PublishableQuerySet.as_manager()

    class Meta(Orderable.Meta):
        abstract = True

    @property
    def is_approved(self) -> bool:
        return self.approval == ApprovalStatus.APPROVED

    def approval_blocker(self) -> str | None:
        """Why this row cannot be approved yet, or None. Checked by clean() and the Approve action."""
        return None

    def clean(self):
        super().clean()
        if self.approval == ApprovalStatus.APPROVED and (reason := self.approval_blocker()):
            raise ValidationError({"approval": reason})


class Slugged(models.Model):
    """
    A URL slug made from the English title, editable, and unique.

    Changing the slug of a saved row records a Redirect from the old path, so
    links already shared or indexed keep working.
    """

    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        help_text="The page address. Filled in from the English title; changing it keeps the old address working.",
    )

    #: e.g. "/services/{slug}/". Locale prefixes are added by the website.
    public_path = ""

    class Meta:
        abstract = True

    def slug_source(self) -> str:
        return str(self)

    def get_public_path(self) -> str:
        return self.public_path.format(slug=self.slug)

    def get_absolute_url(self) -> str:
        return f"{settings.SITE_URL.rstrip('/')}/en{self.get_public_path()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug(slugify(self.slug_source())[:130] or "item")
        previous = None
        if self.pk and self.public_path:
            previous = type(self).objects.filter(pk=self.pk).values_list("slug", flat=True).first()
        super().save(*args, **kwargs)
        if previous and previous != self.slug:
            old = self.public_path.format(slug=previous)
            new = self.get_public_path()
            Redirect.objects.filter(old_path=new).delete()
            Redirect.objects.update_or_create(old_path=old, defaults={"new_path": new, "permanent": True})
            # Collapse chains: anything pointing at the old path now goes direct.
            Redirect.objects.filter(new_path=old).update(new_path=new)

    def _unique_slug(self, base: str) -> str:
        candidate, n = base, 2
        while type(self).objects.filter(slug=candidate).exclude(pk=self.pk).exists():
            candidate = f"{base}-{n}"
            n += 1
        return candidate


class Seo(models.Model):
    seo_title = models.CharField("SEO title", max_length=70, blank=True,
                                 help_text="Shown in Google results and browser tabs. Aim for 60 characters or fewer.")
    seo_title_ar = models.CharField("SEO title (Arabic)", max_length=70, blank=True)
    meta_description = models.CharField("Meta description", max_length=160, blank=True,
                                        help_text="One or two sentences shown under the title in search results. 160 characters at most.")
    meta_description_ar = models.CharField("Meta description (Arabic)", max_length=160, blank=True)
    h1 = models.CharField("Page heading (H1)", max_length=140, blank=True,
                          help_text="The one main heading search engines read. Leave blank to use the title.")
    h1_ar = models.CharField("Page heading (Arabic)", max_length=140, blank=True)
    primary_keyword = models.CharField(
        max_length=120, blank=True,
        help_text="Editor guidance only: the search phrase this page answers. Never output as a meta tag.",
    )
    supporting_keywords = models.CharField(
        max_length=400, blank=True,
        help_text="Editor guidance only: related phrases, separated by commas.",
    )
    og_image = models.ImageField(
        "Share image", upload_to="og/", blank=True, validators=photo_validators(1200, 630),
        help_text="Shown when the page is shared on LinkedIn or WhatsApp (1200×630). Leave blank to generate one.",
    )

    class Meta:
        abstract = True


HERO_HELP = (
    "The photograph behind the page title, at least 1600 × 900. It is decorative (darkened behind the white "
    "title), so it needs no description. Leave blank to use the default in Site settings."
)


class HeroBackground(models.Model):
    """The background image of a page's opening (hero) band."""

    hero_image = models.ImageField("Hero background", upload_to="heroes/", blank=True,
                                   validators=photo_validators(1600, 900), help_text=HERO_HELP)

    class Meta:
        abstract = True


def require_alt(instance, *fields: str) -> None:
    """
    Every uploaded image needs English and Arabic alt text (accessibility), and
    the text must describe the image rather than repeat the page's keyword.
    """
    keyword = (getattr(instance, "primary_keyword", "") or "").strip().casefold()
    errors = {}
    for field in fields:
        if getattr(instance, field, None):
            alt = getattr(instance, f"{field}_alt", "")
            if not alt:
                errors[f"{field}_alt"] = "Describe the image for people using screen readers."
            elif keyword and alt.strip().casefold() == keyword:
                errors[f"{field}_alt"] = "Describe what the image shows; the page’s keyword is not a description."
            if not getattr(instance, f"{field}_alt_ar", ""):
                errors[f"{field}_alt_ar"] = "Arabic description of the image is required."
    if errors:
        raise ValidationError(errors)


# ── Site settings ────────────────────────────────────────────────────────


class SiteSettings(TimeStamped):
    """Singleton for site-wide values, the hero, and the publication switches."""

    #: The switches decide what every page may show (pending content, coming soon), so a
    #: save expires everything: a cached page must never outlive the gate that hid it.
    cache_tags = ("settings", "home", "navigation", "pillars", "services", "sectors", "projects", "insights", "pages",
                  "team", "offices", "certifications", "downloads", "jobs", "kpis", "clients", "testimonials", "approach")

    company_name = models.CharField(max_length=120, default="3 Pillars Project Management Services")
    company_name_ar = models.CharField("Company name (Arabic)", max_length=120, blank=True)
    short_name = models.CharField(max_length=60, default="3 Pillars")
    short_name_ar = models.CharField("Short name (Arabic)", max_length=60, blank=True)
    tagline = models.CharField("Positioning statement", max_length=300, blank=True,
                               help_text="One sentence. Also used as the organisation description for search engines.")
    tagline_ar = models.CharField("Positioning statement (Arabic)", max_length=300, blank=True)
    group_relationship = models.CharField(
        max_length=240, blank=True,
        help_text="How 3 Pillars relates to HS Group, stated exactly as approved. Never present group credentials as 3 Pillars’ own.",
    )
    group_relationship_ar = models.CharField("Group relationship (Arabic)", max_length=240, blank=True)

    logo_light = models.FileField("Logo for light backgrounds", upload_to="brand/", blank=True, validators=LOGO_VALIDATORS,
                                  help_text="SVG or PNG. Leave blank to use the built-in CI logo.")
    logo_dark = models.FileField("Logo for navy backgrounds", upload_to="brand/", blank=True, validators=LOGO_VALIDATORS)
    favicon = models.FileField(upload_to="brand/", blank=True, validators=LOGO_VALIDATORS)

    # Hero
    hero_eyebrow = models.CharField(max_length=100, blank=True)
    hero_eyebrow_ar = models.CharField("Eyebrow (Arabic)", max_length=100, blank=True)
    hero_headline = models.CharField("Display headline", max_length=120, blank=True,
                                     help_text="The large line. Search engines read the home page heading (H1) instead.")
    hero_headline_ar = models.CharField("Display headline (Arabic)", max_length=120, blank=True)
    hero_subline = models.TextField("Supporting copy", blank=True)
    hero_subline_ar = models.TextField("Supporting copy (Arabic)", blank=True)
    hero_primary_label = models.CharField(max_length=40, blank=True)
    hero_primary_label_ar = models.CharField("Primary button (Arabic)", max_length=40, blank=True)
    hero_primary_link = models.CharField(max_length=200, default="/services/")
    hero_secondary_label = models.CharField(max_length=40, blank=True)
    hero_secondary_label_ar = models.CharField("Secondary button (Arabic)", max_length=40, blank=True)
    hero_secondary_link = models.CharField(max_length=200, default="/contact/request-a-consultation/")
    hero_video = models.FileField(
        "Video (desktop MP4)", upload_to="hero/", blank=True, validators=video_validators(8),
        help_text="H.264 MP4, 1080p, up to 8 MB, a 10–20 second seamless loop with no sound.",
    )
    hero_video_webm = models.FileField("Video (desktop WebM, optional)", upload_to="hero/", blank=True,
                                       validators=video_validators(8, ("webm",)))
    hero_video_mobile = models.FileField(
        "Video (mobile MP4)", upload_to="hero/", blank=True, validators=video_validators(4),
        help_text="720p, portrait or a centred crop, up to 4 MB.",
    )
    hero_poster = models.ImageField(
        "Poster image", upload_to="hero/", blank=True, validators=photo_validators(1600, 900),
        help_text="Required with a video. Shown while the video loads, to visitors who prefer reduced motion, and on its own when there is no video.",
    )
    hero_poster_mobile = models.ImageField(
        "Poster image (mobile)", upload_to="hero/", blank=True, validators=photo_validators(720, 1280),
        help_text="Optional. A portrait still of the mobile video, at least 720 × 1280. Phones use the desktop poster when this is empty.",
    )
    default_hero_image = models.ImageField(
        "Default page hero background", upload_to="heroes/", blank=True, validators=photo_validators(1600, 900),
        help_text="Behind the title of every page that has no hero background of its own. Decorative, at least 1600 × 900.",
    )
    hero_poster_alt = models.CharField("Poster description", max_length=200, blank=True)
    hero_poster_alt_ar = models.CharField("Poster description (Arabic)", max_length=200, blank=True)

    # Contact
    contact_verified = models.BooleanField(
        "Contact details verified", default=False,
        help_text="Tick only once every filled-in detail below is confirmed as an official 3 Pillars channel. "
                  "Until then no address, phone, email or opening hours are shown on the site.",
    )
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True, help_text="International format, digits only, e.g. 967700000000.")
    show_whatsapp = models.BooleanField("Show WhatsApp button", default=False)
    address = models.TextField(blank=True)
    address_ar = models.TextField("Address (Arabic)", blank=True)
    business_hours = models.CharField(max_length=120, blank=True)
    business_hours_ar = models.CharField("Business hours (Arabic)", max_length=120, blank=True)
    linkedin = models.URLField(blank=True)
    x_twitter = models.URLField("X (Twitter)", blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    # SEO + analytics
    seo_title = models.CharField("Default SEO title", max_length=70, blank=True)
    seo_title_ar = models.CharField("Default SEO title (Arabic)", max_length=70, blank=True)
    seo_description = models.CharField("Default SEO description", max_length=160, blank=True)
    seo_description_ar = models.CharField("Default SEO description (Arabic)", max_length=160, blank=True)
    og_image = models.ImageField("Default share image", upload_to="og/", blank=True, validators=photo_validators(1200, 630))
    home_seo_title = models.CharField("Home SEO title", max_length=70, blank=True)
    home_seo_title_ar = models.CharField("Home SEO title (Arabic)", max_length=70, blank=True)
    home_meta_description = models.CharField("Home meta description", max_length=160, blank=True)
    home_meta_description_ar = models.CharField("Home meta description (Arabic)", max_length=160, blank=True)
    home_h1 = models.CharField(
        "Home page heading (H1)", max_length=140, blank=True,
        help_text="Shown as the small line above the display headline. This is the heading search engines read.",
    )
    home_h1_ar = models.CharField("Home page heading (Arabic)", max_length=140, blank=True)
    home_primary_keyword = models.CharField(max_length=120, blank=True, help_text="Editor guidance only.")
    home_supporting_keywords = models.CharField(max_length=400, blank=True, help_text="Editor guidance only.")
    home_ar_reviewed = models.BooleanField("Home Arabic reviewed", default=False)
    prefer_www = models.BooleanField(
        "Use the www address", default=False,
        help_text="Visitors on the other form of the address are redirected. Must match the address the site is configured with.",
    )
    analytics_provider = models.CharField(max_length=12, blank=True, choices=[("plausible", "Plausible"), ("ga4", "Google Analytics 4")])
    analytics_id = models.CharField("Analytics ID / domain", max_length=80, blank=True)

    # Forms
    notification_emails = models.TextField(
        blank=True,
        help_text="Who receives new enquiries and consultation requests when the area of interest has no list "
                  "of its own. One email address per line.",
    )
    recipients_project_management = models.TextField("Recipients · Project Management", blank=True)
    recipients_pmo_controls = models.TextField("Recipients · PMO & Controls", blank=True)
    recipients_business_development = models.TextField("Recipients · Business Development", blank=True)
    recipients_strategic_advisory = models.TextField("Recipients · Strategic Advisory", blank=True)
    recipients_other = models.TextField("Recipients · Other", blank=True)
    consent_text = models.TextField(
        "Consent wording", blank=True,
        help_text="The sentence next to the consent tick box. Each change is stored with the next submission as a new version.",
    )
    consent_text_ar = models.TextField("Consent wording (Arabic)", blank=True)
    consent_version = models.PositiveIntegerField(default=1, editable=False)
    turnstile_enabled = models.BooleanField("Bot protection (Cloudflare Turnstile)", default=False)
    turnstile_site_key = models.CharField(max_length=80, blank=True)
    capability_gate = models.BooleanField(
        "Ask for name & email before capability statement download", default=False,
    )

    cookie_notice = models.TextField(blank=True)
    cookie_notice_ar = models.TextField("Cookie notice (Arabic)", blank=True)

    # Switches
    copy_approval = models.CharField(
        "Site-wide wording", max_length=16, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING,
        help_text="Covers the positioning statement, the hero and the home page SEO. Until approved they are "
                  "shown only while content awaiting approval is visible.",
    )
    coming_soon = models.BooleanField(
        "Show the coming-soon page", default=True,
        help_text="ON: visitors see the coming-soon page instead of the website. Takes effect within seconds.",
    )
    show_pending_content = models.BooleanField(
        "Show content awaiting approval", default=True,
        help_text="ON for staging review only. TURN OFF BEFORE GOING LIVE.",
    )

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"
        permissions = [("approve_content", "Can approve content for publication")]

    def __str__(self) -> str:
        return "Site settings"

    def clean(self):
        has_video = any([self.hero_video, self.hero_video_mobile, self.hero_video_webm])
        if has_video and not self.hero_poster:
            raise ValidationError({"hero_poster": "A poster image is required whenever a video is uploaded."})
        require_alt(self, "hero_poster")

    def save(self, *args, **kwargs):
        # One row only: a second would split the gate between admin and API.
        self.pk = 1
        kwargs.pop("force_insert", None)
        existing = type(self).objects.filter(pk=1).values("created_at", "consent_text", "consent_text_ar").first()
        if existing:
            self.created_at = self.created_at or existing["created_at"]
            self._state.adding = False
            if (existing["consent_text"], existing["consent_text_ar"]) != (self.consent_text, self.consent_text_ar):
                self.consent_version += 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Site settings cannot be deleted.")

    @classmethod
    def load(cls) -> "SiteSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def notification_list(self) -> list[str]:
        return email_lines(self.notification_emails)

    def recipients_for(self, area: str) -> list[str]:
        """The area's own list when it has one, otherwise the general list."""
        return email_lines(getattr(self, f"recipients_{area}", "")) or self.notification_list


def email_lines(value: str) -> list[str]:
    return [line.strip() for line in (value or "").splitlines() if "@" in line]


# ── Navigation ───────────────────────────────────────────────────────────


class FooterColumn(Orderable):
    cache_tags = ("navigation",)

    title = models.CharField(max_length=60)
    title_ar = models.CharField("Title (Arabic)", max_length=60, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "footer column"

    def __str__(self) -> str:
        return self.title


class NavItem(Orderable):
    cache_tags = ("navigation",)

    class Menu(models.TextChoices):
        HEADER = "header", "Header"
        FOOTER = "footer", "Footer"
        LEGAL = "legal", "Footer — legal row"

    class MegaMenu(models.TextChoices):
        NONE = "", "None"
        SERVICES = "services", "Services list"
        SECTORS = "sectors", "Sectors list"

    menu = models.CharField(max_length=10, choices=Menu.choices, default=Menu.HEADER)
    label = models.CharField(max_length=60)
    label_ar = models.CharField("Label (Arabic)", max_length=60, blank=True)
    link = models.CharField(max_length=200, help_text="A site path like /services/, or a full https:// address.")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children",
                               help_text="Header only: put this item in another item’s dropdown.")
    column = models.ForeignKey(FooterColumn, null=True, blank=True, on_delete=models.CASCADE, related_name="items",
                               help_text="Footer only: which column this link sits in.")
    mega_menu = models.CharField(max_length=10, choices=MegaMenu.choices, blank=True,
                                 help_text="Header only: open a panel listing every service or sector.")
    visible = models.BooleanField(
        default=True,
        help_text="Items whose page has nothing published are hidden automatically, whatever this says.",
    )
    is_cta = models.BooleanField("Header button", default=False,
                                 help_text="Header only: show this item as the call-to-action button.")

    class Meta(Orderable.Meta):
        verbose_name = "navigation item"

    def __str__(self) -> str:
        return f"{self.get_menu_display()}: {self.label}"


class Redirect(TimeStamped):
    cache_tags = ("redirects",)

    old_path = models.CharField(max_length=300, unique=True, help_text="e.g. /services/old-name/ (without /en or /ar).")
    new_path = models.CharField(max_length=300)
    permanent = models.BooleanField(default=True)

    class Meta:
        ordering = ["old_path"]

    def __str__(self) -> str:
        return f"{self.old_path} → {self.new_path}"

    def clean(self):
        for field in ("old_path", "new_path"):
            value = getattr(self, field)
            if not (value.startswith("/") or value.startswith("https://")):
                raise ValidationError({field: "Start with / for a site path, or https:// for another site."})
        if self.old_path == self.new_path:
            raise ValidationError("A redirect cannot point at itself.")


# ── Home ─────────────────────────────────────────────────────────────────


class HomeSection(Orderable):
    """One band of the home page. The home page renders these in this order."""

    cache_tags = ("home",)

    class Kind(models.TextChoices):
        HERO = "hero", "Video hero"
        INTRO = "intro", "Introduction"
        PILLARS = "pillars", "The three pillars (services overview)"
        SECTORS = "sectors", "Sectors"
        VALUE = "value", "How we create value"
        CTA = "cta", "Call to action band"
        TRUST = "trust", "Client & partner logos"
        KPIS = "kpis", "Key figures"
        PROJECTS = "projects", "Featured projects"
        TESTIMONIAL = "testimonial", "Testimonial"
        INSIGHTS = "insights", "Latest insights"

    kind = models.CharField(max_length=16, choices=Kind.choices, unique=True)
    visible = models.BooleanField(default=True)
    approval = models.CharField(max_length=16, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING,
                                db_index=True, help_text="The section’s own wording is shown live only once approved.")
    eyebrow = models.CharField(max_length=60, blank=True)
    eyebrow_ar = models.CharField("Eyebrow (Arabic)", max_length=60, blank=True)
    title = models.CharField(max_length=140, blank=True)
    title_ar = models.CharField("Title (Arabic)", max_length=140, blank=True)
    intro = models.TextField(blank=True)
    intro_ar = models.TextField("Intro (Arabic)", blank=True)
    ar_reviewed = models.BooleanField("Arabic reviewed", default=False)
    cta_label = models.CharField("Button label", max_length=40, blank=True)
    cta_label_ar = models.CharField("Button label (Arabic)", max_length=40, blank=True)
    cta_link = models.CharField("Button link", max_length=200, blank=True)
    secondary_label = models.CharField("Second button label", max_length=40, blank=True)
    secondary_label_ar = models.CharField("Second button label (Arabic)", max_length=40, blank=True)
    secondary_link = models.CharField("Second button link", max_length=200, blank=True)
    image = models.ImageField("Background image", upload_to="home/", blank=True, validators=photo_validators(), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)

    objects = PublishableQuerySet.as_manager()

    class Meta(Orderable.Meta):
        verbose_name = "home section"

    def __str__(self) -> str:
        return self.get_kind_display()

    @property
    def is_approved(self) -> bool:
        return self.approval == ApprovalStatus.APPROVED

    def approval_blocker(self) -> str | None:
        return None

    def clean(self):
        require_alt(self, "image")


# ── Pages ────────────────────────────────────────────────────────────────


class Page(Publishable, Slugged, Seo, HeroBackground):
    """About, Approach, Careers intro, legal pages — built from ordered blocks."""

    cache_tags = ("pages", "navigation")
    public_path = "/{slug}/"

    title = models.CharField(max_length=140)
    path = models.CharField(
        max_length=200, unique=True, null=True, blank=True,
        help_text="Only for pages that sit under another page, e.g. /about-us/leadership-team/. Leave blank for /{slug}/.",
    )
    title_ar = models.CharField("Title (Arabic)", max_length=140, blank=True)
    eyebrow = models.CharField(max_length=60, blank=True)
    eyebrow_ar = models.CharField("Eyebrow (Arabic)", max_length=60, blank=True)
    intro = models.TextField(blank=True)
    intro_ar = models.TextField("Intro (Arabic)", blank=True)
    cta_label = models.CharField("Main button label", max_length=60, blank=True,
                                 help_text="e.g. the form’s submit button on Contact, or “View Opportunities” on Careers.")
    cta_label_ar = models.CharField("Main button label (Arabic)", max_length=60, blank=True)
    note = models.TextField("Editor note", blank=True, help_text="Internal guidance. Never shown on the site.")
    image = models.ImageField("Header image", upload_to="pages/", blank=True, validators=photo_validators(), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)

    class Meta(Publishable.Meta):
        verbose_name = "page"

    def __str__(self) -> str:
        return self.title

    def slug_source(self) -> str:
        return self.title

    def get_public_path(self) -> str:
        return self.path or super().get_public_path()

    def clean(self):
        super().clean()
        if self.path and not (self.path.startswith("/") and self.path.endswith("/")):
            raise ValidationError({"path": "Start and end the address with /, e.g. /about-us/leadership-team/."})
        require_alt(self, "image")


class PageBlock(Orderable):
    cache_tags = ("pages",)

    class Kind(models.TextChoices):
        RICH_TEXT = "rich_text", "Text"
        IMAGE_TEXT = "image_text", "Image + text"
        STATS = "stats", "Figures"
        QUOTE = "quote", "Quote"
        GALLERY = "gallery", "Gallery"
        CTA = "cta", "Call to action"
        FAQ = "faq", "Questions & answers"
        VALUES = "values", "Company values"
        APPROACH_STEPS = "approach_steps", "Approach steps"
        AFFILIATION = "affiliation", "Group affiliation statement"

    page = models.ForeignKey(Page, related_name="blocks", on_delete=models.CASCADE)
    kind = models.CharField(max_length=16, choices=Kind.choices, default=Kind.RICH_TEXT,
                            help_text="Company values and approach steps show their own lists; edit those under Website — About.")
    visible = models.BooleanField(default=True)
    navy = models.BooleanField("Navy background", default=False)
    note = models.TextField("Editor note", blank=True, help_text="Internal guidance. Never shown on the site.")
    eyebrow = models.CharField(max_length=60, blank=True)
    eyebrow_ar = models.CharField("Eyebrow (Arabic)", max_length=60, blank=True)
    title = models.CharField(max_length=140, blank=True)
    title_ar = models.CharField("Title (Arabic)", max_length=140, blank=True)
    body = RichTextField(blank=True, help_text="Main text. For a quote, the quotation.")
    body_ar = RichTextField("Body (Arabic)", blank=True)
    attribution = models.CharField(max_length=140, blank=True, help_text="Quote only: who said it.")
    attribution_ar = models.CharField("Attribution (Arabic)", max_length=140, blank=True)
    image = models.ImageField(upload_to="pages/", blank=True, validators=photo_validators(800, 500), help_text=PHOTO_HELP)
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)
    image_on_end = models.BooleanField("Image after the text", default=False)
    cta_label = models.CharField(max_length=40, blank=True)
    cta_label_ar = models.CharField("Button label (Arabic)", max_length=40, blank=True)
    cta_link = models.CharField(max_length=200, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "content block"

    def __str__(self) -> str:
        return f"{self.get_kind_display()}: {self.title or self.page.title}"

    def clean(self):
        require_alt(self, "image")


class PageBlockItem(Orderable):
    """A figure, a gallery image or a question — the repeating parts of a block."""

    cache_tags = ("pages",)

    block = models.ForeignKey(PageBlock, related_name="items", on_delete=models.CASCADE)
    label = models.CharField(max_length=200, blank=True, help_text="Figure label, image caption, or the question.")
    label_ar = models.CharField("Label (Arabic)", max_length=200, blank=True)
    value = models.CharField(max_length=40, blank=True, help_text="Figures only, e.g. 25+.")
    text = models.TextField(blank=True, help_text="Answer, or a figure’s source note.")
    text_ar = models.TextField("Text (Arabic)", blank=True)
    image = models.ImageField(upload_to="pages/", blank=True, validators=photo_validators(800, 500))
    image_alt = models.CharField(max_length=200, blank=True)
    image_alt_ar = models.CharField("Image description (Arabic)", max_length=200, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "item"

    def __str__(self) -> str:
        return self.label or self.value or f"Item {self.pk}"

    def clean(self):
        require_alt(self, "image")


# ── Launch readiness ─────────────────────────────────────────────────────


class LaunchReadiness(TimeStamped):
    """Singleton holding the claims to verify and the pre-launch checklist."""

    class Meta:
        verbose_name = "Launch readiness"
        verbose_name_plural = "Launch readiness"

    def __str__(self) -> str:
        return "Launch readiness"

    def save(self, *args, **kwargs):
        self.pk = 1
        kwargs.pop("force_insert", None)
        if type(self).objects.filter(pk=1).exists():
            self._state.adding = False
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Launch readiness cannot be deleted.")

    @classmethod
    def load(cls) -> "LaunchReadiness":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class LaunchReadinessItem(Orderable):
    class Kind(models.TextChoices):
        CLAIM = "claim", "Claim or credential to verify"
        CHECKLIST = "checklist", "Pre-launch checklist"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CONFIRMED = "confirmed", "Confirmed"

    readiness = models.ForeignKey(LaunchReadiness, related_name="items", on_delete=models.CASCADE)
    kind = models.CharField(max_length=10, choices=Kind.choices)
    item = models.CharField(max_length=200)
    requirement = models.TextField("Required confirmation", blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="+", limit_choices_to={"is_staff": True})
    note = models.TextField(blank=True)
    confirmed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="+", editable=False)
    confirmed_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta(Orderable.Meta):
        verbose_name = "readiness item"

    def __str__(self) -> str:
        return self.item
