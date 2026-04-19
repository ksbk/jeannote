from django.http import Http404
from django.views.generic import DetailView, ListView

from apps.site.models import SiteSettings

from .models import Post


class PostListView(ListView):
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        if not SiteSettings.load().blog_enabled:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by("-published_date", "title")


class PostDetailView(DetailView):
    template_name = "blog/detail.html"
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        if not SiteSettings.load().blog_enabled:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(is_published=True)
