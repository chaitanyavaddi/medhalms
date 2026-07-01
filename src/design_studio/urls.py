from django.urls import path
from . import views

app_name = 'design_studio'

urlpatterns = [
    path('',                            views.DesignProjectListView.as_view(),    name='list'),
    path('create/',                     views.DesignProjectCreateView.as_view(),  name='create'),
    path('<int:pk>/edit/',              views.DesignProjectUpdateView.as_view(),  name='edit'),
    path('<int:pk>/delete/',            views.DesignProjectDeleteView.as_view(),  name='delete'),
    path('<int:pk>/workspace/',         views.DesignWorkspaceView.as_view(),      name='workspace'),
    path('<int:pk>/autosave/',          views.DesignAutosaveView.as_view(),       name='autosave'),
    path('<int:pk>/submit/',            views.DesignSubmitView.as_view(),         name='submit'),
    path('<int:pk>/submissions/',       views.DesignSubmissionListView.as_view(), name='submissions'),
    path('assets/upload/',             views.DesignAssetUploadView.as_view(),    name='asset_upload'),
]
