from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from orgs.models import Organization, OrgMember
from utils.view_helper import htmx, redirect_to


def _org_dashboard_url(org):
    scheme = 'http' if settings.DEBUG else 'https'
    main = getattr(settings, 'MAIN_DOMAIN', 'localhost:8000')
    return f'{scheme}://{org.subdomain}.{main}/dashboard/'


class OrgListView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        memberships = list(OrgMember.objects.filter(user=request.user).select_related("org"))
        if len(memberships) == 1:
            return redirect(_org_dashboard_url(memberships[0].org))
        return render(request, "orgs/org_list.html", {"memberships": memberships})


class OrgCreateView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        return render(request, "orgs/org_create.html")

    def post(self, request):
        hx        = htmx(request)
        ctx       = {"data": request.POST}
        name      = request.POST.get("name", "").strip()
        subdomain = request.POST.get("subdomain", "").lower().strip()
        template  = "orgs/org_create.html#create-org-form" if hx else "orgs/org_create.html"

        if not name or not subdomain:
            messages.error(request, "Organization name and subdomain are required")
            return render(request, template, ctx)
        if subdomain in settings.RESERVED_SUBDOMAINS:
            messages.error(request, "That subdomain is reserved")
            return render(request, template, ctx)
        if Organization.objects.filter(subdomain=subdomain).exists():
            messages.error(request, "Subdomain already taken")
            return render(request, template, ctx)

        default_primary = getattr(settings, 'BRAND_PRIMARY', '#3730a3')
        org = Organization.objects.create(name=name, subdomain=subdomain, brand_primary=default_primary)
        OrgMember.objects.create(org=org, user=request.user, role=OrgMember.Role.OWNER)
        return redirect_to(request, _org_dashboard_url(org))
