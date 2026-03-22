"""
Management command: check_content_readiness
-------------------------------------------
Checks that the site has been customised from template defaults and has the
minimum content needed for a public launch.

Exit code 0 — all checks pass.
Exit code 1 — at least one warning was reported.

Usage:
    uv run python manage.py check_content_readiness
    # or via Make:
    make check-content

Suitable as a pre-launch gate.  Add to a deploy checklist, not to `make health`
(health is CI-safe; this command requires a populated database).
"""

import sys

from django.core.management.base import BaseCommand

from apps.core.models import AboutProfile, SiteSettings
from apps.projects.models import Project
from apps.services.models import Service


def collect_warnings() -> list[str]:
    """
    Return a list of human-readable warning strings describing content that
    still looks like an uncustomised template.  Returns an empty list when
    the site passes all checks.

    Separated from the Command class so it can be called directly in tests.
    """
    warnings: list[str] = []

    site = SiteSettings.load()
    about = AboutProfile.load()

    # -- SiteSettings ---------------------------------------------------------

    if not site.site_name:
        warnings.append(
            "SiteSettings.site_name is blank. "
            "Update it in admin \u2192 Site Settings."
        )

    if not site.contact_email:
        warnings.append(
            "SiteSettings.contact_email is blank. "
            "Set it in admin \u2192 Site Settings so enquiries reach your inbox."
        )

    if not site.meta_description:
        warnings.append(
            "SiteSettings.meta_description is blank. "
            "The homepage will have no meta description in search results."
        )

    if not site.og_image:
        warnings.append(
            "SiteSettings.og_image is missing. "
            "Social share cards will have no image."
        )

    # -- AboutProfile ---------------------------------------------------------

    if not about.headline:
        warnings.append(
            "AboutProfile.headline is blank. "
            "The About page will render without a heading."
        )

    if about.experience_years == 0:
        warnings.append(
            "AboutProfile.experience_years is 0. "
            "This value renders publicly \u2014 enter the real figure in admin."
        )

    if not about.portrait:
        warnings.append(
            "AboutProfile.portrait is missing. "
            "The About page will have no portrait image."
        )

    # -- Content collections --------------------------------------------------

    if not Service.objects.filter(active=True).exists():
        warnings.append(
            "No active Service records found. "
            "The Services page will be empty."
        )

    if not Project.objects.exists():
        warnings.append(
            "No Project records found. "
            "The portfolio will be empty."
        )

    return warnings


class Command(BaseCommand):
    help = (
        "Check that the site has been properly customised from template defaults "
        "before launch. Exits with code 1 if any warnings are reported."
    )

    def handle(self, *args, **options):
        warnings = collect_warnings()

        if warnings:
            self.stdout.write(
                self.style.WARNING(f"\n{len(warnings)} content readiness warning(s) found:\n")
            )
            for w in warnings:
                self.stdout.write(self.style.WARNING(f"  \u26a0  {w}"))
            self.stdout.write("")
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS("Content readiness: all checks pass.\n"))
