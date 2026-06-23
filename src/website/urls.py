from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('',            views.HomeView.as_view(),      name='home'),
    path('favicon.svg', views.FaviconView.as_view(),   name='favicon_svg'),
    path('robots.txt',  views.RobotsTxtView.as_view(), name='robots_txt'),
]
