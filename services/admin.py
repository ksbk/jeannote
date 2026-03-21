from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "summary", "order", "active")
    list_editable = ("order", "active")
    prepopulated_fields = {"slug": ("title",)}
