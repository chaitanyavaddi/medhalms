from django.conf import settings
from django.http import HttpResponse
from django.views import View

from utils.view_helper import redirect_to


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect_to(request, 'dashboard:index')
        return redirect_to(request, 'authentication:login')


class FaviconView(View):
    def get(self, request):
        color  = getattr(settings, 'BRAND_PRIMARY', '#3730a3')
        letter = getattr(settings, 'SITE_NAME', 'A')[0].upper()
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
        <rect width="32" height="32" rx="6" fill="{color}"/>
        <text x="16" y="22" font-family="Georgia,serif" font-size="18" font-weight="400" fill="white" text-anchor="middle">{letter}</text>
      </svg>'''
        return HttpResponse(svg, content_type='image/svg+xml', headers={'Cache-Control': 'public, max-age=86400'})


class RobotsTxtView(View):
    def get(self, request):
        lines = ['User-agent: *', 'Allow: /']
        return HttpResponse('\n'.join(lines), content_type='text/plain')
