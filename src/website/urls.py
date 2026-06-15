from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.main_robots_txt, name="main_robots_txt"),
]
