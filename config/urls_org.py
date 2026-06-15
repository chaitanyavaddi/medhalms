from django.urls import path, include
from website import views as website_views

urlpatterns = [
    path("favicon.svg", website_views.favicon_svg, name="favicon_svg"),
    path("dashboard/", include("dashboard.urls")),
    path("", include("authentication.urls")),
]
