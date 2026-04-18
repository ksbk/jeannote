from django.http import Http404
from django.views.generic import ListView

from apps.site.models import SiteSettings

from .models import ServiceItem


class ServiceListView(ListView):
    template_name = "services/list.html"
    context_object_name = "services"

    def dispatch(self, request, *args, **kwargs):
        site = SiteSettings.load()
        if not site.services_enabled:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ServiceItem.objects.filter(active=True)
