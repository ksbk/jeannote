"""
Model tests for apps.services: Service.
"""

import pytest

from apps.services.models import Service


@pytest.mark.django_db
def test_service_str(service):
    assert str(service) == "Architectural Design"


@pytest.mark.django_db
def test_service_slug_auto_generated():
    s = Service.objects.create(title="Urban Planning", order=10, active=True)
    assert s.slug == "urban-planning"


@pytest.mark.django_db
def test_service_deliverables_list(db):
    s = Service.objects.create(
        title="Test Service",
        order=1,
        active=True,
        deliverables="Item one\nItem two\nItem three",
    )
    items = s.deliverables_list()
    assert len(items) == 3
    assert "Item one" in items
