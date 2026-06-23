import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from courses.models import Course
from utils.view_helper import htmx, redirect_to

from .models import Interview, InterviewAnswer, InterviewSession, Question
from .schemas import InterviewSchema

FORM_TEMPLATE = 'interviews/form.html'


class InterviewListView(LoginRequiredMixin, View):
    def get(self, request):
        interviews = Interview.objects.prefetch_related('questions', 'courses').all()
        return render(request, 'interviews/list.html', {'interviews': interviews})


class InterviewCreateView(LoginRequiredMixin, View):
    def _ctx(self, data=None):
        return {
            'interview':    None,
            'courses':      Course.objects.all(),
            'difficulties': Interview.Difficulty.choices,
            'data':         data or {},
        }

    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return render(request, FORM_TEMPLATE, self._ctx())

    def post(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        hx     = htmx(request)
        schema = InterviewSchema.from_post(request)
        tmpl   = f'{FORM_TEMPLATE}#interview-form' if hx else FORM_TEMPLATE
        if not schema.is_valid():
            return render(request, tmpl, self._ctx(data=request.POST))
        iv = Interview.objects.create(
            title          = schema.title,
            persona_prompt = schema.persona_prompt,
            difficulty     = schema.difficulty,
            max_duration   = schema.max_duration,
            created_by     = request.user,
        )
        iv.courses.set(schema.courses)
        _save_questions(iv, schema.questions)
        messages.success(request, f'Interview "{iv.title}" created.')
        return redirect_to(request, reverse('interviews:detail', args=[iv.pk]))


class InterviewUpdateView(LoginRequiredMixin, View):
    def _ctx(self, interview, data=None):
        d = data or {
            'title':          interview.title,
            'persona_prompt': interview.persona_prompt,
            'difficulty':     interview.difficulty,
            'max_duration':   interview.max_duration,
        }
        return {
            'interview':    interview,
            'courses':      Course.objects.all(),
            'difficulties': Interview.Difficulty.choices,
            'data':         d,
        }

    def get(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        iv = get_object_or_404(Interview, pk=pk)
        return render(request, FORM_TEMPLATE, self._ctx(iv))

    def post(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        iv     = get_object_or_404(Interview, pk=pk)
        hx     = htmx(request)
        schema = InterviewSchema.from_post(request)
        tmpl   = f'{FORM_TEMPLATE}#interview-form' if hx else FORM_TEMPLATE
        if not schema.is_valid():
            return render(request, tmpl, self._ctx(iv, data=request.POST))
        iv.title          = schema.title
        iv.persona_prompt = schema.persona_prompt
        iv.difficulty     = schema.difficulty
        iv.max_duration   = schema.max_duration
        iv.save()
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
        if request.user.is_superuser or request.user.is_staff:
            sessions = (InterviewSession.objects
                        .select_related('interview', 'user')
                        .order_by('-ended_at', '-started_at'))
        else:
            sessions = (InterviewSession.objects
                        .filter(user=request.user)
                        .select_related('interview')
                        .order_by('-ended_at', '-started_at'))
        return render(request, 'interviews/results.html', {
            'sessions': sessions,
            'is_admin': request.user.is_superuser or request.user.is_staff,
        })
