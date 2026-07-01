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
    path('<int:pk>/submissions/',                          views.DesignSubmissionListView.as_view(),    name='submissions'),
    path('<int:pk>/submissions/<int:sub_pk>/',             views.DesignSubmissionDetailView.as_view(),  name='submission_detail'),
    path('<int:pk>/submissions/<int:sub_pk>/preview/',    views.DesignSubmissionPreviewView.as_view(), name='submission_preview'),
    path('<int:pk>/submissions/<int:sub_pk>/approve/',    views.DesignSubmissionApproveView.as_view(), name='submission_approve'),
    path('<int:pk>/submissions/<int:sub_pk>/send-back/',  views.DesignSubmissionSendBackView.as_view(), name='submission_send_back'),
    path('<int:pk>/submissions/<int:sub_pk>/delete/',     views.DesignSubmissionDeleteView.as_view(),  name='submission_delete'),
    path('assets/upload/',                                views.DesignAssetUploadView.as_view(),       name='asset_upload'),
]
