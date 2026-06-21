from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from users.models import User
from .models import Chapter, Course, Module


def _can_manage(user, course):
    return user.is_superuser or course.trainers.filter(pk=user.pk).exists()


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
    }

    def post(self, request):
        f = request.FILES.get('file')
        if not f:
            return JsonResponse({'error': 'No file provided'}, status=400)
        if f.content_type not in self._allowed:
            return JsonResponse({'error': 'File type not supported'}, status=400)
        is_video = f.content_type.startswith('video/')
        try:
            from core.bunny import upload_file
            url = upload_file(f, 'courses')
        except RuntimeError as e:
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'url': url, 'type': 'video' if is_video else 'image'})


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
        resp = HttpResponse()
        resp['HX-Redirect'] = f'/courses/{pk}/'
        return resp
