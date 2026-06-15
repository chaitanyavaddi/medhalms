from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found, permission_denied

handler404 = lambda request, exception: page_not_found(request, exception, template_name='404.html')
handler403 = lambda request, exception: permission_denied(request, exception, template_name='403.html')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.svg", __import__('website.views', fromlist=['favicon_svg']).favicon_svg, name="favicon_svg"),
    path("", include("website.urls")),
    path("", include("authentication.urls")),
    path("orgs/", include("orgs.urls")),
]
