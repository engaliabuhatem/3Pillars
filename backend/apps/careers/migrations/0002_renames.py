from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("careers", "0001_initial")]

    operations = [
        migrations.RenameField("job", "seo_description", "meta_description"),
        migrations.RenameField("job", "seo_description_ar", "meta_description_ar"),
    ]
