"""The locale and the approval gate, shared by every content endpoint."""

from rest_framework import mixins, viewsets

from .models import SiteSettings


def request_locale(request) -> str:
    return "ar" if request is not None and request.query_params.get("locale") == "ar" else "en"


def pending_visible() -> bool:
    return SiteSettings.load().show_pending_content


class GatedReadOnlyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    The approval gate, applied once for every content endpoint.

    No view filters by approval on its own, so there is a single place to
    audit before go-live and no route can leak pending content by forgetting.
    """

    lookup_field = "slug"
    model = None

    def base_queryset(self):
        return self.model.objects.all()

    def get_queryset(self):
        return self.base_queryset().visible(include_pending=self.include_pending)

    @property
    def include_pending(self) -> bool:
        if not hasattr(self, "_include_pending"):
            self._include_pending = pending_visible()
        return self._include_pending

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["locale"] = request_locale(self.request)
        context["include_pending"] = self.include_pending
        return context
