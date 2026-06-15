from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def favicon_svg(request):
    default_color = getattr(settings, 'BRAND_PRIMARY', '#3730a3')
    org = getattr(request, 'org', None)
    if org:
        letter = (org.name or 'A')[0].upper()
        color = org.brand_primary or default_color
    else:
        letter = 'A'
        color = default_color
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
            <rect width="32" height="32" rx="6" fill="{color}"/>
            <text x="16" y="22" font-family="Georgia,serif" font-size="18" font-weight="400" fill="white" text-anchor="middle">{letter}</text>
          </svg>'''
    return HttpResponse(svg, content_type='image/svg+xml', headers={'Cache-Control': 'public, max-age=86400'})


def home(request):
    return render(request, "website/home.html")


def main_robots_txt(request):
    main_domain = getattr(settings, 'MAIN_DOMAIN', 'myapp.com')
    lines = [
        'User-agent: *',
        'Allow: /',
        '',
        'User-agent: GPTBot',
        'Allow: /',
        '',
        'User-agent: ClaudeBot',
        'Allow: /',
        '',
        'User-agent: PerplexityBot',
        'Allow: /',
        '',
        'User-agent: OAI-SearchBot',
        'Allow: /',
        '',
        f'Sitemap: https://{main_domain}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
