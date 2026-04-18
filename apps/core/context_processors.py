from apps.site.models import BrandSettings, SiteSettings, SocialLink


def site_settings(request):
    """Make SiteSettings, BrandSettings, and SocialLink entries available in every template."""
    return {
        "site_settings": SiteSettings.load(),
        "brand_settings": BrandSettings.load(),
        "social_links": list(SocialLink.objects.filter(active=True).order_by("order", "label")),
    }
