from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('career-paths/', views.CareerPathsView.as_view(), name='career_paths'),
    path('career-paths/<str:role_id>/', views.CareerPathsView.as_view(), name='career_path_detail'),
]
