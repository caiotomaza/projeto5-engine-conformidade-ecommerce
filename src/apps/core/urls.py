from django.urls import path
from .views import health, home
app_name = "core"
urlpatterns = [path("", home, name="home"), path("health/", health, name="health")]
