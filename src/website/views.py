from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    return redirect('authentication:login')


def favicon_svg(request):
    color  = getattr(settings, 'BRAND_PRIMARY', '#3730a3')
    letter = getattr(settings, 'SITE_NAME', 'A')[0].upper()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
        <rect width="32" height="32" rx="6" fill="{color}"/>
        <text x="16" y="22" font-family="Georgia,serif" font-size="18" font-weight="400" fill="white" text-anchor="middle">{letter}</text>
      </svg>'''
    return HttpResponse(svg, content_type='image/svg+xml', headers={'Cache-Control': 'public, max-age=86400'})


def main_robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
