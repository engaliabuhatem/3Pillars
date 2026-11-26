"""
The four staff roles, kept in sync after every `migrate`.

Assign people to roles under Configuration → Roles. A person can hold more
than one (an Editor who is also an Approver).
"""

from django.contrib.auth.models import Group, Permission

CONTENT_APPS = ("content",)
SITE_MODELS = ("homesection", "page", "pageblock", "pageblockitem", "navitem", "footercolumn", "redirect",
               "launchreadiness", "launchreadinessitem")
BD_APP = "bd"


def _perms(app_label: str, models=None, actions=("add", "change", "delete", "view")):
    qs = Permission.objects.filter(content_type__app_label=app_label)
    if models:
        qs = qs.filter(content_type__model__in=models)
    return [p for p in qs if p.codename.split("_", 1)[0] in actions]


def roles() -> dict[str, list[Permission]]:
    editor = [
        *_perms("content"),
        *_perms("core", SITE_MODELS),
        *_perms("core", ("sitesettings",), ("change", "view")),
        *_perms("careers", ("job",)),
    ]
    bd = [
        *_perms(BD_APP, actions=("change", "view", "delete")),
        *_perms(BD_APP, ("enquirynote", "proposalnote"), ("add",)),
        *_perms("content", ("client",), ("add", "change", "view")),
        *_perms("careers", ("application",), ("change", "view")),
    ]
    viewer = [*_perms("content", actions=("view",)), *_perms("core", actions=("view",)),
              *_perms("careers", actions=("view",))]
    approve = list(Permission.objects.filter(codename="approve_content", content_type__app_label="core"))
    everything = list(Permission.objects.filter(content_type__app_label__in=("content", "core", "bd", "careers", "auth",
                                                                              "otp_totp")))
    return {
        "Editor": editor,
        "BD": bd,
        "Approver": [*viewer, *approve],
        "Admin": everything,
    }


def sync_roles(**kwargs) -> None:
    for name, permissions in roles().items():
        group, _ = Group.objects.get_or_create(name=name)
        group.permissions.set(permissions)
