from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('',         views.CourseListView.as_view(),   name='list'),
    path('create/',  views.CourseCreateView.as_view(), name='create'),
    path('upload/',      views.CourseUploadView.as_view(),     name='upload'),
    path('file-delete/', views.CourseFileDeleteView.as_view(), name='file_delete'),

    path('<int:pk>/',       views.CourseDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/',  views.CourseUpdateView.as_view(), name='edit'),

    path('<int:pk>/c/<int:chapter_pk>/',
         views.ChapterDetailView.as_view(), name='chapter'),
    path('<int:pk>/c/<int:chapter_pk>/save/',
         views.ChapterSaveView.as_view(), name='chapter_save'),

    path('<int:pk>/modules/create/',
         views.ModuleCreateView.as_view(), name='module_create'),
    path('<int:pk>/modules/<int:module_pk>/edit/',
         views.ModuleUpdateView.as_view(), name='module_edit'),
    path('<int:pk>/modules/<int:module_pk>/delete/',
         views.ModuleDeleteView.as_view(), name='module_delete'),

    path('<int:pk>/modules/<int:module_pk>/chapters/create/',
         views.ChapterCreateView.as_view(), name='chapter_create'),
    path('<int:pk>/modules/<int:module_pk>/chapters/<int:chapter_pk>/edit/',
         views.ChapterUpdateView.as_view(), name='chapter_edit'),
    path('<int:pk>/modules/<int:module_pk>/chapters/<int:chapter_pk>/delete/',
         views.ChapterDeleteView.as_view(), name='chapter_delete'),
]
