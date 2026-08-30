from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="animation_mode",
            field=models.CharField(
                choices=[
                    ("full", "Full — always animate"),
                    ("device", "Device preference — respect reduced motion"),
                    ("off", "Off — disable animation"),
                ],
                default="device",
                help_text="Controls motion throughout the public portfolio.",
                max_length=12,
            ),
        ),
    ]
