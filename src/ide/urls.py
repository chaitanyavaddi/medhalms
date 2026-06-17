from django.urls import path

from . import views

app_name = 'ide'

urlpatterns = [
    path('',                         views.CodingLabsView.as_view(),     name='index'),
    path('<int:lab_id>/',            views.CodingLabsView.as_view(),     name='lab'),
    path('lab/modal/',               views.LabCreateModalView.as_view(), name='lab_create_modal'),
    path('lab/create/',              views.LabCreateView.as_view(),      name='lab_create'),
    path('lab/<int:lab_id>/save/',   views.LabSaveView.as_view(),        name='lab_save'),
    path('lab/<int:lab_id>/delete/', views.LabDeleteView.as_view(),      name='lab_delete'),
]
