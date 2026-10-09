import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_page(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    assert "Engine de Conformidade Regulatória" in response.content.decode()
