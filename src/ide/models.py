import json as _json

from django.conf import settings
from django.db import models


class Lab(models.Model):
    CATEGORY_LANGUAGE = 'language'
    CATEGORY_WEB      = 'web'
    CATEGORY_DATABASE = 'database'

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='labs')
    name        = models.CharField(max_length=100)
    language    = models.CharField(max_length=100)
    oc_slug     = models.CharField(max_length=50)
    category    = models.CharField(max_length=20)
    logo_domain = models.CharField(max_length=200, blank=True)
    code        = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def files(self):
        """Return saved code as a files list for OneCompiler populateCode."""
        if not self.code:
            return None
        try:
            data = _json.loads(self.code)
            if isinstance(data, list) and data:
                return data
        except (ValueError, TypeError):
            pass
        return [{'name': 'main', 'content': self.code}]

    def __str__(self):
        return f"{self.name} ({self.language})"
