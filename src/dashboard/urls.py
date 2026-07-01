from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('pending-approval/', views.PendingApprovalView.as_view(), name='pending_approval'),
    path('', views.HomeView.as_view(), name='index'),
    path('career-paths/', views.CareerPathsView.as_view(), name='career_paths'),
    # skills/ must come before <roadmap_id>/ to avoid being matched as an id
    path('career-paths/skills/', views.CareerPathsView.as_view(), {'tab': 'skills'}, name='career_paths_skills'),
    path('career-paths/<str:roadmap_id>/', views.CareerPathsView.as_view(), name='career_path_detail'),
]
