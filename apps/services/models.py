from django.db import models


class ServiceItem(models.Model):
    name = models.CharField(
        max_length=120,
        help_text="Service name as it appears in the services list.",
    )
    short_description = models.TextField(
        help_text="One or two sentences summarising what this service is and who it is for.",
    )
    long_description = models.TextField(
        blank=True,
        help_text="Optional extended description shown on the services page below the summary.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first.",
    )
    active = models.BooleanField(
        default=True,
        help_text="Only active services appear on the public services page.",
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self) -> str:
        return self.name
