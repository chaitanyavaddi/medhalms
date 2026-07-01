import os
import uuid
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from utils.view_helper import redirect_to

from .models import DesignProject, DesignSubmission


def _can_manage(user):
    return user.is_superuser or user.role == 'trainer'


def _parse_tags(tags_str):
    """Return a list of stripped, non-empty tag strings."""
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(',') if t.strip()]


class DesignProjectListView(LoginRequiredMixin, View):
    def get(self, request):
        projects = DesignProject.objects.filter(is_active=True)
        if _can_manage(request.user):
            project_list = [(p, None, _parse_tags(p.tags)) for p in projects]
        else:
            sub_map = {s.project_id: s for s in DesignSubmission.objects.filter(student=request.user)}
            project_list = [(p, sub_map.get(p.pk), _parse_tags(p.tags)) for p in projects]
        return render(request, 'design_studio/list.html', {
            'project_list': project_list,
            'can_manage': _can_manage(request.user),
        })


class DesignProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        return render(request, 'design_studio/form.html', {'project': None})

    def post(self, request):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        tags = request.POST.get('tags', '').strip()
        if not title or not description:
            messages.error(request, 'Title and description are required.')
            return render(request, 'design_studio/form.html', {
                'project': None,
                'fdata': {'title': title, 'description': description, 'tags': tags},
            })
        DesignProject.objects.create(
            title=title, description=description, tags=tags,
            created_by=request.user,
        )
        return redirect_to(request, 'design_studio:list')


class DesignProjectUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        project = get_object_or_404(DesignProject, pk=pk)
        return render(request, 'design_studio/form.html', {'project': project})

    def post(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        project = get_object_or_404(DesignProject, pk=pk)
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        tags = request.POST.get('tags', '').strip()
        if not title or not description:
            messages.error(request, 'Title and description are required.')
            return render(request, 'design_studio/form.html', {'project': project})
        project.title = title
        project.description = description
        project.tags = tags
        project.is_active = request.POST.get('is_active') == '1'
        project.save(update_fields=['title', 'description', 'tags', 'is_active', 'updated_at'])
        return redirect_to(request, 'design_studio:list')


class DesignProjectDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        project = get_object_or_404(DesignProject, pk=pk)
        project.delete()
        return redirect_to(request, 'design_studio:list')


class DesignWorkspaceView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(DesignProject, pk=pk, is_active=True)
        submission, _ = DesignSubmission.objects.get_or_create(
            project=project, student=request.user
        )
        return render(request, 'design_studio/workspace.html', {
            'project': project,
            'submission': submission,
            'grapes_json': json.dumps(submission.grapes_data) if submission.grapes_data else '{}',
            'project_tags': _parse_tags(project.tags),
        })


class DesignAutosaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(DesignProject, pk=pk, is_active=True)
        submission = get_object_or_404(DesignSubmission, project=project, student=request.user)
        if submission.status == DesignSubmission.Status.SUBMITTED:
            return HttpResponse(status=403)
        try:
            body = json.loads(request.body)
            submission.grapes_data = body.get('data', {})
            submission.html_snapshot = body.get('html', '')
            submission.last_saved_at = timezone.now()
            submission.save(update_fields=['grapes_data', 'html_snapshot', 'last_saved_at'])
            return HttpResponse('ok')
        except (json.JSONDecodeError, KeyError):
            return HttpResponse(status=400)


class DesignSubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(DesignProject, pk=pk, is_active=True)
        submission = get_object_or_404(DesignSubmission, project=project, student=request.user)
        if submission.status == DesignSubmission.Status.SUBMITTED:
            return HttpResponse(status=400)
        try:
            body = json.loads(request.body)
            submission.grapes_data = body.get('data', submission.grapes_data)
            submission.html_snapshot = body.get('html', submission.html_snapshot)
        except (json.JSONDecodeError, KeyError):
            pass
        submission.status = DesignSubmission.Status.SUBMITTED
        submission.submitted_at = timezone.now()
        submission.last_saved_at = timezone.now()
        submission.save(update_fields=['grapes_data', 'html_snapshot', 'status', 'submitted_at', 'last_saved_at'])
        resp = HttpResponse()
        resp['HX-Redirect'] = reverse('design_studio:list')
        return resp


class DesignAssetUploadView(LoginRequiredMixin, View):
    ALLOWED_TYPES = {
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml',
        'video/mp4', 'video/webm',
    }

    def post(self, request):
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({'data': []})
        result = []
        for f in files:
            if f.content_type not in self.ALLOWED_TYPES:
                continue
            ext = os.path.splitext(f.name)[1].lower() or '.bin'
            filename = f'design_assets/{uuid.uuid4().hex}{ext}'
            path = default_storage.save(filename, ContentFile(f.read()))
            url = default_storage.url(path)
            asset_type = 'video' if f.content_type.startswith('video') else 'image'
            result.append({'src': url, 'type': asset_type, 'name': f.name})
        return JsonResponse({'data': result})


class DesignSubmissionListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        project = get_object_or_404(DesignProject, pk=pk)
        submissions = project.submissions.select_related('student').order_by('-submitted_at', '-last_saved_at')
        return render(request, 'design_studio/submissions.html', {
            'project': project,
            'submissions': submissions,
        })
