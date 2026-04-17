from django.db import models


class SocialLink(models.Model):
    label = models.CharField(max_length=60)
    url = models.URLField()
    icon_slug = models.CharField(
        max_length=60,
        blank=True,
        help_text="Optional icon identifier (e.g. 'linkedin', 'github', 'instagram').",
    )
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
        ordering = ["order", "label"]

    def __str__(self):
        return self.label
