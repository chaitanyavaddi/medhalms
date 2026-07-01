from django.shortcuts import redirect

_PENDING_APPROVAL_PATH = '/dashboard/pending-approval/'
_PENDING_EXEMPT_PATHS = frozenset([
    '/login/',
    '/signup/',
    '/logout/',
    '/forgot-password/',
    _PENDING_APPROVAL_PATH,
])


class PendingStudentMiddleware:
    """
    Redirect students with pending status away from all app pages
    until an admin approves them.
    Must be placed after AuthenticationMiddleware in settings.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if (
            user.is_authenticated
            and getattr(user, 'role', None) == 'student'
            and getattr(user, 'status', None) == 'pending'
            and request.path not in _PENDING_EXEMPT_PATHS
            and not request.path.startswith('/static/')
            and not request.path.startswith('/reset-password/')
        ):
            return redirect(_PENDING_APPROVAL_PATH)
        return self.get_response(request)


class CacheableResponseMiddleware:
    """Strip Set-Cookie and Vary: Cookie from publicly cacheable responses."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 's-maxage' in response.get('Cache-Control', ''):
            if 'csrftoken' in response.cookies:
                del response.cookies['csrftoken']
            vary    = response.get('Vary', '')
            stripped = ', '.join(v.strip() for v in vary.split(',') if v.strip().lower() != 'cookie')
            if stripped:
                response['Vary'] = stripped
            elif vary:
                del response['Vary']
        return response
