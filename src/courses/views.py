import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from users.models import User
from .models import Chapter, Course, Module


def _can_manage(user, course):
    return user.is_superuser or course.trainers.filter(pk=user.pk).exists()


def _renumber_modules(course):
    for i, m in enumerate(Module.objects.filter(course=course).order_by('order', 'created_at')):
        if m.order != i:
            Module.objects.filter(pk=m.pk).update(order=i)


def _renumber_chapters(module):
    for i, c in enumerate(Chapter.objects.filter(module=module).order_by('order', 'created_at')):
        if c.order != i:
            Chapter.objects.filter(pk=c.pk).update(order=i)


# ── Course list / create ─────────────────────────────────────────────────────

class CourseListView(LoginRequiredMixin, View):
    def get(self, request):
        courses = Course.objects.prefetch_related('trainers').all()
        return render(request, 'courses/list.html', {'courses': courses})


class CourseCreateView(LoginRequiredMixin, View):
    def _trainers(self):
        return User.objects.filter(role='trainer').order_by('first_name', 'last_name')

    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return render(request, 'courses/partials/course_form_modal.html', {
            'course': None, 'trainers': self._trainers(),
        })

    def post(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        name = request.POST.get('name', '').strip()
        if not name:
            return render(request, 'courses/partials/course_form_modal.html', {
                'course': None, 'trainers': self._trainers(),
                'error': 'Course name is required.',
            })
        course = Course.objects.create(
            name=name,
            description=request.POST.get('description', '').strip(),
            status=request.POST.get('status', Course.Status.DRAFT),
            created_by=request.user,
        )
        trainer_ids = request.POST.getlist('trainers')
        if trainer_ids:
            course.trainers.set(trainer_ids)
        resp = HttpResponse()
        resp['HX-Redirect'] = f'/courses/{course.pk}/'
        return resp


class CourseUpdateView(LoginRequiredMixin, View):
    def _trainers(self):
        return User.objects.filter(role='trainer').order_by('first_name', 'last_name')

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return render(request, 'courses/partials/course_form_modal.html', {
            'course': course, 'trainers': self._trainers(),
        })

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        name = request.POST.get('name', '').strip()
        if not name:
            return render(request, 'courses/partials/course_form_modal.html', {
                'course': course, 'trainers': self._trainers(),
                'error': 'Course name is required.',
            })
        course.name        = name
        course.description = request.POST.get('description', '').strip()
        course.status      = request.POST.get('status', Course.Status.DRAFT)
        course.save(update_fields=['name', 'description', 'status', 'updated_at'])
        trainer_ids = request.POST.getlist('trainers')
        course.trainers.set(trainer_ids)
        resp = HttpResponse()
        resp['HX-Trigger'] = 'closeModal'
        return resp


# ── Course detail / chapter editor ──────────────────────────────────────────

class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        first  = course.first_chapter
        if first:
            return redirect('courses:chapter', pk=course.pk, chapter_pk=first.pk)
        return render(request, 'courses/detail.html', {
            'course':         course,
            'active_chapter': None,
            'can_manage':     _can_manage(request.user, course),
        })


class ChapterDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, chapter_pk):
        course  = get_object_or_404(Course, pk=pk)
        chapter = get_object_or_404(Chapter, pk=chapter_pk, module__course=course)
        return render(request, 'courses/detail.html', {
            'course':         course,
            'active_chapter': chapter,
            'can_manage':     _can_manage(request.user, course),
        })


class ChapterSaveView(LoginRequiredMixin, View):
    def post(self, request, pk, chapter_pk):
        course  = get_object_or_404(Course, pk=pk)
        if not _can_manage(request.user, course):
            return JsonResponse({'error': 'Permission denied'}, status=403)
        chapter = get_object_or_404(Chapter, pk=chapter_pk, module__course=course)
        title = request.POST.get('title', '').strip()
        body  = request.POST.get('body', '')
        if title:
            chapter.title = title
        chapter.content = body
        chapter.save(update_fields=['title', 'content', 'updated_at'])
        return JsonResponse({'ok': True})


# ── Upload ───────────────────────────────────────────────────────────────────

class CourseUploadView(LoginRequiredMixin, View):
    _allowed = {
        'image/jpeg', 'image/png', 'image/gif', 'image/webp',
        'video/mp4', 'video/webm', 'video/quicktime',
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword',
    }

    def post(self, request):
        f = request.FILES.get('file')
        if not f:
            return JsonResponse({'error': 'No file provided'}, status=400)
        if f.content_type not in self._allowed:
            return JsonResponse({'error': 'File type not supported'}, status=400)
        try:
            from core.bunny import upload_file
            course_id = request.POST.get('course_id', 'general')
            folder = f'courses/{course_id}'
            url = upload_file(f, folder)
        except RuntimeError as e:
            return JsonResponse({'error': str(e)}, status=500)
        ct = f.content_type
        if ct.startswith('image/'):
            file_type = 'image'
        elif ct.startswith('video/'):
            file_type = 'video'
        else:
            file_type = 'file'
        return JsonResponse({'url': url, 'type': file_type, 'filename': f.name, 'mimetype': ct})


class CourseFileDeleteView(LoginRequiredMixin, View):
    """Delete a previously uploaded course file from Bunny CDN."""
    login_url = '/login/'

    def post(self, request):
        from django.conf import settings
        from core.bunny import delete_file
        url = request.POST.get('url', '').strip()
        if not url:
            return JsonResponse({'error': 'No URL provided'}, status=400)
        cdn_base = getattr(settings, 'BUNNY_CDN_BASE', '').rstrip('/')
        if cdn_base and url.startswith(cdn_base + '/'):
            object_path = url[len(cdn_base) + 1:]
            delete_file(object_path)
        return JsonResponse({'ok': True})


# ── Modules ──────────────────────────────────────────────────────────────────

class ModuleCreateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        return render(request, 'courses/partials/module_form_modal.html', {
            'course': course, 'module_obj': None,
        })

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        title = request.POST.get('title', '').strip()
        if not title:
            return render(request, 'courses/partials/module_form_modal.html', {
                'course': course, 'module_obj': None, 'error': 'Title is required.',
            })
        order = Module.objects.filter(course=course).count()
        Module.objects.create(course=course, title=title, order=order)
        resp = HttpResponse()
        resp['HX-Trigger'] = 'closeModal'
        return resp


class ModuleUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, module_pk):
        course     = get_object_or_404(Course, pk=pk)
        module_obj = get_object_or_404(Module, pk=module_pk, course=course)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        return render(request, 'courses/partials/module_form_modal.html', {
            'course': course, 'module_obj': module_obj,
        })

    def post(self, request, pk, module_pk):
        course     = get_object_or_404(Course, pk=pk)
        module_obj = get_object_or_404(Module, pk=module_pk, course=course)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        title = request.POST.get('title', '').strip()
        if not title:
            return render(request, 'courses/partials/module_form_modal.html', {
                'course': course, 'module_obj': module_obj, 'error': 'Title is required.',
            })
        module_obj.title = title
        module_obj.save(update_fields=['title'])
        resp = HttpResponse()
        resp['HX-Trigger'] = 'closeModal'
        return resp


class ModuleDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, module_pk):
        course     = get_object_or_404(Course, pk=pk)
        module_obj = get_object_or_404(Module, pk=module_pk, course=course)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        return render(request, 'courses/partials/delete_modal.html', {
            'title':      'Delete Module',
            'message':    f'Delete "{module_obj.title}" and all its chapters? This cannot be undone.',
            'delete_url': request.path,
        })

    def post(self, request, pk, module_pk):
        course     = get_object_or_404(Course, pk=pk)
        module_obj = get_object_or_404(Module, pk=module_pk, course=course)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        module_obj.delete()
        _renumber_modules(course)
        resp = HttpResponse()
        resp['HX-Trigger'] = 'closeModal'
        return resp


# ── Chapters ─────────────────────────────────────────────────────────────────

class ChapterCreateView(LoginRequiredMixin, View):
    def get(self, request, pk, module_pk):
        course     = get_object_or_404(Course, pk=pk)
        module_obj = get_object_or_404(Module, pk=module_pk, course=course)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        return render(request, 'courses/partials/chapter_form_modal.html', {
            'course': course, 'module_obj': module_obj, 'chapter_obj': None,
        })

    def post(self, request, pk, module_pk):
        course     = get_object_or_404(Course, pk=pk)
        module_obj = get_object_or_404(Module, pk=module_pk, course=course)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        title = request.POST.get('title', '').strip()
        if not title:
            return render(request, 'courses/partials/chapter_form_modal.html', {
                'course': course, 'module_obj': module_obj, 'chapter_obj': None,
                'error': 'Title is required.',
            })
        order   = Chapter.objects.filter(module=module_obj).count()
        chapter = Chapter.objects.create(module=module_obj, title=title, order=order)
        resp    = HttpResponse()
        resp['HX-Redirect'] = f'/courses/{pk}/c/{chapter.pk}/'
        return resp


class ChapterUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, module_pk, chapter_pk):
        course      = get_object_or_404(Course, pk=pk)
        module_obj  = get_object_or_404(Module, pk=module_pk, course=course)
        chapter_obj = get_object_or_404(Chapter, pk=chapter_pk, module=module_obj)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        return render(request, 'courses/partials/chapter_form_modal.html', {
            'course': course, 'module_obj': module_obj, 'chapter_obj': chapter_obj,
        })

    def post(self, request, pk, module_pk, chapter_pk):
        course      = get_object_or_404(Course, pk=pk)
        module_obj  = get_object_or_404(Module, pk=module_pk, course=course)
        chapter_obj = get_object_or_404(Chapter, pk=chapter_pk, module=module_obj)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        title = request.POST.get('title', '').strip()
        if not title:
            return render(request, 'courses/partials/chapter_form_modal.html', {
                'course': course, 'module_obj': module_obj, 'chapter_obj': chapter_obj,
                'error': 'Title is required.',
            })
        chapter_obj.title = title
        chapter_obj.save(update_fields=['title'])
        resp = HttpResponse()
        resp['HX-Trigger'] = 'closeModal'
        return resp


class ChapterDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, module_pk, chapter_pk):
        course      = get_object_or_404(Course, pk=pk)
        module_obj  = get_object_or_404(Module, pk=module_pk, course=course)
        chapter_obj = get_object_or_404(Chapter, pk=chapter_pk, module=module_obj)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        return render(request, 'courses/partials/delete_modal.html', {
            'title':      'Delete Chapter',
            'message':    f'Delete "{chapter_obj.title}"? This cannot be undone.',
            'delete_url': request.path,
        })

    def post(self, request, pk, module_pk, chapter_pk):
        course      = get_object_or_404(Course, pk=pk)
        module_obj  = get_object_or_404(Module, pk=module_pk, course=course)
        chapter_obj = get_object_or_404(Chapter, pk=chapter_pk, module=module_obj)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        chapter_obj.delete()
        _renumber_chapters(module_obj)
        resp = HttpResponse()
        resp['HX-Redirect'] = f'/courses/{pk}/'
        return resp


# ── Reorder ───────────────────────────────────────────────────────────────────

class ModuleReorderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        order = json.loads(request.body).get('order', [])
        for i, module_id in enumerate(order):
            Module.objects.filter(pk=module_id, course=course).update(order=i)
        return JsonResponse({'ok': True})


class ChapterReorderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if not _can_manage(request.user, course):
            return HttpResponseForbidden()
        data           = json.loads(request.body)
        chapter_id     = data.get('chapter_id')
        to_module_id   = data.get('to_module_id')
        from_module_id = data.get('from_module_id')
        to_chapters    = data.get('chapters', [])
        from_chapters  = data.get('from_chapters', [])

        to_module = get_object_or_404(Module, pk=to_module_id, course=course)
        chapter   = get_object_or_404(Chapter, pk=chapter_id)

        if chapter.module_id != to_module.pk:
            chapter.module = to_module
            chapter.save(update_fields=['module'])

        for i, cid in enumerate(to_chapters):
            Chapter.objects.filter(pk=cid, module=to_module).update(order=i)

        if from_module_id and str(from_module_id) != str(to_module_id):
            from_module = get_object_or_404(Module, pk=from_module_id, course=course)
            for i, cid in enumerate(from_chapters):
                Chapter.objects.filter(pk=cid, module=from_module).update(order=i)

        return JsonResponse({'ok': True})
