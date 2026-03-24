"""
Admin unit tests for apps.core: SiteSettings and AboutProfile singleton guards.
"""

import pytest
from django.contrib import admin
from django.contrib.messages import WARNING
from django.test import RequestFactory

from apps.core.admin.site import AboutProfileAdmin, SiteSettingsAdmin
from apps.core.models import AboutProfile, SiteSettings


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.mark.django_db
def test_site_settings_admin_allows_add_when_empty(rf):
    a = SiteSettingsAdmin(SiteSettings, admin.site)
    assert a.has_add_permission(rf.get("/admin/")) is True


@pytest.mark.django_db
def test_site_settings_admin_blocks_add_when_row_exists(rf):
    SiteSettings.objects.create(pk=1)
    a = SiteSettingsAdmin(SiteSettings, admin.site)
    assert a.has_add_permission(rf.get("/admin/")) is False


@pytest.mark.django_db
def test_about_profile_admin_allows_add_when_empty(rf):
    a = AboutProfileAdmin(AboutProfile, admin.site)
    assert a.has_add_permission(rf.get("/admin/")) is True


@pytest.mark.django_db
def test_about_profile_admin_blocks_add_when_row_exists(rf):
    AboutProfile.objects.create(pk=1)
    a = AboutProfileAdmin(AboutProfile, admin.site)
    assert a.has_add_permission(rf.get("/admin/")) is False


# ---------------------------------------------------------------------------
# SiteSettingsAdmin.changeform_view — site_name blank warning
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_site_settings_admin_warns_when_site_name_blank(admin_client):
    """A WARNING message appears when the admin views settings with a blank site_name."""
    SiteSettings.objects.update_or_create(pk=1, defaults={"site_name": ""})
    response = admin_client.get("/admin/core/sitesettings/1/change/")
    msgs = list(response.context["messages"])
    assert any(
        m.level == WARNING and "site name" in str(m).lower() for m in msgs
    )


@pytest.mark.django_db
def test_site_settings_admin_no_warning_when_site_name_set(admin_client):
    """No WARNING message when site_name is populated."""
    SiteSettings.objects.update_or_create(pk=1, defaults={"site_name": "My Studio"})
    response = admin_client.get("/admin/core/sitesettings/1/change/")
    msgs = list(response.context["messages"])
    assert not any(
        m.level == WARNING and "site name" in str(m).lower() for m in msgs
    )
