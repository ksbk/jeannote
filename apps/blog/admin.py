from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "is_published", "tags")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "summary", "body")}),
        ("Publishing", {"fields": ("published_date", "is_published")}),
        ("Taxonomy", {"fields": ("tags",)}),
    )
    search_fields = ("title", "summary", "tags")
    list_filter = ("is_published",)
    date_hierarchy = "published_date"
