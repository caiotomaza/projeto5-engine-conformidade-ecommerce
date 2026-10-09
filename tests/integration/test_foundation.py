import pytest
from django.conf import settings
from django.urls import reverse

@pytest.mark.django_db
def test_health_endpoint(client):
    response = client.get(reverse("core:health"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_sqlite_is_configured():
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
