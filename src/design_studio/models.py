from django.conf import settings
from django.db import models


class DesignProject(models.Model):
    title        = models.CharField(max_length=200)
    description  = models.TextField(help_text='Full brief shown to the student in the workspace.')
    tags         = models.CharField(max_length=200, blank=True, help_text='Comma-separated e.g. landing-page, ecommerce')
    is_active    = models.BooleanField(default=True)
    created_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='design_projects_created')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def submission_count(self):
        return self.submissions.count()

    @property
    def active_count(self):
        return self.submissions.filter(status=DesignSubmission.Status.IN_PROGRESS).count()


class DesignSubmission(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        SUBMITTED   = 'submitted',   'Submitted'

    project      = models.ForeignKey(DesignProject, on_delete=models.CASCADE, related_name='submissions')
    student      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='design_submissions')
    grapes_data  = models.JSONField(default=dict)
    html_snapshot = models.TextField(blank=True)
    status       = models.CharField(max_length=15, choices=Status.choices, default=Status.IN_PROGRESS)
    started_at   = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    last_saved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('project', 'student')
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.student} — {self.project}'
