from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "apps.core"
    label = "core"
    verbose_name = "Site"

    def ready(self):
        from django.db.models.signals import post_migrate

        from . import signals  # noqa: F401  (connects the receivers)
        from .roles import sync_roles

        # Fires once per app; idempotent, so the final run sees every permission.
        post_migrate.connect(sync_roles, dispatch_uid="core.sync_roles")
