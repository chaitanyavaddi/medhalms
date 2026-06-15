from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "first_name", "last_name", "role", "status", "created_at"]
    ordering     = ["-created_at"]
    fieldsets    = (
        (None, {"fields": ("email", "password")}),
        ("Personal", {"fields": ("first_name", "last_name", "gender", "avatar", "phone_prefix", "phone", "role", "status")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
    )
    search_fields = ["email", "first_name", "last_name"]
    filter_horizontal = ("groups", "user_permissions")
