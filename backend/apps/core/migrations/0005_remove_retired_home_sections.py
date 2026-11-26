from django.db import migrations


def remove_retired_sections(apps, schema_editor):
    """The services grid and the lifecycle timeline are no longer home page sections."""
    apps.get_model("core", "HomeSection").objects.filter(kind__in=("services", "approach")).delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0004_launchreadiness_homesection_approval_and_more")]

    operations = [migrations.RunPython(remove_retired_sections, migrations.RunPython.noop)]
