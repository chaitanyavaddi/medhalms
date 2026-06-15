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
