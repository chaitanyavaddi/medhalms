from django.urls import path
from . import views

urlpatterns = [
    path("",           views.home,           name="home"),
    path("favicon.svg", views.favicon_svg,   name="favicon_svg"),
    path("robots.txt", views.main_robots_txt, name="main_robots_txt"),
]
