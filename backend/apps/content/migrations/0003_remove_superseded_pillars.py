from django.db import migrations


def remove_pillars(apps, schema_editor):
    """
    The pillars were abstract principles; they are now numbered service lines
    with a unique number, so the old rows cannot carry over. `seed_content`
    creates the three service-line pillars.
    """
    apps.get_model("content", "Pillar").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("content", "0002_renames")]

    operations = [migrations.RunPython(remove_pillars, migrations.RunPython.noop)]
