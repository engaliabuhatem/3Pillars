from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("core", "0002_hero_poster_mobile")]

    operations = [
        migrations.RenameField("page", "seo_description", "meta_description"),
        migrations.RenameField("page", "seo_description_ar", "meta_description_ar"),
    ]
