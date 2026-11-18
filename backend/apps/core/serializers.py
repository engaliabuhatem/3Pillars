"""
The serializer base every public endpoint uses.

For `?locale=ar`, each field `x` whose model has an `x_ar` twin is replaced by
the Arabic value; an empty Arabic value falls back to English and the field's
name is listed in `fallbacks`, so the site can mark it and editors can see
what still needs translating. The `_ar` columns themselves are never sent.
"""

from rest_framework import serializers

from .images import file_payload, image_payload
from .models import FooterColumn, HomeSection, NavItem, Page, PageBlock, PageBlockItem, Redirect, SiteSettings


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


class SeoMixin(serializers.Serializer):
    seo = serializers.SerializerMethodField()

    def get_seo(self, obj):
        ar = self.context.get("locale") == "ar"
        pick = lambda f: (getattr(obj, f"{f}_ar", "") if ar else "") or getattr(obj, f, "")  # noqa: E731
        return {
            "title": pick("seo_title"),
            "description": pick("seo_description"),
            "image": image_payload(obj, "og_image", request=self.context.get("request")),
        }


# ── Site settings ────────────────────────────────────────────────────────


class SiteSettingsSerializer(LocalizedSerializer):
    image_fields = ("hero_poster", "hero_poster_mobile", "og_image")
    hero = serializers.SerializerMethodField()
    logos = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()
    capability_statement = serializers.SerializerMethodField()
    analytics = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            "company_name", "short_name", "tagline", "group_relationship", "hero", "logos",
            "phone", "email", "whatsapp", "show_whatsapp", "address", "socials",
            "seo_title", "seo_description", "analytics", "cookie_notice",
            "turnstile_enabled", "turnstile_site_key", "capability_gate", "capability_statement",
            "coming_soon", "show_pending_content",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["hero"]["poster"] = data.pop("hero_poster")
        data["hero"]["poster_mobile"] = data.pop("hero_poster_mobile")
        data["default_og_image"] = data.pop("og_image")
        return data

    def get_hero(self, obj):
        ar = self.locale == "ar"
        pick = lambda f: (getattr(obj, f"{f}_ar") if ar else "") or getattr(obj, f)  # noqa: E731
        request = self.context.get("request")
        return {
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


class NavItemSerializer(LocalizedSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = NavItem
        fields = ["label", "link", "mega_menu", "children"]

    def get_children(self, obj):
        children = [c for c in obj.children.all() if c.visible]
        return NavItemSerializer(children, many=True, context=self.context).data


class FooterColumnSerializer(LocalizedSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = FooterColumn
        fields = ["title", "items"]

    def get_items(self, obj):
        items = [i for i in obj.items.all() if i.visible and i.menu == NavItem.Menu.FOOTER]
        return NavItemSerializer(items, many=True, context=self.context).data


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

    class Meta:
        model = PageBlock
        fields = ["id", "kind", "navy", "eyebrow", "title", "body", "attribution", "image_on_end",
                  "cta_label", "cta_link", "items"]


class PageSerializer(SeoMixin, LocalizedSerializer):
    image_fields = ("image",)
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ["slug", "title", "eyebrow", "intro", "blocks", "seo", "updated_at"]

    def get_blocks(self, obj):
        blocks = [b for b in obj.blocks.all() if b.visible]
        return PageBlockSerializer(blocks, many=True, context=self.context).data
