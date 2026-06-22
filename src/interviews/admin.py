from django.contrib import admin
from .models import Interview, Question, InterviewSession, InterviewAnswer


class QuestionInline(admin.TabularInline):
    model   = Question
    extra   = 3
    fields  = ['order', 'text']
    ordering = ['order']


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display  = ['title', 'difficulty', 'max_duration', 'question_count', 'created_by', 'created_at']
    list_filter   = ['difficulty']
    search_fields = ['title']
    filter_horizontal = ['courses']
    inlines       = [QuestionInline]
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class InterviewAnswerInline(admin.TabularInline):
    model     = InterviewAnswer
    extra     = 0
    readonly_fields = ['question', 'transcript', 'duration_seconds', 'answered_at']
    can_delete = False


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display  = ['user', 'interview', 'status', 'started_at', 'ended_at']
    list_filter   = ['status']
    readonly_fields = ['started_at', 'ended_at', 'feedback']
    inlines       = [InterviewAnswerInline]
