from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0002_sitesettings_animation_mode")]

    operations = [
        migrations.CreateModel(
            name="ExperienceLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")),
                ("label", models.CharField(default="View live site", max_length=80)),
                ("url", models.URLField(max_length=500)),
                ("experience", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="site_links", to="portfolio.experience")),
            ],
            options={
                "verbose_name": "Experience live-site link",
                "verbose_name_plural": "Experience live-site links",
                "ordering": ["order", "id"],
            },
        ),
    ]
