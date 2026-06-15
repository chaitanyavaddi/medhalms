from django.urls import path
from . import views

app_name = "orgs"

urlpatterns = [
    path("", views.OrgListView.as_view(), name="list"),
    path("create/", views.OrgCreateView.as_view(), name="create"),
]
