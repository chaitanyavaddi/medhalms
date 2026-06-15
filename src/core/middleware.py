from django.conf import settings
from orgs.models import Organization


class CacheableResponseMiddleware:
    """Strip Set-Cookie and Vary: Cookie from publicly cacheable responses."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 's-maxage' in response.get('Cache-Control', ''):
            if 'csrftoken' in response.cookies:
                del response.cookies['csrftoken']
            vary = response.get('Vary', '')
            stripped = ', '.join(v.strip() for v in vary.split(',') if v.strip().lower() != 'cookie')
            if stripped:
                response['Vary'] = stripped
            elif vary:
                del response['Vary']
        return response


class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        main_domain = getattr(settings, 'MAIN_DOMAIN', 'localhost').split(':')[0].lower()
        request.org    = None
        request.domain = getattr(settings, 'MAIN_DOMAIN', 'localhost:8000')

        if host.endswith(f'.{main_domain}'):
            subdomain = host[: -(len(main_domain) + 1)]
            if subdomain and subdomain not in settings.RESERVED_SUBDOMAINS:
                try:
                    request.org     = Organization.objects.get(subdomain=subdomain, is_active=True)
                    request.urlconf = 'config.urls_org'
                except Organization.DoesNotExist:
                    from django.http import HttpResponseRedirect
                    main = getattr(settings, 'MAIN_DOMAIN', 'myapp.com')
                    return HttpResponseRedirect(f'https://{main}/')

        return self.get_response(request)
