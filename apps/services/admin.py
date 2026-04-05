from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "summary", "order", "active")
    list_editable = ("order", "active")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Identity", {"fields": ("title", "slug", "summary")}),
        (
            "Detail",
            {
                "fields": ("description", "who_for", "value_proposition", "deliverables"),
                "classes": ("collapse",),
            },
        ),
        ("Display", {"fields": ("order", "active")}),
    )
