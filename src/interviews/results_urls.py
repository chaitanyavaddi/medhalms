from django.urls import path
from . import views

app_name = 'mock_results'

urlpatterns = [
    path('interviews/', views.InterviewResultsView.as_view(), name='interviews'),
]
