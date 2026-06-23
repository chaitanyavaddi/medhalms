import json
import secrets
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from authentication.schemas import LoginSchema, SignupSchema
from authentication.tasks import send_welcome_email
from users.models import User
from utils.view_helper import htmx, redirect_to

backend = "django.contrib.auth.backends.ModelBackend"

GOOGLE_AUTH_URL  = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_INFO_URL  = "https://www.googleapis.com/oauth2/v3/userinfo"


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return render(request, 'auth/login.html')

    def post(self, request):
        hx       = htmx(request)
        schema   = LoginSchema.from_post(request)
        ctx      = {'data': request.POST}
        template = 'auth/login.html#login-form' if hx else 'auth/login.html'

        if not schema.is_valid(request):
            return render(request, template, ctx)
        user = authenticate(request, username=schema.email, password=schema.password)
        if not user:
            messages.error(request, 'Invalid email or password')
            return render(request, template, ctx)
        login(request, user, backend=backend)
        messages.success(request, f'Welcome back, {user.first_name or user.email}!')
        return redirect_to(request, 'dashboard:index')


class SignupView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return render(request, 'auth/signup.html')

    def post(self, request):
        hx       = htmx(request)
        schema   = SignupSchema.from_post(request)
        ctx      = {'data': request.POST}
        template = 'auth/signup.html#signup-form' if hx else 'auth/signup.html'

        if not schema.is_valid(request):
            return render(request, template, ctx)
        user = User.objects.create_user(
            email=schema.email,
            password=schema.password,
            first_name=schema.first_name,
            last_name=schema.last_name,
        )
        send_welcome_email.enqueue(user.email)
        login(request, user, backend=backend)
        messages.success(request, f'Welcome to {settings.SITE_NAME}, {user.first_name or user.email}!')
        return redirect_to(request, 'dashboard:index')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('authentication:login')

    def post(self, request):
        logout(request)
        return redirect('authentication:login')


class ForgotPasswordView(View):

    def get(self, request):
        return render(request, 'auth/forgot_password.html')

    def post(self, request):
        email = request.POST.get('email', '').strip()
        if email:
            try:
                user      = User.objects.get(email=email)
                token     = PasswordResetTokenGenerator().make_token(user)
                uidb64    = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(
                    reverse('authentication:reset-password', kwargs={'uidb64': uidb64, 'token': token})
                )
                html = render_to_string('emails/password_reset.html', {
                    'reset_url':   reset_url,
                    'brand_color': settings.BRAND_PRIMARY,
                })
                from core.email import send_email_async
                send_email_async(user.email, 'Reset your password', html)
            except User.DoesNotExist:
                pass
        return render(request, 'auth/forgot_password.html', {'sent': True})


class ResetPasswordConfirmView(View):

    def _get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def get(self, request, uidb64, token):
        user  = self._get_user(uidb64)
        valid = user is not None and PasswordResetTokenGenerator().check_token(user, token)
        return render(request, 'auth/reset_password_confirm.html', {
            'valid': valid, 'uidb64': uidb64, 'token': token,
        })

    def post(self, request, uidb64, token):
        user = self._get_user(uidb64)
        if not user or not PasswordResetTokenGenerator().check_token(user, token):
            return render(request, 'auth/reset_password_confirm.html', {'valid': False})

        password  = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')
        ctx = {'valid': True, 'uidb64': uidb64, 'token': token}

        if not password or not password1:
            messages.error(request, 'Both fields are required')
            return render(request, 'auth/reset_password_confirm.html', ctx)
        if password != password1:
            messages.error(request, "Passwords don't match")
            return render(request, 'auth/reset_password_confirm.html', ctx)

        user.set_password(password)
        user.save()
        login(request, user, backend=backend)
        messages.success(request, 'Password reset successfully. You are now logged in.')
        return redirect_to(request, 'dashboard:index')


class GoogleLoginView(View):

    def get(self, request):
        state = secrets.token_urlsafe(16)
        request.session['google_oauth_state'] = state
        params = {
            'client_id':     settings.GOOGLE_CLIENT_ID,
            'redirect_uri':  request.build_absolute_uri(reverse('authentication:google-callback')),
            'response_type': 'code',
            'scope':         'openid email profile',
            'state':         state,
            'access_type':   'online',
        }
        return redirect(GOOGLE_AUTH_URL + '?' + urllib.parse.urlencode(params))


class GoogleCallbackView(View):

    def get(self, request):
        if request.GET.get('error'):
            messages.error(request, 'Google sign-in was cancelled.')
            return redirect('authentication:login')

        state_in    = request.GET.get('state', '')
        state_saved = request.session.pop('google_oauth_state', '')
        if not state_saved or state_in != state_saved:
            messages.error(request, 'Invalid state. Please try again.')
            return redirect('authentication:login')

        code = request.GET.get('code', '')
        if not code:
            messages.error(request, 'No code returned by Google.')
            return redirect('authentication:login')

        token_data = urllib.parse.urlencode({
            'code':          code,
            'client_id':     settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri':  request.build_absolute_uri(reverse('authentication:google-callback')),
            'grant_type':    'authorization_code',
        }).encode()
        try:
            req = urllib.request.Request(GOOGLE_TOKEN_URL, data=token_data, method='POST')
            with urllib.request.urlopen(req, timeout=10) as resp:
                token_json = json.loads(resp.read())
            info_req = urllib.request.Request(
                GOOGLE_INFO_URL,
                headers={'Authorization': f'Bearer {token_json.get("access_token", "")}'},
            )
            with urllib.request.urlopen(info_req, timeout=10) as resp:
                info = json.loads(resp.read())
        except Exception:
            messages.error(request, 'Could not connect to Google. Please try again.')
            return redirect('authentication:login')

        email = info.get('email', '').lower().strip()
        if not email:
            messages.error(request, 'Google did not return an email address.')
            return redirect('authentication:login')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': info.get('given_name', ''),
                'last_name':  info.get('family_name', ''),
                'avatar':     info.get('picture', ''),
            },
        )
        if created:
            send_welcome_email.enqueue(user.email)
        login(request, user, backend=backend)
        return redirect('dashboard:index')
