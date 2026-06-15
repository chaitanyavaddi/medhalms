from django.urls import path
from . import views

urlpatterns = [
    path("", views.overview, name="dashboard_index"),
    path("overview/", views.overview, name="dashboard_overview"),
    path("settings/", views.settings_view, name="dashboard_settings"),
    path("settings/verify-domain/", views.verify_custom_domain, name="dashboard_verify_domain"),
    path("settings/<str:section>/", views.settings_view, name="dashboard_settings_section"),
    path("upload/", views.media_upload, name="dashboard_upload"),
    path("media/delete/", views.media_delete, name="dashboard_media_delete"),
    path("org/delete/", views.org_delete, name="dashboard_org_delete"),
    path("logo/upload/", views.logo_upload, name="dashboard_logo_upload"),
    path("logo/delete/", views.logo_delete, name="dashboard_logo_delete"),
]
