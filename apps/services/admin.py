from django.contrib import admin

from .models import ServiceItem


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "active")
    list_editable = ("order", "active")
    list_display_links = ("name",)
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "short_description", "long_description", "order", "active"),
                "description": (
                    "Each active service appears on the public Services page and in the homepage "
                    "services preview (when the Services module is enabled in Site Settings)."
                ),
            },
        ),
    )
