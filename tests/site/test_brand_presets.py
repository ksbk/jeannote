"""
Tests for apps.site.brand_presets and BrandSettings.css_vars().
"""

import pytest

from apps.site.brand_presets import COLOR_PRESETS, TYPOGRAPHY_PRESETS, VISUAL_STYLE_PRESETS
from apps.site.models import BrandSettings

# ---------------------------------------------------------------------------
# Preset constant integrity
# ---------------------------------------------------------------------------


def test_typography_presets_has_all_expected_keys():
    expected = {"balanced", "editorial_serif", "modern_clean", "technical", "warm_professional"}
    assert set(TYPOGRAPHY_PRESETS.keys()) == expected


def test_typography_presets_each_entry_has_required_keys():
    for name, preset in TYPOGRAPHY_PRESETS.items():
        assert "heading" in preset, f"{name}: missing 'heading'"
        assert "body" in preset, f"{name}: missing 'body'"
        assert "accent" in preset, f"{name}: missing 'accent'"


def test_color_presets_has_all_expected_keys():
    expected = {"neutral", "blue", "green", "burgundy", "amber", "custom"}
    assert set(COLOR_PRESETS.keys()) == expected


def test_color_presets_non_custom_have_required_keys():
    for name, preset in COLOR_PRESETS.items():
        if name == "custom":
            assert preset is None
        else:
            assert preset is not None
            assert "brand" in preset, f"{name}: missing 'brand'"
            assert "brand_strong" in preset, f"{name}: missing 'brand_strong'"
            assert "brand_soft" in preset, f"{name}: missing 'brand_soft'"


def test_visual_style_presets_has_all_expected_keys():
    expected = {"crisp", "balanced", "soft"}
    assert set(VISUAL_STYLE_PRESETS.keys()) == expected


def test_visual_style_presets_each_entry_has_required_keys():
    for name, preset in VISUAL_STYLE_PRESETS.items():
        assert "radius_card" in preset, f"{name}: missing 'radius_card'"
        assert "radius_button" in preset, f"{name}: missing 'radius_button'"
        assert "radius_image" in preset, f"{name}: missing 'radius_image'"


# ---------------------------------------------------------------------------
# BrandSettings.css_vars()
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_css_vars_balanced_default_returns_expected_keys():
    brand = BrandSettings.load()
    # Defaults: balanced typography, neutral color, balanced visual style
    result = brand.css_vars()
    assert "--font-heading" in result
    assert "--font-body" in result
    assert "--font-accent" in result
    assert "--color-brand" in result
    assert "--color-brand-strong" in result
    assert "--color-brand-soft" in result
    assert "--radius-card" in result
    assert "--radius-button" in result
    assert "--radius-image" in result


@pytest.mark.django_db
def test_css_vars_balanced_typography_uses_cormorant():
    brand = BrandSettings.load()
    brand.typography_preset = "balanced"
    result = brand.css_vars()
    assert "Cormorant Garamond" in result["--font-heading"]
    assert "DM Sans" in result["--font-body"]


@pytest.mark.django_db
def test_css_vars_modern_clean_typography_uses_system_ui():
    brand = BrandSettings.load()
    brand.typography_preset = "modern_clean"
    result = brand.css_vars()
    assert "system-ui" in result["--font-heading"]
    assert "system-ui" in result["--font-body"]


@pytest.mark.django_db
def test_css_vars_technical_typography_uses_monospace_heading():
    brand = BrandSettings.load()
    brand.typography_preset = "technical"
    result = brand.css_vars()
    assert "monospace" in result["--font-heading"]


@pytest.mark.django_db
def test_css_vars_neutral_color_uses_warm_bronze():
    brand = BrandSettings.load()
    brand.color_preset = "neutral"
    result = brand.css_vars()
    assert result["--color-brand"] == "#7A6347"


@pytest.mark.django_db
def test_css_vars_blue_color_preset():
    brand = BrandSettings.load()
    brand.color_preset = "blue"
    result = brand.css_vars()
    assert result["--color-brand"] == "#1D4ED8"


@pytest.mark.django_db
def test_css_vars_custom_color_uses_custom_hex():
    brand = BrandSettings.load()
    brand.color_preset = "custom"
    brand.accent_color_custom = "#FF5500"
    result = brand.css_vars()
    assert result["--color-brand"] == "#FF5500"
    # Custom mode only overrides brand — not brand_strong/soft from presets
    assert "--color-brand-strong" not in result


@pytest.mark.django_db
def test_css_vars_crisp_visual_style_has_zero_radius():
    brand = BrandSettings.load()
    brand.visual_style = "crisp"
    result = brand.css_vars()
    assert result["--radius-card"] == "0"
    assert result["--radius-button"] == "0"
    assert result["--radius-image"] == "0"


@pytest.mark.django_db
def test_css_vars_soft_visual_style_has_large_radius():
    brand = BrandSettings.load()
    brand.visual_style = "soft"
    result = brand.css_vars()
    # Soft radii should be non-zero strings
    assert result["--radius-card"] != "0"
    assert result["--radius-button"] != "0"


# ---------------------------------------------------------------------------
# BrandSettings model defaults
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_brand_settings_default_typography_is_balanced():
    brand = BrandSettings.load()
    assert brand.typography_preset == BrandSettings.TypographyPreset.BALANCED


@pytest.mark.django_db
def test_brand_settings_default_color_is_neutral():
    brand = BrandSettings.load()
    assert brand.color_preset == BrandSettings.ColorPreset.NEUTRAL


@pytest.mark.django_db
def test_brand_settings_default_visual_style_is_balanced():
    brand = BrandSettings.load()
    assert brand.visual_style == BrandSettings.VisualStyle.BALANCED


@pytest.mark.django_db
def test_brand_settings_default_social_links_display_is_text():
    brand = BrandSettings.load()
    assert brand.social_links_display == BrandSettings.SocialLinksDisplay.TEXT


@pytest.mark.django_db
def test_brand_settings_default_logo_display_mode_is_auto():
    brand = BrandSettings.load()
    assert brand.logo_display_mode == BrandSettings.LogoDisplayMode.AUTO


@pytest.mark.django_db
def test_brand_settings_default_logo_max_width():
    brand = BrandSettings.load()
    assert brand.logo_max_width == 160
    assert brand.logo_max_width_mobile == 120


@pytest.mark.django_db
def test_brand_settings_singleton():
    a = BrandSettings.load()
    b = BrandSettings.load()
    assert a.pk == b.pk == 1
    assert BrandSettings.objects.count() == 1


# ---------------------------------------------------------------------------
# BrandSettings.clean() validation
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_brand_settings_clean_custom_color_without_hex_raises():
    from django.core.exceptions import ValidationError

    brand = BrandSettings.load()
    brand.color_preset = "custom"
    brand.accent_color_custom = ""
    with pytest.raises(ValidationError) as exc_info:
        brand.clean()
    assert "accent_color_custom" in exc_info.value.message_dict


@pytest.mark.django_db
def test_brand_settings_clean_invalid_hex_raises():
    from django.core.exceptions import ValidationError

    brand = BrandSettings.load()
    brand.color_preset = "custom"
    brand.accent_color_custom = "not-a-hex"
    with pytest.raises(ValidationError) as exc_info:
        brand.clean()
    assert "accent_color_custom" in exc_info.value.message_dict


@pytest.mark.django_db
def test_brand_settings_clean_valid_custom_hex_passes():
    brand = BrandSettings.load()
    brand.color_preset = "custom"
    brand.accent_color_custom = "#B45309"
    brand.clean()  # should not raise


@pytest.mark.django_db
def test_brand_settings_clean_mobile_width_exceeds_desktop_raises():
    from django.core.exceptions import ValidationError

    brand = BrandSettings.load()
    brand.logo_max_width = 100
    brand.logo_max_width_mobile = 150
    with pytest.raises(ValidationError) as exc_info:
        brand.clean()
    assert "logo_max_width_mobile" in exc_info.value.message_dict
