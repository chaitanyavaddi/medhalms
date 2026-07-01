import os
import uuid
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from utils.view_helper import redirect_to

from .models import DesignProject, DesignSubmission, DesignFeedback


def _can_manage(user):
    return user.is_superuser or user.role == 'trainer'


def _parse_tags(tags_str):
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(',') if t.strip()]


_LOCKED_STATUSES = (DesignSubmission.Status.SUBMITTED, DesignSubmission.Status.APPROVED)


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
        return render(request, 'design_studio/form.html', {
            'project': None,
            'fdata': {'title': '', 'description': '', 'tags': ''},
        })

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
        return render(request, 'design_studio/form.html', {
            'project': project,
            'fdata': {'title': project.title, 'description': project.description, 'tags': project.tags},
        })

    def post(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        project = get_object_or_404(DesignProject, pk=pk)
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        tags = request.POST.get('tags', '').strip()
        if not title or not description:
            messages.error(request, 'Title and description are required.')
            return render(request, 'design_studio/form.html', {
                'project': project,
                'fdata': {'title': title, 'description': description, 'tags': tags},
            })
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
        if submission.status == DesignSubmission.Status.APPROVED:
            return redirect_to(request, reverse('design_studio:submission_detail', kwargs={'pk': pk, 'sub_pk': submission.pk}))
        feedback_entries = submission.feedback_entries.select_related('author').all()
        return render(request, 'design_studio/workspace.html', {
            'project': project,
            'submission': submission,
            'grapes_json': json.dumps(submission.grapes_data) if submission.grapes_data else '{}',
            'project_tags': _parse_tags(project.tags),
            'feedback_entries': feedback_entries,
        })


class DesignAutosaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(DesignProject, pk=pk, is_active=True)
        submission = get_object_or_404(DesignSubmission, project=project, student=request.user)
        if submission.status in _LOCKED_STATUSES:
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
        if submission.status in _LOCKED_STATUSES:
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


class DesignSubmissionDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, sub_pk):
        project = get_object_or_404(DesignProject, pk=pk)
        submission = get_object_or_404(DesignSubmission, pk=sub_pk, project=project)
        if not _can_manage(request.user) and submission.student != request.user:
            return HttpResponseForbidden()
        preview_url = reverse('design_studio:submission_preview', kwargs={'pk': pk, 'sub_pk': sub_pk})
        feedback_entries = submission.feedback_entries.select_related('author').all()
        return render(request, 'design_studio/submission_detail.html', {
            'project': project,
            'submission': submission,
            'preview_url': preview_url,
            'can_manage': _can_manage(request.user),
            'feedback_entries': feedback_entries,
            'project_tags': _parse_tags(project.tags),
        })


@method_decorator(xframe_options_exempt, name='dispatch')
class DesignSubmissionPreviewView(LoginRequiredMixin, View):
    def get(self, request, pk, sub_pk):
        project = get_object_or_404(DesignProject, pk=pk)
        submission = get_object_or_404(DesignSubmission, pk=sub_pk, project=project)
        if not _can_manage(request.user) and submission.student != request.user:
            return HttpResponseForbidden()
        html = submission.html_snapshot or ''
        page = (
            '<!DOCTYPE html><html><head>'
            '<meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + project.title + '</title>'
            '<style>*{box-sizing:border-box}body{margin:0;padding:0;font-family:sans-serif}</style>'
            '</head><body>' + html + '</body></html>'
        )
        return HttpResponse(page, content_type='text/html')


class DesignSubmissionApproveView(LoginRequiredMixin, View):
    def post(self, request, pk, sub_pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        submission = get_object_or_404(DesignSubmission, pk=sub_pk, project_id=pk)
        comment = request.POST.get('comment', '').strip()
        submission.status = DesignSubmission.Status.APPROVED
        submission.save(update_fields=['status'])
        DesignFeedback.objects.create(
            submission=submission,
            author=request.user,
            action=DesignFeedback.Action.APPROVED,
            comment=comment,
        )
        return redirect_to(request, reverse('design_studio:submissions', kwargs={'pk': pk}))


class DesignSubmissionSendBackView(LoginRequiredMixin, View):
    def post(self, request, pk, sub_pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        submission = get_object_or_404(DesignSubmission, pk=sub_pk, project_id=pk)
        comment = request.POST.get('comment', '').strip()
        if not comment:
            messages.error(request, 'A comment is required when sending back for revision.')
            return redirect_to(request, reverse('design_studio:submission_detail', kwargs={'pk': pk, 'sub_pk': sub_pk}))
        submission.status = DesignSubmission.Status.NEEDS_REVISION
        submission.submitted_at = None
        submission.save(update_fields=['status', 'submitted_at'])
        DesignFeedback.objects.create(
            submission=submission,
            author=request.user,
            action=DesignFeedback.Action.SENT_BACK,
            comment=comment,
        )
        return redirect_to(request, reverse('design_studio:submissions', kwargs={'pk': pk}))


class DesignSubmissionDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, sub_pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        submission = get_object_or_404(DesignSubmission, pk=sub_pk, project_id=pk)
        submission.delete()
        return redirect_to(request, reverse('design_studio:submissions', kwargs={'pk': pk}))


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
