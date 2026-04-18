from urllib.parse import urlsplit

from django import template
from django.utils.safestring import mark_safe

from apps.core.brand import compute_monogram
from apps.core.brand import nav_needs_monogram as _brand_nav_needs_monogram

register = template.Library()

# ---------------------------------------------------------------------------
# Navbar monogram — spec v3 (logic lives in apps.core.brand)
# ---------------------------------------------------------------------------


@register.filter
def nav_monogram(site_name: str | None) -> str:
    """Template filter: return the computed monogram for *site_name*."""
    return compute_monogram(site_name or "")


@register.filter
def nav_needs_monogram(site_name: str | None) -> bool:
    """Return True when site_name fails the safe-text test.

    Both conditions must pass for full text to render:
      - character count at or below NAV_TEXT_MAX_CHARS, AND
      - word count at or below NAV_TEXT_MAX_WORDS
    If either fails the monogram path is triggered.
    """
    return _brand_nav_needs_monogram(site_name or "")


@register.filter
def first_paragraph(text: str | None) -> str:
    """Return the first double-newline-separated paragraph of a text block.

    Used on the homepage to show only the opening paragraph of the About-page
    approach text without wrapping the whole multi-paragraph field in a blockquote.
    """
    if not text:
        return ""
    return text.split("\n\n")[0].strip()


@register.simple_tag
def absolute_url(request, value: str | None) -> str:
    """Return *value* as an absolute URL for the current request.

    Absolute URLs are returned unchanged. Relative URLs are resolved against the
    request host using Django's build_absolute_uri(path) behavior.
    """
    if not value:
        return ""
    parsed = urlsplit(value)
    if parsed.scheme and parsed.netloc:
        return value
    return request.build_absolute_uri(value)


@register.simple_tag
def brand_css_vars(brand_settings) -> str:
    """Render an inline <style> block that overrides CSS custom properties.

    Consumes the ``css_vars()`` dict from a BrandSettings instance and emits
    a ``<style>:root{...}</style>`` block suitable for placement in <head>.
    Returns an empty string when brand_settings is None.

    Values come from fixed preset maps (brand_presets.py) or validated hex
    strings — they are not escaped because they are never user free-text.
    """
    if brand_settings is None:
        return mark_safe("")
    css_vars = brand_settings.css_vars()
    if not css_vars:
        return mark_safe("")
    declarations = "\n    ".join(f"{k}: {v};" for k, v in css_vars.items())
    return mark_safe(f"<style>:root {{\n    {declarations}\n}}</style>")
