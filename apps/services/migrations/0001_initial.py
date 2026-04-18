import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ServiceItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="Service name as it appears in the services list.", max_length=120)),
                ("short_description", models.TextField(help_text="One or two sentences summarising what this service is and who it is for.")),
                ("long_description", models.TextField(blank=True, help_text="Optional extended description shown on the services page below the summary.")),
                ("order", models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")),
                ("active", models.BooleanField(default=True, help_text="Only active services appear on the public services page.")),
            ],
            options={
                "verbose_name": "Service",
                "verbose_name_plural": "Services",
                "ordering": ["order", "name"],
            },
        ),
    ]
