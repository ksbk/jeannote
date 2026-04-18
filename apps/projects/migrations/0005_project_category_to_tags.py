from django.db import migrations, models


def copy_category_to_tags(apps, schema_editor):
    """Copy each project's category slug into the new tags field."""
    Project = apps.get_model("projects", "Project")
    for project in Project.objects.all():
        project.tags = project.category or ""
        project.save(update_fields=["tags"])


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_alter_testimonial_project"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="tags",
            field=models.CharField(
                blank=True,
                default="",
                help_text='Comma-separated tags, e.g. "housing, residential". Used to group and filter projects.',
                max_length=200,
            ),
        ),
        migrations.RunPython(copy_category_to_tags, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="project",
            name="category",
        ),
    ]
