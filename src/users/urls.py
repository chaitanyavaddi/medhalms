from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('',          views.UserManageView.as_view(), name='manage'),
    path('students/', views.UserRoleView.as_view(), {'role_slug': 'students'}, name='students'),
    path('trainers/', views.UserRoleView.as_view(), {'role_slug': 'trainers'}, name='trainers'),
    path('staff/',    views.UserRoleView.as_view(), {'role_slug': 'staff'},    name='staff'),
    path('admins/',   views.UserRoleView.as_view(), {'role_slug': 'admins'},   name='admins'),
    path('create/',          views.UserCreateView.as_view(),  name='create'),
    path('<int:pk>/edit/',   views.UserUpdateView.as_view(),  name='edit'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(),  name='delete'),
]
