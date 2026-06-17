from django.contrib import admin

from .models import Lab


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display  = ['name', 'language', 'category', 'user', 'created_at']
    list_filter   = ['category', 'language']
    search_fields = ['name', 'user__email']
    ordering      = ['-created_at']
