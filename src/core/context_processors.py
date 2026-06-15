from django.conf import settings


def brand(request):
    org = getattr(request, 'org', None)
    if org:
        primary   = org.brand_primary   or getattr(settings, 'BRAND_PRIMARY',   '#3730a3')
        secondary = org.brand_secondary or getattr(settings, 'BRAND_SECONDARY', '#2a6e96')
    else:
        primary   = getattr(settings, 'BRAND_PRIMARY',   '#3730a3')
        secondary = getattr(settings, 'BRAND_SECONDARY', '#2a6e96')
    return {
        'brand_primary':   primary,
        'brand_secondary': secondary,
        'brand_font_url':    getattr(settings, 'BRAND_FONT_URL',    ''),
        'brand_font_family': getattr(settings, 'BRAND_FONT_FAMILY', "'Inter', system-ui, sans-serif"),
    }
