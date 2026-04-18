"""
Logo processing utilities for the v1.4.0 Brand Customization System.

Pillow-based helpers for trimming, resizing, and inspecting uploaded logos.
Pure Python — no Django model imports. Call from admin actions or management
commands; do not call from model.save() to keep models thin.

Typical workflow
----------------
1. User uploads master logo via SiteSettings.logo.
2. Admin calls process_logo(site_settings.logo) to get candidates.
3. Store results back on BrandSettings logo_light / logo_dark / logo_icon as
   needed, or leave blank to use the master logo fallback chain.
"""

from __future__ import annotations

import io
from typing import TYPE_CHECKING

from PIL import Image, ImageChops

if TYPE_CHECKING:
    from django.core.files.base import ContentFile

# Maximum output dimension for optimised web logo files.
LOGO_MAX_OUTPUT_PX: int = 800

# Canonical square size for icon candidates.
LOGO_ICON_SIZE_PX: int = 512


# ---------------------------------------------------------------------------
# Low-level image utilities
# ---------------------------------------------------------------------------


def detect_has_transparency(img: Image.Image) -> bool:
    """Return True if *img* has any fully or partially transparent pixels."""
    if img.mode == "RGBA":
        alpha = img.split()[-1]
        # getextrema() returns (min, max) — if min < 255 any pixel is non-opaque
        extrema = alpha.getextrema()
        return extrema[0] < 255  # type: ignore[operator]
    if img.mode == "LA":
        alpha = img.split()[-1]
        return alpha.getextrema()[0] < 255  # type: ignore[operator]
    if img.mode == "P":
        # Palette mode may have a transparency index
        return "transparency" in img.info
    return False


def trim_whitespace(img: Image.Image) -> Image.Image:
    """Crop transparent or white/near-white border from *img*.

    For RGBA images the alpha channel is used as the bounding box mask.
    For RGB images white (255, 255, 255) is treated as background.
    Returns *img* unchanged if no border is detected.
    """
    if img.mode == "RGBA":
        alpha = img.split()[-1]
        bbox = alpha.getbbox()  # (left, upper, right, lower) of non-transparent pixels
        if bbox:
            return img.crop(bbox)
        return img

    # For RGB (and anything else) compare against solid white
    rgb = img.convert("RGB")
    bg = Image.new("RGB", rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, bg)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def resize_to_max(img: Image.Image, max_px: int = LOGO_MAX_OUTPUT_PX) -> Image.Image:
    """Resize *img* so its longest dimension does not exceed *max_px*.

    Aspect ratio is preserved. Images already within *max_px* are returned
    unchanged (no upscaling).
    """
    w, h = img.size
    if max(w, h) <= max_px:
        return img
    if w >= h:
        new_w = max_px
        new_h = round(h * max_px / w)
    else:
        new_h = max_px
        new_w = round(w * max_px / h)
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)


def generate_icon_candidate(img: Image.Image, size: int = LOGO_ICON_SIZE_PX) -> Image.Image:
    """Crop *img* to a centred square and resize to *size* × *size* px.

    The input is expected to already be trimmed. A transparent RGBA canvas is
    used so SVG/PNG logos with transparency render cleanly.
    """
    # Ensure RGBA so we can compose on transparent canvas
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    w, h = img.size
    side = min(w, h)

    # Centred crop to square
    left = (w - side) // 2
    top = (h - side) // 2
    cropped = img.crop((left, top, left + side, top + side))

    return cropped.resize((size, size), Image.Resampling.LANCZOS)


# ---------------------------------------------------------------------------
# High-level processing entry point
# ---------------------------------------------------------------------------


def to_content_file(img: Image.Image, fmt: str = "PNG", filename: str = "logo.png") -> ContentFile:
    """Encode *img* as *fmt* and return a Django ContentFile ready to save.

    PNG is the default to preserve transparency. Pass fmt="JPEG" for opaque logos.
    """
    from django.core.files.base import ContentFile

    buf = io.BytesIO()
    save_kwargs: dict[str, object] = {}
    if fmt == "PNG":
        save_kwargs["optimize"] = True
    elif fmt == "JPEG":
        # Flatten alpha before JPEG encoding to prevent conversion errors
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
            img = bg
        save_kwargs["quality"] = 90
    img.save(buf, format=fmt, **save_kwargs)
    buf.seek(0)
    return ContentFile(buf.read(), name=filename)


def process_logo(
    source_bytes: bytes,
    *,
    trim: bool = True,
    max_px: int = LOGO_MAX_OUTPUT_PX,
    generate_icon: bool = True,
    icon_size: int = LOGO_ICON_SIZE_PX,
) -> dict[str, ContentFile]:
    """Process a raw logo image and return a dict of ContentFile candidates.

    Args:
        source_bytes: Raw bytes of the uploaded logo file.
        trim:         Strip transparent/white borders before processing.
        max_px:       Maximum output dimension for the web-optimised variant.
        generate_icon: Whether to produce a square icon candidate.
        icon_size:    Target side length (px) for the icon candidate.

    Returns:
        dict with keys:
          ``"web"``   — trimmed + resized logo, PNG, suitable for logo_light/logo_dark.
          ``"icon"``  — square icon candidate, PNG (only if generate_icon=True).
        Missing keys mean that step was skipped or failed silently.
    """
    results: dict[str, ContentFile] = {}

    try:
        img: Image.Image = Image.open(io.BytesIO(source_bytes))
        img.load()  # force decode so errors surface here
    except Exception:
        return results  # unreadable file — caller handles the empty dict

    if trim:
        img = trim_whitespace(img)

    web_img = resize_to_max(img, max_px=max_px)
    results["web"] = to_content_file(web_img, fmt="PNG", filename="logo_web.png")

    if generate_icon:
        icon_img = generate_icon_candidate(img, size=icon_size)
        results["icon"] = to_content_file(icon_img, fmt="PNG", filename="logo_icon.png")

    return results
