from django.views.generic import ListView

from .models import Service


class ServicesView(ListView):
    model = Service
    template_name = "services/services.html"
    context_object_name = "services"
    queryset = Service.objects.filter(active=True)
