"""
Model tests for apps.contact: ContactInquiry.
"""

import pytest

from apps.contact.models import ContactInquiry


@pytest.mark.django_db
def test_contact_inquiry_default_status(db):
    inq = ContactInquiry.objects.create(
        name="Alice",
        email="alice@example.com",
        message="Hello, I'd like to enquire.",
    )
    assert inq.status == "new"
    assert "Alice" in str(inq)
