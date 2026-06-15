from django.contrib import admin
from .models import Organization, OrgMember


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "subdomain", "is_active", "created_at"]
    search_fields = ["name", "subdomain"]


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ["user", "org", "role", "created_at"]
