from django.conf import settings
from django.db import models


class SavedJob(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job_id       = models.CharField(max_length=100)
    job_title    = models.CharField(max_length=300)
    company_name = models.CharField(max_length=300, blank=True)
    saved_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job_id')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.job_title} — {self.user}"
