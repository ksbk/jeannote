"""
Tests for apps.site.services.logo_processor.
"""

import io

import pytest
from PIL import Image

from apps.site.services.logo_processor import (
    LOGO_ICON_SIZE_PX,
    LOGO_MAX_OUTPUT_PX,
    detect_has_transparency,
    generate_icon_candidate,
    process_logo,
    resize_to_max,
    to_content_file,
    trim_whitespace,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_rgb(width=200, height=100, color=(200, 200, 200)):
    img = Image.new("RGB", (width, height), color)
    return img


def _make_rgba(width=200, height=100, color=(200, 200, 200, 255)):
    img = Image.new("RGBA", (width, height), color)
    return img


def _make_rgba_with_transparent_border(inner_size=50, border=20, fill=(0, 0, 0, 255)):
    """RGBA image: transparent border around an opaque inner square."""
    total = inner_size + border * 2
    img = Image.new("RGBA", (total, total), (0, 0, 0, 0))
    inner = Image.new("RGBA", (inner_size, inner_size), fill)
    img.paste(inner, (border, border))
    return img


def _make_white_border_rgb(inner_size=50, border=20, fill=(50, 50, 50)):
    """RGB image: white border around a darker inner square."""
    total = inner_size + border * 2
    img = Image.new("RGB", (total, total), (255, 255, 255))
    inner = Image.new("RGB", (inner_size, inner_size), fill)
    img.paste(inner, (border, border))
    return img


def _encode(img: Image.Image, fmt="PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# detect_has_transparency
# ---------------------------------------------------------------------------


def test_detect_has_transparency_opaque_rgba_returns_false():
    img = _make_rgba(color=(100, 100, 100, 255))
    assert detect_has_transparency(img) is False


def test_detect_has_transparency_with_alpha_returns_true():
    img = _make_rgba_with_transparent_border()
    assert detect_has_transparency(img) is True


def test_detect_has_transparency_rgb_returns_false():
    img = _make_rgb()
    assert detect_has_transparency(img) is False


def test_detect_has_transparency_semi_transparent_returns_true():
    img = Image.new("RGBA", (10, 10), (0, 0, 0, 128))
    assert detect_has_transparency(img) is True


# ---------------------------------------------------------------------------
# trim_whitespace
# ---------------------------------------------------------------------------


def test_trim_whitespace_rgba_removes_transparent_border():
    original = _make_rgba_with_transparent_border(inner_size=50, border=20)
    trimmed = trim_whitespace(original)
    assert trimmed.size == (50, 50)


def test_trim_whitespace_rgb_removes_white_border():
    original = _make_white_border_rgb(inner_size=50, border=20)
    trimmed = trim_whitespace(original)
    assert trimmed.size == (50, 50)


def test_trim_whitespace_no_border_unchanged():
    img = _make_rgb(200, 100, (128, 64, 32))
    result = trim_whitespace(img)
    # Uniform color — no border detected; size preserved (or image returned as-is)
    # The result size may stay the same for uniform-fill images
    assert result.size == img.size


# ---------------------------------------------------------------------------
# resize_to_max
# ---------------------------------------------------------------------------


def test_resize_to_max_larger_image_is_reduced():
    img = _make_rgb(1200, 800)
    result = resize_to_max(img, max_px=LOGO_MAX_OUTPUT_PX)
    assert max(result.size) <= LOGO_MAX_OUTPUT_PX


def test_resize_to_max_preserves_aspect_ratio():
    img = _make_rgb(1200, 600)
    result = resize_to_max(img, max_px=800)
    w, h = result.size
    # Original ratio is 2:1; result should preserve it within rounding
    assert abs(w / h - 2.0) < 0.02


def test_resize_to_max_small_image_unchanged():
    img = _make_rgb(100, 50)
    result = resize_to_max(img, max_px=800)
    assert result.size == (100, 50)


# ---------------------------------------------------------------------------
# generate_icon_candidate
# ---------------------------------------------------------------------------


def test_generate_icon_candidate_output_is_square():
    img = _make_rgba(200, 100)
    icon = generate_icon_candidate(img, size=LOGO_ICON_SIZE_PX)
    w, h = icon.size
    assert w == h == LOGO_ICON_SIZE_PX


def test_generate_icon_candidate_output_is_rgba():
    img = _make_rgb(200, 100)
    icon = generate_icon_candidate(img)
    assert icon.mode == "RGBA"


# ---------------------------------------------------------------------------
# to_content_file
# ---------------------------------------------------------------------------


def test_to_content_file_png_returns_content_file():
    from django.core.files.base import ContentFile

    img = _make_rgba(100, 100)
    cf = to_content_file(img, fmt="PNG", filename="test.png")
    assert isinstance(cf, ContentFile)
    assert cf.name == "test.png"
    assert len(cf) > 0


def test_to_content_file_jpeg_returns_content_file():
    from django.core.files.base import ContentFile

    img = _make_rgb(100, 100)
    cf = to_content_file(img, fmt="JPEG", filename="test.jpg")
    assert isinstance(cf, ContentFile)
    assert cf.name == "test.jpg"


def test_to_content_file_jpeg_flattens_alpha():
    """JPEG encoding of an RGBA image should not raise."""
    img = _make_rgba(100, 100, (50, 100, 150, 200))
    cf = to_content_file(img, fmt="JPEG", filename="flat.jpg")
    assert len(cf) > 0


# ---------------------------------------------------------------------------
# process_logo (integration)
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_process_logo_returns_web_and_icon_candidates():
    img = _make_rgba_with_transparent_border(inner_size=200, border=50)
    source_bytes = _encode(img, fmt="PNG")
    results = process_logo(source_bytes)
    assert "web" in results
    assert "icon" in results


@pytest.mark.django_db
def test_process_logo_web_candidate_within_max_px():
    img = _make_rgb(2000, 1000)
    source_bytes = _encode(img, fmt="PNG")
    results = process_logo(source_bytes, trim=False)
    assert "web" in results
    # Re-open and check dimensions
    web_file = results["web"]
    web_img = Image.open(io.BytesIO(web_file.read()))
    assert max(web_img.size) <= LOGO_MAX_OUTPUT_PX


@pytest.mark.django_db
def test_process_logo_icon_is_square():
    img = _make_rgb(300, 200)
    source_bytes = _encode(img, fmt="PNG")
    results = process_logo(source_bytes, trim=False)
    icon_img = Image.open(io.BytesIO(results["icon"].read()))
    assert icon_img.size == (LOGO_ICON_SIZE_PX, LOGO_ICON_SIZE_PX)


@pytest.mark.django_db
def test_process_logo_invalid_bytes_returns_empty_dict():
    results = process_logo(b"not-an-image")
    assert results == {}


@pytest.mark.django_db
def test_process_logo_no_icon_when_generate_icon_false():
    img = _make_rgb(100, 100)
    source_bytes = _encode(img, fmt="PNG")
    results = process_logo(source_bytes, generate_icon=False)
    assert "web" in results
    assert "icon" not in results
