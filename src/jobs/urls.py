from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('',                     views.JobBoardView.as_view(),       name='board'),
    path('list/',                views.JobListPartialView.as_view(), name='list'),
    path('<str:job_id>/detail/', views.JobDetailView.as_view(),      name='detail'),
    path('<str:job_id>/save/',   views.JobSaveToggleView.as_view(),  name='save_toggle'),
]
