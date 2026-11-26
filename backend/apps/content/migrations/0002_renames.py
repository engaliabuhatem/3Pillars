from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("content", "0001_initial")]

    operations = [
        migrations.RenameModel("LifecycleStage", "ApproachStep"),
        migrations.RenameModel("ServiceDeliverable", "ServiceCapability"),
        migrations.RenameField("servicecapability", "text", "title"),
        migrations.RenameField("servicecapability", "text_ar", "title_ar"),
        migrations.RenameField("service", "overview", "intro"),
        migrations.RenameField("service", "overview_ar", "intro_ar"),
        migrations.RenameField("service", "sectors", "related_sectors"),
        migrations.RenameField("project", "outcome", "results"),
        migrations.RenameField("project", "outcome_ar", "results_ar"),
        *[
            op
            for model in ("sector", "service", "project", "insight")
            for op in (
                migrations.RenameField(model, "seo_description", "meta_description"),
                migrations.RenameField(model, "seo_description_ar", "meta_description_ar"),
            )
        ],
    ]
