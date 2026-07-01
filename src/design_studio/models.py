from django.conf import settings
from django.db import models


class DesignProject(models.Model):
    title        = models.CharField(max_length=200)
    description  = models.TextField(help_text='Full brief shown to the student in the workspace.')
    tags         = models.CharField(max_length=200, blank=True, help_text='Comma-separated e.g. landing-page, ecommerce')
    thumbnail_url = models.URLField(blank=True)
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
        return self.submissions.filter(
            status__in=[DesignSubmission.Status.IN_PROGRESS, DesignSubmission.Status.NEEDS_REVISION]
        ).count()


class DesignSubmission(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS    = 'in_progress',    'In Progress'
        SUBMITTED      = 'submitted',      'Submitted'
        NEEDS_REVISION = 'needs_revision', 'Needs Revision'
        APPROVED       = 'approved',       'Approved'

    project       = models.ForeignKey(DesignProject, on_delete=models.CASCADE, related_name='submissions')
    student       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='design_submissions')
    grapes_data   = models.JSONField(default=dict)
    html_snapshot = models.TextField(blank=True)
    status        = models.CharField(max_length=16, choices=Status.choices, default=Status.IN_PROGRESS)
    started_at    = models.DateTimeField(auto_now_add=True)
    submitted_at  = models.DateTimeField(null=True, blank=True)
    last_saved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('project', 'student')
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.student} — {self.project}'


class DesignFeedback(models.Model):
    class Action(models.TextChoices):
        APPROVED  = 'approved',  'Approved'
        SENT_BACK = 'sent_back', 'Sent Back'

    submission = models.ForeignKey(DesignSubmission, on_delete=models.CASCADE, related_name='feedback_entries')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='design_feedback_given')
    action     = models.CharField(max_length=10, choices=Action.choices)
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.action} by {self.author} on {self.submission}'
