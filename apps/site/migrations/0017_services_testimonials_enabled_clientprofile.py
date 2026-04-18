from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_sitesettings_blog_enabled"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="services_enabled",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Show the Services module in public navigation, footer, and homepage preview. "
                    "Enable this for client sites that offer clearly defined services. "
                    "Add Service items first so the page has content when you enable this."
                ),
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="testimonials_enabled",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Show a testimonials section on the homepage. "
                    "Testimonials are managed under Projects \u2192 Testimonials. "
                    "Only active testimonials without a project association appear in the homepage section."
                ),
            ),
        ),
        migrations.CreateModel(
            name="ClientProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("client_name", models.CharField(help_text="Business or studio name for this client site.", max_length=200)),
                ("contact_name", models.CharField(blank=True, help_text="Primary contact person at the client.", max_length=200)),
                ("contact_email", models.EmailField(blank=True, help_text="Primary contact email for the client.")),
                ("website_domain", models.CharField(blank=True, help_text="Live domain for this deployment, e.g. jat21.com", max_length=200)),
                ("package_type", models.CharField(blank=True, choices=[("starter", "Starter"), ("pro", "Pro"), ("academic", "Academic"), ("consultant", "Consultant"), ("custom", "Custom")], help_text="Commercial package this client purchased.", max_length=50)),
                ("handover_status", models.CharField(blank=True, choices=[("pending", "Pending"), ("in_progress", "In Progress"), ("complete", "Complete")], help_text="Current handover progress.", max_length=50)),
                ("support_status", models.CharField(blank=True, choices=[("active", "Active"), ("inactive", "Inactive"), ("included", "Included (first 30 days)")], help_text="Post-launch support status.", max_length=50)),
                ("notes", models.TextField(blank=True, help_text="Internal notes \u2014 not visible on any public page.")),
                ("is_active", models.BooleanField(default=True, help_text="Uncheck to mark this client record as inactive/archived.")),
            ],
            options={
                "verbose_name": "Client Profile",
                "verbose_name_plural": "Client Profiles",
            },
        ),
    ]
