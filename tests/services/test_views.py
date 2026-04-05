"""
View tests for apps.services: services list page.
"""

import pytest
from django.urls import reverse

from apps.services.models import Service


@pytest.mark.django_db
def test_services_page(client, site_settings):
    Service.objects.create(
        title="Housing",
        slug="housing",
        summary="Housing projects.",
        order=1,
        active=True,
    )

    response = client.get(reverse("services:list"))
    assert response.status_code == 200
    assert b"Professional support for complex projects" in response.content
    assert b"Architectural Services" not in response.content
    assert b"Enquire About This Service" in response.content


@pytest.mark.django_db
def test_services_empty_state_uses_template_neutral_copy(client, site_settings):
    Service.objects.all().delete()

    response = client.get(reverse("services:list"))

    assert response.status_code == 200
    assert b"planning, design, and delivery support" in response.content
    assert b"getting in touch with a short outline" in response.content


@pytest.mark.django_db
def test_services_page_uses_mapped_contact_project_type_query_param(client, site_settings):
    Service.objects.create(
        title="Workplace",
        slug="workplace",
        summary="Workplace projects.",
        order=1,
        active=True,
    )

    response = client.get(reverse("services:list"))

    assert response.status_code == 200
    assert b"?project_type=Workplace" in response.content


@pytest.mark.django_db
def test_services_page_renders_service_description_when_present(client, site_settings):
    Service.objects.create(
        title="Strategy",
        slug="strategy",
        summary="Strategic support.",
        description="Line one.\n\nLine two.",
        order=1,
        active=True,
    )

    response = client.get(reverse("services:list"))

    assert response.status_code == 200
    assert b"Line one." in response.content
    assert b"Line two." in response.content
