from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [
    path('',                              views.InterviewListView.as_view(),    name='list'),
    path('create/',                       views.InterviewCreateView.as_view(),  name='create'),
    path('<int:pk>/edit/',                views.InterviewUpdateView.as_view(),  name='edit'),
    path('<int:pk>/delete/',              views.InterviewDeleteView.as_view(),  name='delete'),
    path('<int:pk>/',                     views.InterviewDetailView.as_view(),  name='detail'),
    path('<int:pk>/start/',               views.SessionStartView.as_view(),     name='session_start'),
    path('session/<int:session_pk>/',     views.SessionRoomView.as_view(),      name='session_room'),
    path('session/<int:session_pk>/answer/', views.AnswerSaveView.as_view(),    name='answer_save'),
    path('session/<int:session_pk>/end/', views.SessionEndView.as_view(),       name='session_end'),
    path('session/<int:session_pk>/result/', views.SessionResultView.as_view(), name='session_result'),
]
