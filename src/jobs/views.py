from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .service import JobspyClient, SavedJobService

EMPTY_JOBS = {'total': 0, 'page': 1, 'page_size': 12, 'items': []}
EMPTY_META = {'roles': [], 'locations': [], 'experience_bands': [], 'sites': []}


def _enrich(jobs, saved_ids):
    for job in jobs:
        job['is_saved'] = job['id'] in saved_ids
        if job.get('key_skills'):
            job['skills_list'] = [s.strip() for s in job['key_skills'].split(',') if s.strip()]
        else:
            job['skills_list'] = []
    return jobs


class JobBoardView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            meta = JobspyClient.get_meta()
        except Exception:
            meta = EMPTY_META
        return render(request, 'jobs/board.html', meta)


class JobListPartialView(LoginRequiredMixin, View):
    def get(self, request):
        params = {}
        for key in ('keyword', 'company', 'role', 'location', 'experience', 'site', 'page'):
            val = request.GET.get(key, '').strip()
            if val:
                params[key] = val
        if request.GET.get('is_remote'):
            params['is_remote'] = 'true'
        try:
            data = JobspyClient.get_jobs(params)
        except Exception:
            data = dict(EMPTY_JOBS)
        saved_ids = SavedJobService.get_saved_ids(request.user)
        _enrich(data['items'], saved_ids)
        ctx = {
            'jobs':      data['items'],
            'total':     data['total'],
            'page':      data['page'],
            'page_size': data['page_size'],
            'has_prev':  data['page'] > 1,
            'has_next':  (data['page'] * data['page_size']) < data['total'],
            'prev_page': data['page'] - 1,
            'next_page': data['page'] + 1,
            'filters':   request.GET,
        }
        resp = render(request, 'jobs/partials/job_cards.html', ctx)
        resp['Cache-Control'] = 'no-store'
        return resp


class JobDetailView(LoginRequiredMixin, View):
    def get(self, request, job_id):
        try:
            job = JobspyClient.get_job(job_id)
        except Exception:
            job = {}
        if job.get('key_skills'):
            job['skills_list'] = [s.strip() for s in job['key_skills'].split(',') if s.strip()]
        else:
            job['skills_list'] = []
        job['is_saved'] = SavedJobService.is_saved(request.user, job_id)
        return render(request, 'jobs/partials/job_detail_modal.html', {'job': job})


class JobSaveToggleView(LoginRequiredMixin, View):
    def post(self, request, job_id):
        title   = request.POST.get('title', '')
        company = request.POST.get('company', '')
        is_saved = SavedJobService.toggle(request.user, job_id, title, company)
        return render(request, 'jobs/partials/save_btn.html', {
            'job_id':   job_id,
            'is_saved': is_saved,
            'title':    title,
            'company':  company,
        })
