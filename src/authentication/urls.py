from django.urls import path
from . import views

urlpatterns = [
    path("login/",   views.LoginView.as_view(),   name="auth_login"),
    path("signup/",  views.SignupView.as_view(),   name="auth_signup"),
    path("logout/",  views.LogoutView.as_view(),   name="auth_logout"),
    path("forgot-password/", views.ForgotPasswordView.as_view(), name="auth_forgot_password"),
    path("reset-password/<uidb64>/<token>/", views.ResetPasswordConfirmView.as_view(), name="auth_reset_password"),
    path("auth/google/",          views.google_login,    name="google_login"),
    path("auth/google/callback/", views.google_callback, name="google_callback"),
]
