"""
The serializer base every public endpoint uses.

For `?locale=ar`, each field `x` whose model has an `x_ar` twin is replaced by
the Arabic value; an empty Arabic value falls back to English and the field's
name is listed in `fallbacks`, so the site can mark it and editors can see
what still needs translating. The `_ar` columns themselves are never sent.
"""

from rest_framework import serializers

from .images import file_payload, image_payload
from .models import (
    ApprovalStatus,
    FooterColumn,
    HomeSection,
    NavItem,
    Page,
    PageBlock,
    PageBlockItem,
    Redirect,
    SiteSettings,
)


def gated(queryset, context):
    """Related rows obey the same approval gate as the row that holds them."""
    return queryset if context.get("include_pending") else queryset.approved()


class LocalizedSerializer(serializers.ModelSerializer):
    #: Image fields rendered as `{src, alt, width, height, sources}`.
    image_fields: tuple[str, ...] = ()

    @property
    def locale(self) -> str:
        return self.context.get("locale", "en")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        fallbacks = []
        if self.locale == "ar":
            for name, field in self.fields.items():
                source = getattr(field, "source", None)
                if not isinstance(source, str) or "." in source or not hasattr(instance, f"{source}_ar"):
                    continue
                arabic = getattr(instance, f"{source}_ar")
                if arabic:
                    data[name] = arabic
                elif data.get(name):
                    fallbacks.append(name)
        request = self.context.get("request")
        for field in self.image_fields:
            data[field] = image_payload(instance, field, request=request, locale=self.locale)
        if hasattr(instance, "approval"):
            data["pending"] = not instance.is_approved
        if fallbacks:
            data["fallbacks"] = fallbacks
        return data


def indexable(approved: bool, ar_reviewed: bool) -> dict[str, bool]:
    """
    Which language versions search engines may index. Unapproved pages never;
    an Arabic page only once its translation has been reviewed, so machine
    drafts and English fallbacks never compete in search.
    """
    return {"en": approved, "ar": approved and ar_reviewed}


class SeoMixin(serializers.Serializer):
    seo = serializers.SerializerMethodField()

    def get_seo(self, obj):
        ar = self.context.get("locale") == "ar"
        pick = lambda f: (getattr(obj, f"{f}_ar", "") if ar else "") or getattr(obj, f, "")  # noqa: E731
        return {
            "title": pick("seo_title"),
            "description": pick("meta_description"),
            "h1": pick("h1"),
            "image": image_payload(obj, "og_image", request=self.context.get("request")),
            "indexable": indexable(obj.is_approved, obj.ar_reviewed),
        }


# ── Site settings ────────────────────────────────────────────────────────


class SiteSettingsSerializer(LocalizedSerializer):
    image_fields = ("hero_poster", "hero_poster_mobile", "og_image", "default_hero_image")
    hero = serializers.SerializerMethodField()
    logos = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()
    capability_statement = serializers.SerializerMethodField()
    analytics = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            "company_name", "short_name", "tagline", "group_relationship", "hero", "logos",
            "phone", "email", "whatsapp", "show_whatsapp", "address", "business_hours", "socials",
            "seo_title", "seo_description", "home_seo", "prefer_www", "analytics", "cookie_notice", "consent_text",
            "turnstile_enabled", "turnstile_site_key", "capability_gate", "capability_statement",
            "coming_soon", "show_pending_content",
        ]

    #: Shown only once Site settings → Contact → "Contact details verified" is ticked.
    CONTACT_FIELDS = ("phone", "email", "whatsapp", "address", "business_hours")

    home_seo = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["hero"]["poster"] = data.pop("hero_poster")
        data["hero"]["poster_mobile"] = data.pop("hero_poster_mobile")
        data["default_og_image"] = data.pop("og_image")
        if not instance.contact_verified:
            for field in self.CONTACT_FIELDS:
                data[field] = ""
            data["show_whatsapp"] = False
            data["socials"] = []
        if instance.copy_approval != ApprovalStatus.APPROVED and not self.context.get("include_pending"):
            data["tagline"] = ""
            data["home_seo"] = {**data["home_seo"], "title": "", "description": "", "h1": ""}
            hero = data["hero"]
            for key in ("h1", "eyebrow", "headline", "subline"):
                hero[key] = ""
            hero["primary"]["label"] = hero["secondary"]["label"] = ""
        data["copy_pending"] = instance.copy_approval != ApprovalStatus.APPROVED
        return data

    def get_home_seo(self, obj):
        ar = self.locale == "ar"
        pick = lambda f: (getattr(obj, f"{f}_ar") if ar else "") or getattr(obj, f)  # noqa: E731
        return {
            "title": pick("home_seo_title"),
            "description": pick("home_meta_description"),
            "h1": pick("home_h1"),
            "image": None,
            "indexable": indexable(obj.copy_approval == ApprovalStatus.APPROVED, obj.home_ar_reviewed),
        }

    def get_hero(self, obj):
        ar = self.locale == "ar"
        pick = lambda f: (getattr(obj, f"{f}_ar") if ar else "") or getattr(obj, f)  # noqa: E731
        request = self.context.get("request")
        return {
            "h1": pick("home_h1"),
            "eyebrow": pick("hero_eyebrow"),
            "headline": pick("hero_headline"),
            "subline": pick("hero_subline"),
            "primary": {"label": pick("hero_primary_label"), "href": obj.hero_primary_link},
            "secondary": {"label": pick("hero_secondary_label"), "href": obj.hero_secondary_link},
            "video": {
                "mp4": file_payload(obj, "hero_video", request=request),
                "webm": file_payload(obj, "hero_video_webm", request=request),
                "mobile": file_payload(obj, "hero_video_mobile", request=request),
            },
        }

    def get_logos(self, obj):
        request = self.context.get("request")
        return {
            "light": file_payload(obj, "logo_light", request=request),
            "dark": file_payload(obj, "logo_dark", request=request),
            "favicon": file_payload(obj, "favicon", request=request),
        }

    def get_socials(self, obj):
        names = ("linkedin", "x_twitter", "facebook", "instagram", "youtube")
        return [{"network": n, "href": getattr(obj, n)} for n in names if getattr(obj, n)]

    def get_analytics(self, obj):
        if not obj.analytics_provider or not obj.analytics_id:
            return None
        return {"provider": obj.analytics_provider, "id": obj.analytics_id}

    def get_capability_statement(self, obj):
        from apps.content.models import Download

        doc = gated(Download.objects.filter(is_capability_statement=True), self.context).first()
        if not doc:
            return None
        return {"id": doc.pk, "slug": doc.slug, "gated": doc.gated or obj.capability_gate}


# ── Navigation ───────────────────────────────────────────────────────────


def shown(items, context):
    """Visible items whose target has content (see navigation.py)."""
    resolver = context["links"]
    return [item for item in items if item.visible and resolver.has_content(item.link)]


class NavItemSerializer(LocalizedSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = NavItem
        fields = ["label", "link", "mega_menu", "is_cta", "children"]

    def get_children(self, obj):
        return NavItemSerializer(shown(obj.children.all(), self.context), many=True, context=self.context).data


class FooterColumnSerializer(LocalizedSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = FooterColumn
        fields = ["title", "items"]

    def get_items(self, obj):
        items = [i for i in obj.items.all() if i.menu == NavItem.Menu.FOOTER]
        return NavItemSerializer(shown(items, self.context), many=True, context=self.context).data


class RedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redirect
        fields = ["old_path", "new_path", "permanent"]


# ── Home sections and pages ──────────────────────────────────────────────


class HomeSectionSerializer(LocalizedSerializer):
    image_fields = ("image",)

    class Meta:
        model = HomeSection
        fields = ["kind", "eyebrow", "title", "intro", "cta_label", "cta_link", "secondary_label", "secondary_link"]


class PageBlockItemSerializer(LocalizedSerializer):
    image_fields = ("image",)

    class Meta:
        model = PageBlockItem
        fields = ["label", "value", "text"]


class PageBlockSerializer(LocalizedSerializer):
    image_fields = ("image",)
    items = PageBlockItemSerializer(many=True, read_only=True)
    entries = serializers.SerializerMethodField()

    class Meta:
        model = PageBlock
        fields = ["id", "kind", "navy", "eyebrow", "title", "body", "attribution", "image_on_end",
                  "cta_label", "cta_link", "items", "entries"]

    def get_entries(self, obj):
        """Values and approach steps live in their own tables; the block shows them in place."""
        from apps.content import serializers as content
        from apps.content.models import ApproachStep, CompanyValue

        source = {
            PageBlock.Kind.VALUES: (CompanyValue, content.CompanyValueSerializer),
            PageBlock.Kind.APPROACH_STEPS: (ApproachStep, content.ApproachStepSerializer),
        }.get(obj.kind)
        if not source:
            return []
        model, serializer = source
        rows = model.objects.visible(include_pending=self.context.get("include_pending"))
        return serializer(rows, many=True, context=self.context).data


class PageSerializer(SeoMixin, LocalizedSerializer):
    image_fields = ("image", "hero_image")
    blocks = serializers.SerializerMethodField()

    path = serializers.CharField(source="get_public_path")

    class Meta:
        model = Page
        fields = ["slug", "path", "title", "eyebrow", "intro", "cta_label", "blocks", "seo", "updated_at"]

    def get_blocks(self, obj):
        blocks = [b for b in obj.blocks.all() if b.visible]
        return PageBlockSerializer(blocks, many=True, context=self.context).data
