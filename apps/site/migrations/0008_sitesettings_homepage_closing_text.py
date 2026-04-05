from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_sitesettings_nav_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="homepage_closing_text",
            field=models.CharField(
                blank=True,
                default="Ready to discuss a project? Bring a brief, a question, or an early idea.",
                help_text="Short closing invitation shown above the contact CTA on the homepage. Keep it under 120 characters.",
                max_length=220,
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="tagline",
            field=models.CharField(
                blank=True,
                default="Design shaped by purpose, context, and enduring quality.",
                help_text="One or two sentences describing your practice. Under 140 characters fits most hero layouts cleanly.",
                max_length=220,
            ),
        ),
    ]
