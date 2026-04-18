from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, ClassVar

from django.db import models
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify

# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------



def get_safe_image_dimensions(image) -> dict[str, int] | None:
    if not image:
        return None
    with contextlib.suppress(Exception):
        width = int(image.width)
        height = int(image.height)
        if width > 0 and height > 0:
            return {"width": width, "height": height}
    return None


class ProjectQuerySet(models.QuerySet):
    def with_preview_media(self) -> ProjectQuerySet:
        return self.prefetch_related(
            Prefetch(
                "images",
                queryset=ProjectImage.objects.filter(image_type="gallery").order_by("order"),
                to_attr="_preview_gallery_images",
            )
        )


class ProjectManager(models.Manager):
    def get_queryset(self) -> ProjectQuerySet:
        return ProjectQuerySet(self.model, using=self._db)

    def with_preview_media(self) -> ProjectQuerySet:
        return self.get_queryset().with_preview_media()


class Project(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("in_progress", "In Progress"),
        ("concept", "Concept"),
        ("competition", "Competition Entry"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(
        max_length=300,
        help_text="One or two clear sentences shown on project cards and in search results. Under 160 characters is ideal.",
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Comma-separated tags, e.g. \"housing, residential\". Used to group and filter projects.",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="completed")

    # Location & metadata
    location = models.CharField(max_length=150, blank=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    client = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=60, blank=True, help_text='e.g. "2 400 m²"')
    services_provided = models.TextField(
        blank=True,
        help_text="Scope of services delivered, e.g. 'Concept design through construction administration.' One service per line.",
    )

    # Story
    overview = models.TextField(blank=True, help_text="Project introduction paragraph.")
    challenge = models.TextField(blank=True)
    concept = models.TextField(blank=True)
    process = models.TextField(
        blank=True,
        help_text="Optional — describe the design and construction process, methods used, or team collaboration.",
    )
    outcome = models.TextField(blank=True)

    # Media
    cover_image = models.ImageField(
        upload_to="projects/covers/",
        blank=True,
        null=True,
        help_text="Recommended: at least 1600 × 900 px, JPEG or WebP. Used as the hero image and OpenGraph share image.",
    )

    # Flags
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    # SEO
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Overrides project title in browser tab and search results. Ideal length: under 60 characters.",
    )
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Overrides short description in search results. Under 160 characters.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: ClassVar[ProjectManager] = ProjectManager()

    class Meta:
        ordering = ["order", "-year", "title"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    def get_seo_title(self):
        return self.seo_title or self.title

    def get_seo_description(self):
        return self.seo_description or self.short_description

    @property
    def tag_list(self) -> list[str]:
        """Return a stripped list of individual tags."""
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    @cached_property
    def preview_gallery_image(self):
        prefetched = getattr(self, "_preview_gallery_images", None)
        if prefetched is not None:
            return prefetched[0] if prefetched else None
        return self.images.filter(image_type="gallery").order_by("order").first()

    @cached_property
    def preview_image(self):
        if self.cover_image:
            return self.cover_image
        preview_gallery = self.preview_gallery_image
        return preview_gallery.image if preview_gallery else None

    @cached_property
    def preview_image_alt(self):
        if self.cover_image:
            return self.title
        preview_gallery = self.preview_gallery_image
        return preview_gallery.get_alt_text() if preview_gallery else self.title

    @cached_property
    def cover_image_dimensions(self):
        return get_safe_image_dimensions(self.cover_image)

    @cached_property
    def preview_image_dimensions(self):
        return get_safe_image_dimensions(self.preview_image)

    if TYPE_CHECKING:
        from django.db.models import Manager

        images: Manager[ProjectImage]
        testimonials: Manager[Testimonial]


# ---------------------------------------------------------------------------
# ProjectImage
# ---------------------------------------------------------------------------


class ProjectImage(models.Model):
    TYPE_CHOICES = [
        ("gallery", "Gallery"),
        ("plan", "Floor Plan"),
        ("section", "Section / Elevation"),
        ("sketch", "Sketch"),
        ("detail", "Detail"),
        ("render", "Render"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Descriptive alt text for screen readers. Falls back to caption if empty.",
    )
    order = models.PositiveIntegerField(default=0)
    image_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="gallery")

    class Meta:
        ordering = ["order"]
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"{self.project.title} — image {self.order}"

    def get_alt_text(self):
        """Return alt_text if set, falling back to caption, then project title."""
        return self.alt_text or self.caption or self.project.title

    @cached_property
    def dimensions(self):
        return get_safe_image_dimensions(self.image)


# ---------------------------------------------------------------------------
# Testimonial
# ---------------------------------------------------------------------------


class Testimonial(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
        help_text=(
            "The project this testimonial is associated with. "
            "Testimonials without a project are stored but not rendered on any public page "
            "— only project-linked testimonials appear on project detail pages."
        ),
    )
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    quote = models.TextField()
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} — {self.role or 'Client'}"
