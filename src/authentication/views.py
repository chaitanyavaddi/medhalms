import json
import secrets
import urllib.parse
import urllib.request

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from users.models import User
from utils.view_helper import htmx, redirect_to

backend = "django.contrib.auth.backends.ModelBackend"

GOOGLE_AUTH_URL  = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_INFO_URL  = "https://www.googleapis.com/oauth2/v3/userinfo"


def _send_welcome_email(user):
    from core.email import send_email_async
    brand_color = getattr(settings, 'BRAND_PRIMARY', '#3730a3')
    html = render_to_string('emails/welcome.html', {'brand_color': brand_color})
    send_email_async(user.email, 'Welcome', html)


def _user_home(user):
    from orgs.models import OrgMember
    membership = OrgMember.objects.filter(user=user).select_related('org').first()
    if membership:
        scheme = 'http' if settings.DEBUG else 'https'
        main = getattr(settings, 'MAIN_DOMAIN', 'localhost:8000')
        return f'{scheme}://{membership.org.subdomain}.{main}/dashboard/'
    return '/orgs/create/'


def _redirect_if_subdomain(request, path):
    if getattr(request, 'org', None):
        main = getattr(settings, 'MAIN_DOMAIN', 'localhost:8000')
        return redirect(f'http://{main}{path}')
    return None


class LoginView(View):

    def get(self, request):
        r = _redirect_if_subdomain(request, '/login/')
        if r: return r
        if request.user.is_authenticated:
            return redirect("orgs:list")
        return render(request, "auth/login.html")

    def post(self, request):
        hx       = htmx(request)
        ctx      = {"data": request.POST}
        email    = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        template = "auth/login.html#login-form" if hx else "auth/login.html"

        if not email or not password:
            messages.error(request, "All fields are required")
            return render(request, template, ctx)
        user = authenticate(request, username=email, password=password)
        if not user:
            messages.error(request, "Invalid email or password")
            return render(request, template, ctx)
        login(request, user, backend=backend)
        return redirect_to(request, _user_home(user))


class SignupView(View):

    def get(self, request):
        r = _redirect_if_subdomain(request, '/signup/')
        if r: return r
        if request.user.is_authenticated:
            return redirect("orgs:list")
        return render(request, "auth/signup.html")

    def post(self, request):
        hx        = htmx(request)
        ctx       = {"data": request.POST}
        email     = request.POST.get("email", "").strip()
        password  = request.POST.get("password", "")
        password1 = request.POST.get("password1", "")
        template  = "auth/signup.html#signup-form" if hx else "auth/signup.html"

        if not email or not password or not password1:
            messages.error(request, "All fields are required")
            return render(request, template, ctx)
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, template, ctx)
        if password != password1:
            messages.error(request, "Passwords don't match")
            return render(request, template, ctx)
        user = User.objects.create_user(email=email, password=password)
        _send_welcome_email(user)
        login(request, user, backend=backend)
        return redirect_to(request, "orgs:create")


class LogoutView(View):

    def get(self, request):
        logout(request)
        main = getattr(settings, "MAIN_DOMAIN", "localhost:8000")
        return redirect(f"http://{main}/")

    def post(self, request):
        logout(request)
        main = getattr(settings, "MAIN_DOMAIN", "localhost:8000")
        return redirect(f"http://{main}/")


class ForgotPasswordView(View):

    def get(self, request):
        r = _redirect_if_subdomain(request, '/forgot-password/')
        if r: return r
        return render(request, 'auth/forgot_password.html')

    def post(self, request):
        email = request.POST.get('email', '').strip()
        if email:
            try:
                user = User.objects.get(email=email)
                token  = PasswordResetTokenGenerator().make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                main = getattr(settings, 'MAIN_DOMAIN', 'localhost:8000')
                reset_url = f'https://{main}/reset-password/{uidb64}/{token}/'
                html = render_to_string('emails/password_reset.html', {
                    'reset_url': reset_url,
                    'brand_color': getattr(settings, 'BRAND_PRIMARY', '#3730a3'),
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
        r = _redirect_if_subdomain(request, f'/reset-password/{uidb64}/{token}/')
        if r: return r
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
        return redirect_to(request, _user_home(user))


def _google_callback_url(request):
    scheme = 'https' if not settings.DEBUG else 'http'
    main = getattr(settings, 'MAIN_DOMAIN', 'localhost:8000')
    return f'{scheme}://{main}/auth/google/callback/'


def google_login(request):
    state = secrets.token_urlsafe(16)
    request.session['google_oauth_state'] = state
    params = {
        'client_id':     settings.GOOGLE_CLIENT_ID,
        'redirect_uri':  _google_callback_url(request),
        'response_type': 'code',
        'scope':         'openid email profile',
        'state':         state,
        'access_type':   'online',
    }
    return redirect(GOOGLE_AUTH_URL + '?' + urllib.parse.urlencode(params))


def google_callback(request):
    error = request.GET.get('error')
    if error:
        messages.error(request, 'Google sign-in was cancelled.')
        return redirect('auth_login')

    state_in    = request.GET.get('state', '')
    state_saved = request.session.pop('google_oauth_state', '')
    if not state_saved or state_in != state_saved:
        messages.error(request, 'Invalid state. Please try again.')
        return redirect('auth_login')

    code = request.GET.get('code', '')
    if not code:
        messages.error(request, 'No code returned by Google.')
        return redirect('auth_login')

    token_data = urllib.parse.urlencode({
        'code':          code,
        'client_id':     settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri':  _google_callback_url(request),
        'grant_type':    'authorization_code',
    }).encode()
    try:
        req = urllib.request.Request(GOOGLE_TOKEN_URL, data=token_data, method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_json = json.loads(resp.read())
        access_token = token_json.get('access_token', '')
        info_req = urllib.request.Request(
            GOOGLE_INFO_URL,
            headers={'Authorization': f'Bearer {access_token}'},
        )
        with urllib.request.urlopen(info_req, timeout=10) as resp:
            info = json.loads(resp.read())
    except Exception:
        messages.error(request, 'Could not connect to Google. Please try again.')
        return redirect('auth_login')

    email = info.get('email', '').lower().strip()
    if not email:
        messages.error(request, 'Google did not return an email address.')
        return redirect('auth_login')

    user, created = User.objects.get_or_create(
        email=email,
        defaults={'name': info.get('name', '')},
    )
    if created:
        _send_welcome_email(user)
    login(request, user, backend=backend)
    return redirect(_user_home(user))
