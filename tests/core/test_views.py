"""
View tests for apps.core: home, about, admin, sitemap, robots.txt.
"""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_page(client, site_settings):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_about_page(client, site_settings):
    response = client.get(reverse("core:about"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_login_page_resolves(client):
    """Admin login should redirect or render — never 404/500."""
    response = client.get("/admin/login/")
    assert response.status_code in (200, 302)


# ---------------------------------------------------------------------------
# SEO routes
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_sitemap_returns_200(client, site_settings, project):
    """Sitemap renders with a project present so ProjectSitemap.lastmod/location are exercised."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert b"urlset" in response.content
    assert project.slug.encode() in response.content


@pytest.mark.django_db
def test_robots_txt_returns_200(client, site_settings):
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert b"User-agent" in response.content
    assert b"sitemap.xml" in response.content


# ---------------------------------------------------------------------------
# Home — all_projects excludes featured
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_home_all_projects_excludes_featured(client, site_settings, project):
    """Featured projects should not appear in 'all_projects' context."""
    project.featured = True
    project.save()
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    all_pks = [p.pk for p in response.context["all_projects"]]
    assert project.pk not in all_pks
