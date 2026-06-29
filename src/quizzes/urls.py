from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('',                                    views.QuizListView.as_view(),         name='list'),
    path('create/',                             views.QuizCreateView.as_view(),       name='create'),
    path('wizard/',                             views.QuizWizardView.as_view(),       name='wizard'),
    path('<int:pk>/edit/',                      views.QuizUpdateView.as_view(),       name='edit'),
    path('<int:pk>/delete/',                    views.QuizDeleteView.as_view(),       name='delete'),
    path('<int:pk>/questions/',                 views.QuizBuilderView.as_view(),      name='builder'),

    # Question CRUD (HTMX partials)
    path('<int:pk>/questions/add/',             views.QuestionAddView.as_view(),      name='question_add'),
    path('<int:pk>/questions/<int:qpk>/edit/',  views.QuestionEditView.as_view(),     name='question_edit'),
    path('<int:pk>/questions/<int:qpk>/delete/',views.QuestionDeleteView.as_view(),   name='question_delete'),
    path('<int:pk>/questions/reorder/',         views.QuestionReorderView.as_view(),  name='question_reorder'),

    # Labs picker (HTMX modal)
    path('labs-picker/',                        views.LabsPickerView.as_view(),       name='labs_picker'),

    # Student take flow
    path('<int:pk>/take/',                      views.QuizTakeView.as_view(),         name='take'),
    path('<int:pk>/submit/',                    views.QuizSubmitView.as_view(),       name='submit'),
    path('<int:pk>/attempts/<int:apk>/',        views.AttemptResultView.as_view(),    name='attempt_result'),
]
