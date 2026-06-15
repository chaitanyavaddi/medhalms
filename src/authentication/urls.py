from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path("login/",    views.LoginView.as_view(),               name="login"),
    path("signup/",   views.SignupView.as_view(),              name="signup"),
    path("logout/",   views.LogoutView.as_view(),              name="logout"),
    path("forgot-password/",                       views.ForgotPasswordView.as_view(),     name="forgot-password"),
    path("reset-password/<uidb64>/<token>/",       views.ResetPasswordConfirmView.as_view(), name="reset-password"),
    path("auth/google/",          views.GoogleLoginView.as_view(),    name="google-login"),
    path("auth/google/callback/", views.GoogleCallbackView.as_view(), name="google-callback"),
]
