from django.contrib import admin
from .models import DesignProject, DesignSubmission

@admin.register(DesignProject)
class DesignProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_by', 'submission_count', 'created_at')
    list_filter = ('is_active',)

@admin.register(DesignSubmission)
class DesignSubmissionAdmin(admin.ModelAdmin):
    list_display = ('project', 'student', 'status', 'last_saved_at', 'submitted_at')
    list_filter = ('status',)
    raw_id_fields = ('project', 'student')
