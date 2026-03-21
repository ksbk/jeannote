"""
View tests for apps.services: services list page.
"""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_services_page(client, site_settings):
    response = client.get(reverse("services:list"))
    assert response.status_code == 200
