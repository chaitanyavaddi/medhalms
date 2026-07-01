import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from courses.access import get_user_course_ids
from courses.models import Course
from users.models import User
from utils.view_helper import htmx, redirect_to

from .models import Interview, InterviewAnswer, InterviewSession, Question
from .schemas import InterviewSchema

FORM_TEMPLATE = 'interviews/form.html'


def _can_manage_interview(user):
    return user.is_superuser or user.role == 'trainer'


class InterviewListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        interviews = Interview.objects.prefetch_related('questions', 'courses').all()

        user_course_ids = get_user_course_ids(user)
        if user_course_ids is not None:
            accessible_iv_ids = frozenset(
                Interview.objects.filter(courses__in=user_course_ids).values_list('pk', flat=True)
            )
        else:
            accessible_iv_ids = None

        return render(request, 'interviews/list.html', {
            'interviews':         interviews,
            'can_manage':         _can_manage_interview(user),
            'accessible_iv_ids':  accessible_iv_ids,
            'is_restricted':      accessible_iv_ids is not None,
        })


class InterviewCreateView(LoginRequiredMixin, View):
    def _ctx(self, user, data=None):
        trainer_course_ids = get_user_course_ids(user)
        return {
            'interview':           None,
            'courses':             Course.objects.all(),
            'difficulties':        Interview.Difficulty.choices,
            'data':                data or {},
            'trainer_course_ids':  trainer_course_ids,
            'is_course_restricted': trainer_course_ids is not None,
        }

    def get(self, request):
        if not _can_manage_interview(request.user):
            return HttpResponseForbidden()
        return render(request, FORM_TEMPLATE, self._ctx(request.user))

    def post(self, request):
        if not _can_manage_interview(request.user):
            return HttpResponseForbidden()
        hx     = htmx(request)
        schema = InterviewSchema.from_post(request)
        tmpl   = f'{FORM_TEMPLATE}#interview-form' if hx else FORM_TEMPLATE
        if not schema.is_valid():
            return render(request, tmpl, self._ctx(request.user, data=request.POST))
        iv = Interview.objects.create(
            title          = schema.title,
            persona_prompt = schema.persona_prompt,
            difficulty     = schema.difficulty,
            max_duration   = schema.max_duration,
            created_by     = request.user,
        )
        trainer_course_ids = get_user_course_ids(request.user)
        allowed_courses = schema.courses
        if trainer_course_ids is not None:
            allowed_courses = [c for c in schema.courses if int(c) in trainer_course_ids]
        iv.courses.set(allowed_courses)
        _save_questions(iv, schema.questions)
        messages.success(request, f'Interview "{iv.title}" created.')
        return redirect_to(request, reverse('interviews:detail', args=[iv.pk]))


class InterviewUpdateView(LoginRequiredMixin, View):
    def _ctx(self, interview, user, data=None):
        d = data or {
            'title':          interview.title,
            'persona_prompt': interview.persona_prompt,
            'difficulty':     interview.difficulty,
            'max_duration':   interview.max_duration,
        }
        trainer_course_ids = get_user_course_ids(user)
        return {
            'interview':           interview,
            'courses':             Course.objects.all(),
            'difficulties':        Interview.Difficulty.choices,
            'data':                d,
            'trainer_course_ids':  trainer_course_ids,
            'is_course_restricted': trainer_course_ids is not None,
        }

    def get(self, request, pk):
        if not _can_manage_interview(request.user):
            return HttpResponseForbidden()
        iv = get_object_or_404(Interview, pk=pk)
        return render(request, FORM_TEMPLATE, self._ctx(iv, request.user))

    def post(self, request, pk):
        if not _can_manage_interview(request.user):
            return HttpResponseForbidden()
        iv     = get_object_or_404(Interview, pk=pk)
        hx     = htmx(request)
        schema = InterviewSchema.from_post(request)
        tmpl   = f'{FORM_TEMPLATE}#interview-form' if hx else FORM_TEMPLATE
        if not schema.is_valid():
            return render(request, tmpl, self._ctx(iv, request.user, data=request.POST))
        iv.title          = schema.title
        iv.persona_prompt = schema.persona_prompt
        iv.difficulty     = schema.difficulty
        iv.max_duration   = schema.max_duration
        iv.save()
        trainer_course_ids = get_user_course_ids(request.user)
        if trainer_course_ids is not None:
            existing_other = list(iv.courses.exclude(pk__in=trainer_course_ids).values_list('pk', flat=True))
            allowed = [c for c in schema.courses if int(c) in trainer_course_ids]
            iv.courses.set(existing_other + allowed)
        else:
            iv.courses.set(schema.courses)
        iv.questions.all().delete()
        _save_questions(iv, schema.questions)
        messages.success(request, f'Interview "{iv.title}" updated.')
        return redirect_to(request, reverse('interviews:detail', args=[iv.pk]))


class InterviewDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        iv = get_object_or_404(Interview, pk=pk)
        title = iv.title
        iv.delete()
        messages.success(request, f'Interview "{title}" deleted.')
        return redirect_to(request, reverse('interviews:list'))


def _save_questions(interview, question_texts):
    for i, text in enumerate(question_texts):
        Question.objects.create(interview=interview, order=i + 1, text=text)


class InterviewDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        return render(request, 'interviews/detail.html', {'interview': interview})


class SessionStartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        session   = InterviewSession.objects.create(interview=interview, user=request.user)
        return redirect_to(request, reverse('interviews:session_room', args=[session.pk]))


class SessionRoomView(LoginRequiredMixin, View):
    def get(self, request, session_pk):
        session   = get_object_or_404(InterviewSession, pk=session_pk, user=request.user)
        questions = list(session.interview.questions.values('id', 'order', 'text'))
        return render(request, 'interviews/room.html', {
            'session':   session,
            'questions': questions,
        })


class AnswerSaveView(LoginRequiredMixin, View):
    def post(self, request, session_pk):
        session     = get_object_or_404(InterviewSession, pk=session_pk, user=request.user)
        question_id = request.POST.get('question_id')
        transcript  = request.POST.get('transcript', '').strip()
        duration    = int(request.POST.get('duration', 0))
        question    = get_object_or_404(Question, pk=question_id, interview=session.interview)
        InterviewAnswer.objects.update_or_create(
            session=session, question=question,
            defaults={'transcript': transcript, 'duration_seconds': duration},
        )
        return JsonResponse({'ok': True})


class SessionEndView(LoginRequiredMixin, View):
    def post(self, request, session_pk):
        session = get_object_or_404(InterviewSession, pk=session_pk, user=request.user)
        session.status   = InterviewSession.Status.COMPLETED
        session.ended_at = timezone.now()
        session.save(update_fields=['status', 'ended_at'])
        return JsonResponse({'ok': True, 'result_url': reverse('interviews:session_result', args=[session_pk])})


class SessionResultView(LoginRequiredMixin, View):
    def get(self, request, session_pk):
        session = get_object_or_404(InterviewSession, pk=session_pk, user=request.user)
        answers_data = list(
            session.answers.select_related('question').values(
                'question__order', 'question__text', 'transcript'
            ).order_by('question__order')
        )
        return render(request, 'interviews/result.html', {
            'session':      session,
            'answers_data': answers_data,
        })

    def post(self, request, session_pk):
        session = get_object_or_404(InterviewSession, pk=session_pk, user=request.user)
        try:
            feedback = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'bad json'}, status=400)
        session.feedback = feedback
        session.save(update_fields=['feedback'])
        return JsonResponse({'ok': True})


class InterviewResultsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_superuser or user.is_staff:
            sessions = (InterviewSession.objects
                        .select_related('interview', 'user')
                        .order_by('-ended_at', '-started_at'))
            results_label = 'All Interview Sessions'
            show_student_col = True
            is_trainer_view  = False
        elif user.role == 'trainer':
            # Show interview results for students enrolled in trainer's courses
            student_ids = (User.objects
                           .filter(enrolled_courses__in=user.assigned_courses.all())
                           .values_list('pk', flat=True).distinct())
            sessions = (InterviewSession.objects
                        .filter(user__in=student_ids)
                        .select_related('interview', 'user')
                        .order_by('-ended_at', '-started_at'))
            results_label = "Your Students' Interview Results"
            show_student_col = True
            is_trainer_view  = True
        else:
            sessions = (InterviewSession.objects
                        .filter(user=user)
                        .select_related('interview')
                        .order_by('-ended_at', '-started_at'))
            results_label = 'Your Interview Sessions'
            show_student_col = False
            is_trainer_view  = False

        return render(request, 'interviews/results.html', {
            'sessions':         sessions,
            'is_admin':         user.is_superuser or user.is_staff or user.role == 'trainer',
            'show_student_col': show_student_col,
            'results_label':    results_label,
            'is_trainer_view':  is_trainer_view,
        })
