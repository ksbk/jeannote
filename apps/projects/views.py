from typing import Any, TypedDict

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .models import Project

# ---------------------------------------------------------------------------
# Project list
# ---------------------------------------------------------------------------


class ProjectListView(ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_public_queryset(self):
        return Project.objects.with_preview_media().all().order_by("order", "-year")

    def get_available_tags(self, queryset):
        """Return sorted list of unique tags present in the queryset."""
        all_tags_raw = queryset.values_list("tags", flat=True)
        seen: dict[str, int] = {}
        for raw in all_tags_raw:
            for tag in (t.strip() for t in raw.split(",") if t.strip()):
                seen[tag] = seen.get(tag, 0) + 1
        return sorted(seen.keys())

    def build_tag_redirect(self, tag=""):
        base_url = reverse("projects:list")
        if not tag:
            return HttpResponseRedirect(base_url)
        params = self.request.GET.copy()
        params["tag"] = tag
        params.pop("category", None)
        return HttpResponseRedirect(f"{base_url}?{params.urlencode()}")

    def dispatch(self, request, *args, **kwargs):
        self.public_projects = self.get_public_queryset()
        self.available_tags = self.get_available_tags(self.public_projects)

        # Backward-compat: ?category= → redirect to ?tag=
        legacy_category = request.GET.get("category", "").strip()
        if legacy_category:
            return self.build_tag_redirect(legacy_category)

        self.active_tag = request.GET.get("tag", "").strip()
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def _tag_filter(qs, tag: str):
        """Exact-match a single tag in a comma-separated tags field."""
        return qs.filter(
            Q(tags=tag)
            | Q(tags__startswith=f"{tag},")
            | Q(tags__endswith=f",{tag}")
            | Q(tags__contains=f",{tag},")
        )

    def get_queryset(self):
        qs = self.public_projects.all()
        if self.active_tag:
            qs = self._tag_filter(qs, self.active_tag)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["available_tags"] = self.available_tags
        ctx["active_tag"] = self.active_tag
        ctx["show_tag_filters"] = len(self.available_tags) > 1
        return ctx


# ---------------------------------------------------------------------------
# Project detail
# ---------------------------------------------------------------------------


class DetailMedia(TypedDict):
    image: Any | None
    alt: str
    dimensions: Any | None


def _resolve_detail_media(project: Project, gallery: list[Any]) -> DetailMedia:
    if project.cover_image:
        return {
            "image": project.cover_image,
            "alt": project.title,
            "dimensions": project.cover_image_dimensions,
        }

    first_gallery = gallery[0] if gallery else None
    if first_gallery:
        return {
            "image": first_gallery.image,
            "alt": first_gallery.get_alt_text(),
            "dimensions": first_gallery.dimensions,
        }

    return {"image": None, "alt": project.title, "dimensions": None}


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project = self.object
        gallery = list(project.images.filter(image_type="gallery"))
        drawings = list(project.images.exclude(image_type="gallery"))
        detail_media = _resolve_detail_media(project, gallery)

        ctx["gallery"] = gallery
        ctx["drawings"] = drawings
        ctx["detail_media"] = detail_media
        first_tag = project.tag_list[0] if project.tag_list else None
        if first_tag:
            related_qs = (
                ProjectListView._tag_filter(
                    Project.objects.with_preview_media(), first_tag
                )
                .exclude(pk=project.pk)
                .order_by("order")
            )
        else:
            related_qs = Project.objects.with_preview_media().exclude(pk=project.pk).order_by("order")
        ctx["related"] = related_qs[:3]
        ctx["testimonials"] = project.testimonials.filter(active=True)
        if detail_media["image"]:
            ctx["og_image"] = detail_media["image"].url
        return ctx
