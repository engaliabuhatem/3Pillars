from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .api import GatedReadOnlyViewSet, pending_visible, request_locale
from .home import build_home
from .models import ApprovalStatus, FooterColumn, NavItem, Page, PageBlock, Redirect, SiteSettings
from .navigation import LinkResolver
from .serializers import (
    FooterColumnSerializer,
    NavItemSerializer,
    PageSerializer,
    RedirectSerializer,
    SiteSettingsSerializer,
    shown,
)


class LocaleContextMixin:
    def context(self, request):
        return {"request": request, "locale": request_locale(request), "include_pending": pending_visible()}


class SiteSettingsView(LocaleContextMixin, APIView):
    def get(self, request):
        return Response(SiteSettingsSerializer(SiteSettings.load(), context=self.context(request)).data)


class NavigationView(LocaleContextMixin, APIView):
    def get(self, request):
        from apps.content.models import Sector, Service
        from apps.content.serializers import SectorCardSerializer, ServiceCardSerializer

        context = self.context(request)
        pending = context["include_pending"]
        context["links"] = LinkResolver(include_pending=pending)
        header = NavItem.objects.filter(menu=NavItem.Menu.HEADER, parent=None).prefetch_related("children")
        columns = FooterColumn.objects.prefetch_related("items")
        legal = NavItem.objects.filter(menu=NavItem.Menu.LEGAL)
        return Response({
            "header": NavItemSerializer(shown(header, context), many=True, context=context).data,
            "footer": FooterColumnSerializer(columns, many=True, context=context).data,
            "legal": NavItemSerializer(shown(legal, context), many=True, context=context).data,
            "mega": {
                "services": ServiceCardSerializer(Service.objects.visible(include_pending=pending), many=True, context=context).data,
                "sectors": SectorCardSerializer(Sector.objects.visible(include_pending=pending), many=True, context=context).data,
            },
        })


class HomeView(LocaleContextMixin, APIView):
    def get(self, request):
        return Response(build_home(self.context(request)))


class PageViewSet(GatedReadOnlyViewSet):
    model = Page
    serializer_class = PageSerializer
    pagination_class = None

    def base_queryset(self):
        return Page.objects.prefetch_related(Prefetch("blocks", queryset=PageBlock.objects.prefetch_related("items")))


class RedirectListView(APIView):
    def get(self, request):
        return Response(RedirectSerializer(Redirect.objects.all(), many=True).data)


@api_view(["GET"])
def sitemap(request):
    """
    Every approved page, whatever the staging switch says, with whether its
    Arabic version may be listed. Draft topics are excluded by Insight's own gate.
    """
    from .seo import page_models

    settings = SiteSettings.load()
    entries = []
    if settings.copy_approval == ApprovalStatus.APPROVED:
        entries.append({"path": "/", "updated_at": settings.updated_at, "ar": settings.home_ar_reviewed})
    for model in page_models():
        rows = model.objects.approved()
        if hasattr(model, "is_open"):
            rows = rows.filter(is_open=True)
        for obj in rows:
            entries.append({"path": obj.get_public_path(), "updated_at": obj.updated_at, "ar": obj.ar_reviewed})
    return Response(entries)


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})
