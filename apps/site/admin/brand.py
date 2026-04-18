"""
Admin for BrandSettings singleton — v1.4.0 Brand Customization System.
"""

from django.contrib import admin

from ..models import BrandSettings


@admin.register(BrandSettings)
class BrandSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Logo Assets",
            {
                "fields": (
                    "logo_display_mode",
                    "logo_max_width",
                    "logo_max_width_mobile",
                    "logo_light",
                    "logo_dark",
                    "logo_icon",
                ),
                "description": (
                    "Upload logo variants for light and dark contexts. "
                    "All fields are optional — leave blank to fall back to the master logo set under "
                    "Site Settings → Identity → Logo. "
                    "The master logo must be uploaded there first."
                ),
            },
        ),
        (
            "Typography",
            {
                "fields": ("typography_preset",),
                "description": (
                    "Choose a named type preset. The selection updates heading and body font families "
                    "site-wide via CSS custom properties. "
                    "'Balanced' is the default and uses Cormorant Garamond for headings and DM Sans for body."
                ),
            },
        ),
        (
            "Colors / Visual Style",
            {
                "fields": ("color_preset", "accent_color_custom", "visual_style"),
                "description": (
                    "Select a brand color preset. Accent colors apply to interactive elements, "
                    "selection highlights, borders, and emphasis details. "
                    "Visual Style controls corner rounding on cards, buttons, and images."
                ),
            },
        ),
        (
            "Social Links Display",
            {
                "fields": ("social_links_display",),
                "description": (
                    "Controls how social links appear in the footer. "
                    "Icons and Icons + Text modes require icon_slug to be set on each Social Link entry "
                    "(Site Admin → Social Links)."
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        # Singleton — no new rows; force use of the existing row via load()
        return not BrandSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
