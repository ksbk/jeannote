"""
Brand preset constants for the v1.4.0 Brand Customization System.

Maps named preset keys → CSS custom property values.
Imported by:
  - apps.site.models.brand   (BrandSettings.css_vars())
  - apps.core.templatetags.core_tags  (brand_css_vars template tag)
  - tests
"""

# ---------------------------------------------------------------------------
# Typography presets
# ---------------------------------------------------------------------------

# Maps typography_preset → CSS font-family values for heading, body, and accent.
# The 'balanced' preset intentionally mirrors the default token values in
# static/css/base/tokens.css so the generated <style> block is a no-op until
# the client selects a different preset.

TYPOGRAPHY_PRESETS: dict[str, dict[str, str]] = {
    "balanced": {
        "heading": "'Cormorant Garamond', Georgia, serif",
        "body": "'DM Sans', system-ui, -apple-system, sans-serif",
        "accent": "'DM Sans', system-ui, -apple-system, sans-serif",
    },
    "editorial_serif": {
        "heading": "'Cormorant Garamond', Georgia, serif",
        "body": "Georgia, 'Times New Roman', serif",
        "accent": "Georgia, serif",
    },
    "modern_clean": {
        "heading": "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
        "body": "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
        "accent": "system-ui, -apple-system, sans-serif",
    },
    "technical": {
        "heading": "'Courier New', Courier, monospace",
        "body": "system-ui, -apple-system, sans-serif",
        "accent": "'Courier New', Courier, monospace",
    },
    "warm_professional": {
        "heading": "Palatino, 'Palatino Linotype', 'Book Antiqua', serif",
        "body": "system-ui, -apple-system, sans-serif",
        "accent": "Palatino, 'Palatino Linotype', serif",
    },
}

# ---------------------------------------------------------------------------
# Color presets
# ---------------------------------------------------------------------------

# Maps color_preset → brand color values.
# 'custom' is None — the caller substitutes accent_color_custom.
# brand:        primary accent color
# brand_strong: dark variant (used for --color-brand-strong)
# brand_soft:   light tint (used for --color-brand-soft)

COLOR_PRESETS: dict[str, dict[str, str] | None] = {
    "neutral": {
        "brand": "#7A6347",
        "brand_strong": "#1A1917",
        "brand_soft": "#F2EEE9",
    },
    "blue": {
        "brand": "#1D4ED8",
        "brand_strong": "#1E3A8A",
        "brand_soft": "#EFF6FF",
    },
    "green": {
        "brand": "#166534",
        "brand_strong": "#14532D",
        "brand_soft": "#F0FDF4",
    },
    "burgundy": {
        "brand": "#881337",
        "brand_strong": "#4C0519",
        "brand_soft": "#FFF1F2",
    },
    "amber": {
        "brand": "#B45309",
        "brand_strong": "#451A03",
        "brand_soft": "#FFFBEB",
    },
    "custom": None,
}

# ---------------------------------------------------------------------------
# Visual style presets (border-radius)
# ---------------------------------------------------------------------------

# Maps visual_style → CSS custom property values for card, button, and image radii.

VISUAL_STYLE_PRESETS: dict[str, dict[str, str]] = {
    "crisp": {
        "radius_card": "0",
        "radius_button": "0",
        "radius_image": "0",
    },
    "balanced": {
        "radius_card": "0.375rem",
        "radius_button": "0.25rem",
        "radius_image": "0",
    },
    "soft": {
        "radius_card": "1rem",
        "radius_button": "2rem",
        "radius_image": "0.5rem",
    },
}
