# Generated 2026-04-05 — remove unused icon_name field from Service model

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="service",
            name="icon_name",
        ),
    ]
