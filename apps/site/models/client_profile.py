from django.db import models


class ClientProfile(models.Model):
    """
    Lightweight record of who owns/operates this deployed site.

    This is not multi-tenant — it is metadata about the single client for this
    deployment. Used for handover tracking, support status, and package context.
    It does not affect public site behaviour; it is admin-only.
    """

    PACKAGE_CHOICES = [
        ("starter", "Starter"),
        ("pro", "Pro"),
        ("academic", "Academic"),
        ("consultant", "Consultant"),
        ("custom", "Custom"),
    ]

    HANDOVER_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("complete", "Complete"),
    ]

    SUPPORT_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("included", "Included (first 30 days)"),
    ]

    client_name = models.CharField(
        max_length=200,
        help_text="Business or studio name for this client site.",
    )
    contact_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Primary contact person at the client.",
    )
    contact_email = models.EmailField(
        blank=True,
        help_text="Primary contact email for the client.",
    )
    website_domain = models.CharField(
        max_length=200,
        blank=True,
        help_text="Live domain for this deployment, e.g. mystudio.com",
    )
    package_type = models.CharField(
        max_length=50,
        blank=True,
        choices=PACKAGE_CHOICES,
        help_text="Commercial package this client purchased.",
    )
    handover_status = models.CharField(
        max_length=50,
        blank=True,
        choices=HANDOVER_CHOICES,
        help_text="Current handover progress.",
    )
    support_status = models.CharField(
        max_length=50,
        blank=True,
        choices=SUPPORT_CHOICES,
        help_text="Post-launch support status.",
    )
    notes = models.TextField(
        blank=True,
        help_text="Internal notes — not visible on any public page.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to mark this client record as inactive/archived.",
    )

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"

    def __str__(self) -> str:
        domain = f" ({self.website_domain})" if self.website_domain else ""
        return f"{self.client_name}{domain}"
