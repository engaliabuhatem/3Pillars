"""
Which navigation links have something to show.

A menu item pointing at a page with no visible content is hidden, so the menu
never leads to an empty page. "Visible" follows the same gate as the content:
on staging (pending shown) pending pages count. Projects are the exception:
that item needs at least one approved project, because a projects page built
only from unapproved work is never something to advertise.
"""

from urllib.parse import urlsplit

from django.apps import apps


class LinkResolver:
    def __init__(self, *, include_pending: bool):
        self.include_pending = include_pending
        self._cache: dict[str, bool] = {}

    def has_content(self, link: str) -> bool:
        if not link or link.startswith(("http://", "https://", "mailto:", "tel:")):
            return True
        path = urlsplit(link).path
        path = path if path.endswith("/") else f"{path}/"
        if path not in self._cache:
            self._cache[path] = self._resolve(path)
        return self._cache[path]

    def _visible(self, label: str):
        return apps.get_model(label).objects.visible(include_pending=self.include_pending)

    def _resolve(self, path: str) -> bool:
        if path == "/":
            return True
        parts = [p for p in path.split("/") if p]
        if parts[0] == "projects":
            approved = apps.get_model("content.Project").objects.approved()
            return approved.exists() if len(parts) == 1 else approved.filter(slug=parts[1]).exists()
        detail = {"services": "content.Service", "sectors": "content.Sector", "insights": "content.Insight",
                  "careers": "careers.Job"}
        if len(parts) == 2 and parts[0] in detail:
            return self._visible(detail[parts[0]]).filter(slug=parts[1]).exists()
        pages = self._visible("core.Page")
        return pages.filter(path=path).exists() or (len(parts) == 1 and pages.filter(slug=parts[0], path=None).exists())
