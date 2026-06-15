from django.conf import settings


def brand(request):
    return {
        # 5 brand variables — change them in settings/base.py only
        'brand_dark':    settings.BRAND_DARK,
        'brand_navy':    settings.BRAND_NAVY,
        'brand_blue':    settings.BRAND_BLUE,
        'brand_accent':  settings.BRAND_ACCENT,
        'brand_surface': settings.BRAND_SURFACE,
        # Typography
        'brand_font_url':    settings.BRAND_FONT_URL,
        'brand_font_family': settings.BRAND_FONT_FAMILY,
        # Site identity
        'SITE_NAME': settings.SITE_NAME,
        # Backwards-compat aliases used by base.html / app_base.html
        'brand_primary':   settings.BRAND_ACCENT,
        'brand_secondary': settings.BRAND_SURFACE,
    }
