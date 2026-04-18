"""
BrandSettings singleton model for the v1.4.0 Brand Customization System.

Controls visual brand identity: logo variants, typography preset, brand
color preset, visual style, and social links display mode.

Kept separate from SiteSettings to isolate brand-display concerns from
identity/content concerns. Both are singletons using SingletonModel.
"""

import re

from django.core.exceptions import ValidationError
from django.db import models

from .site import SingletonModel

_HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


class BrandSettings(SingletonModel):
    """Singleton that controls all runtime visual brand customization."""

    # ------------------------------------------------------------------
    # Choices
    # ------------------------------------------------------------------

    class TypographyPreset(models.TextChoices):
        BALANCED = "balanced", "Balanced — Cormorant Garamond + DM Sans (default)"
        EDITORIAL_SERIF = "editorial_serif", "Editorial Serif — serif headings + serif body"
        MODERN_CLEAN = "modern_clean", "Modern Clean — system sans-serif throughout"
        TECHNICAL = "technical", "Technical — monospace headings + system sans body"
        WARM_PROFESSIONAL = "warm_professional", "Warm Professional — Palatino headings + system body"

    class ColorPreset(models.TextChoices):
        NEUTRAL = "neutral", "Neutral — warm bronze (default)"
        BLUE = "blue", "Blue — professional navy"
        GREEN = "green", "Green — organic forest"
        BURGUNDY = "burgundy", "Burgundy — confident deep red"
        AMBER = "amber", "Amber — warm earth"
        CUSTOM = "custom", "Custom — use accent color field below"

    class VisualStyle(models.TextChoices):
        CRISP = "crisp", "Crisp — sharp edges, no rounding"
        BALANCED = "balanced", "Balanced — subtle rounding (default)"
        SOFT = "soft", "Soft — rounded corners throughout"

    class SocialLinksDisplay(models.TextChoices):
        TEXT = "text", "Text labels only (default)"
        ICONS = "icons", "Icons only (requires icon_slug on each Social Link)"
        ICONS_TEXT = "icons_text", "Icons + text labels"

    class LogoDisplayMode(models.TextChoices):
        TRANSPARENT = "transparent", "Always on transparent background"
        SAFE_CARD = "safe_card", "On card / padded background"
        AUTO = "auto", "Auto (default — let the template decide)"

    # ------------------------------------------------------------------
    # Logo variants
    # ------------------------------------------------------------------

    logo_light = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text=(
            "Logo optimised for light backgrounds. "
            "Leave blank to use the master logo (Site Settings → Identity → Logo)."
        ),
    )
    logo_dark = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text=(
            "Logo optimised for dark or inverse backgrounds. "
            "Leave blank to use the master logo."
        ),
    )
    logo_icon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text=(
            "Square icon or favicon candidate (1:1 aspect ratio). "
            "Leave blank to use the master logo. "
            "Recommended size: 512×512 px or larger."
        ),
    )
    logo_display_mode = models.CharField(
        max_length=20,
        choices=LogoDisplayMode.choices,
        default=LogoDisplayMode.AUTO,
        help_text=(
            "Controls the CSS context wrapper applied to the logo in the navbar. "
            "'Auto' works for transparent or legible single-colour logos. "
            "Use 'On card' to add a padded white background for logos that blend with the nav."
        ),
    )
    logo_max_width = models.PositiveSmallIntegerField(
        default=160,
        help_text="Maximum logo width on desktop (px). Default: 160. Keep between 80 and 300.",
    )
    logo_max_width_mobile = models.PositiveSmallIntegerField(
        default=120,
        help_text="Maximum logo width on mobile (px). Default: 120. Must be ≤ desktop max width.",
    )

    # ------------------------------------------------------------------
    # Typography
    # ------------------------------------------------------------------

    typography_preset = models.CharField(
        max_length=30,
        choices=TypographyPreset.choices,
        default=TypographyPreset.BALANCED,
        help_text=(
            "Sets the heading and body type families used across the site. "
            "Applied via CSS custom properties — no font files are uploaded. "
            "Web-safe and Google Fonts variants are bundled with the template."
        ),
    )

    # ------------------------------------------------------------------
    # Brand colors
    # ------------------------------------------------------------------

    color_preset = models.CharField(
        max_length=20,
        choices=ColorPreset.choices,
        default=ColorPreset.NEUTRAL,
        help_text=(
            "Accent color applied to interactive elements, borders, selection, and emphasis details. "
            "Choose 'Custom' and set the accent color field below to use your own hex value."
        ),
    )
    accent_color_custom = models.CharField(
        max_length=7,
        blank=True,
        help_text=(
            "Custom accent hex color, e.g. #B45309. "
            "Only applied when Color Preset is set to 'Custom'. "
            "Must be a 6-digit hex including the # prefix."
        ),
    )

    # ------------------------------------------------------------------
    # Visual style
    # ------------------------------------------------------------------

    visual_style = models.CharField(
        max_length=20,
        choices=VisualStyle.choices,
        default=VisualStyle.BALANCED,
        help_text="Controls corner rounding on cards, buttons, and images across the site.",
    )

    # ------------------------------------------------------------------
    # Social links display
    # ------------------------------------------------------------------

    social_links_display = models.CharField(
        max_length=20,
        choices=SocialLinksDisplay.choices,
        default=SocialLinksDisplay.TEXT,
        help_text=(
            "Controls how social links are rendered in the footer. "
            "'Icons' and 'Icons + text' require icon_slug to be set on each Social Link entry."
        ),
    )

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    class Meta:
        verbose_name = "Brand Settings"
        verbose_name_plural = "Brand Settings"

    def __str__(self) -> str:
        return "Brand Settings"

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def clean(self) -> None:
        errors: dict[str, str] = {}

        if self.color_preset == self.ColorPreset.CUSTOM:
            if not self.accent_color_custom:
                errors["accent_color_custom"] = (
                    "A custom hex color is required when Color Preset is set to 'Custom'. "
                    "Example: #B45309"
                )
            elif not _HEX_COLOR_RE.match(self.accent_color_custom):
                errors["accent_color_custom"] = (
                    "Enter a valid 6-digit hex color including the # prefix, e.g. #B45309."
                )

        if self.logo_max_width_mobile > self.logo_max_width:
            errors["logo_max_width_mobile"] = (
                "Mobile max width cannot exceed desktop max width."
            )

        if errors:
            raise ValidationError(errors)

    # ------------------------------------------------------------------
    # CSS variable generation
    # ------------------------------------------------------------------

    def css_vars(self) -> dict[str, str]:
        """Return a dict of CSS custom property overrides based on current settings.

        Keys are CSS variable names (e.g. '--font-heading').
        Values are the CSS values (e.g. 'Georgia, serif').

        Used by the brand_css_vars template tag to inject an inline <style> block.
        """
        from apps.site.brand_presets import COLOR_PRESETS, TYPOGRAPHY_PRESETS, VISUAL_STYLE_PRESETS

        result: dict[str, str] = {}

        # Typography
        type_map = TYPOGRAPHY_PRESETS.get(self.typography_preset, TYPOGRAPHY_PRESETS["balanced"])
        result["--font-heading"] = type_map["heading"]
        result["--font-body"] = type_map["body"]
        result["--font-accent"] = type_map["accent"]

        # Colors
        if self.color_preset == self.ColorPreset.CUSTOM and self.accent_color_custom:
            # Custom preset: only override the primary accent
            result["--color-brand"] = self.accent_color_custom
        else:
            color_map = COLOR_PRESETS.get(self.color_preset)
            if color_map is None:
                color_map = COLOR_PRESETS["neutral"]  # safe fallback — "neutral" is never None
            result["--color-brand"] = color_map["brand"]  # type: ignore[index]
            result["--color-brand-strong"] = color_map["brand_strong"]  # type: ignore[index]
            result["--color-brand-soft"] = color_map["brand_soft"]  # type: ignore[index]

        # Visual style (radii)
        style_map = VISUAL_STYLE_PRESETS.get(self.visual_style, VISUAL_STYLE_PRESETS["balanced"])
        result["--radius-card"] = style_map["radius_card"]
        result["--radius-button"] = style_map["radius_button"]
        result["--radius-image"] = style_map["radius_image"]

        return result
