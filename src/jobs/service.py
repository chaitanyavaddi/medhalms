import json
import urllib.request
from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import cache

from .models import SavedJob


class JobspyClient:

    @staticmethod
    def _get(path, params=None):
        url = f"{settings.JOBSPY_API_URL}{path}"
        if params:
            url = f"{url}?{urlencode(params)}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    @staticmethod
    def get_meta():
        cached = cache.get('jobs_meta')
        if cached:
            return cached
        roles     = JobspyClient._get('/api/v1/meta/roles')
        locations = JobspyClient._get('/api/v1/meta/locations')
        exp_bands = JobspyClient._get('/api/v1/meta/experience-bands')
        sites     = JobspyClient._get('/api/v1/meta/sites')
        meta = {
            'roles': roles,
            'locations': locations,
            'experience_bands': exp_bands,
            'sites': sites,
        }
        cache.set('jobs_meta', meta, 3600)
        return meta

    @staticmethod
    def get_jobs(params):
        clean = {k: v for k, v in params.items() if v}
        clean['bucket'] = 'tagged'
        clean.setdefault('page_size', 12)
        return JobspyClient._get('/api/v1/jobs', clean)

    @staticmethod
    def get_job(job_id):
        return JobspyClient._get(f'/api/v1/jobs/{job_id}')


class SavedJobService:

    @staticmethod
    def get_saved_ids(user):
        return set(SavedJob.objects.filter(user=user).values_list('job_id', flat=True))

    @staticmethod
    def is_saved(user, job_id):
        return SavedJob.objects.filter(user=user, job_id=job_id).exists()

    @staticmethod
    def toggle(user, job_id, title, company):
        existing = SavedJob.objects.filter(user=user, job_id=job_id).first()
        if existing:
            existing.delete()
            return False
        SavedJob.objects.create(user=user, job_id=job_id, job_title=title, company_name=company)
        return True
