from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from courses.models import Course
from .models import Interview, InterviewAnswer, InterviewSession, Question


class InterviewListView(LoginRequiredMixin, View):
    def get(self, request):
        interviews = Interview.objects.prefetch_related('questions', 'courses').all()
        return render(request, 'interviews/list.html', {'interviews': interviews})


class InterviewCreateView(LoginRequiredMixin, View):
    def _ctx(self, data=None, interview=None, error=None):
        return {
            'interview': interview,
            'courses':   Course.objects.all(),
            'difficulties': Interview.Difficulty.choices,
            'data': data or {},
            'error': error,
        }

    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return render(request, 'interviews/form.html', self._ctx())

    def post(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        title  = request.POST.get('title', '').strip()
        prompt = request.POST.get('persona_prompt', '').strip()
        if not title or not prompt:
            return render(request, 'interviews/form.html',
                          self._ctx(data=request.POST, error='Title and persona prompt are required.'))
        iv = Interview.objects.create(
            title          = title,
            persona_prompt = prompt,
            difficulty     = request.POST.get('difficulty', Interview.Difficulty.INTERMEDIATE),
            max_duration   = int(request.POST.get('max_duration', 30)),
            created_by     = request.user,
        )
        iv.courses.set(request.POST.getlist('courses'))
        _save_questions(iv, request.POST)
        return redirect('interviews:detail', pk=iv.pk)


class InterviewUpdateView(LoginRequiredMixin, View):
    def _ctx(self, interview, data=None, error=None):
        return {
            'interview':    interview,
            'courses':      Course.objects.all(),
            'difficulties': Interview.Difficulty.choices,
            'data': data or {},
            'error': error,
        }

    def get(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        iv = get_object_or_404(Interview, pk=pk)
        return render(request, 'interviews/form.html', self._ctx(iv))

    def post(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        iv     = get_object_or_404(Interview, pk=pk)
        title  = request.POST.get('title', '').strip()
        prompt = request.POST.get('persona_prompt', '').strip()
        if not title or not prompt:
            return render(request, 'interviews/form.html',
                          self._ctx(iv, data=request.POST, error='Title and persona prompt are required.'))
        iv.title          = title
        iv.persona_prompt = prompt
        iv.difficulty     = request.POST.get('difficulty', iv.difficulty)
        iv.max_duration   = int(request.POST.get('max_duration', iv.max_duration))
        iv.save()
        iv.courses.set(request.POST.getlist('courses'))
        iv.questions.all().delete()
        _save_questions(iv, request.POST)
        return redirect('interviews:detail', pk=iv.pk)


class InterviewDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        get_object_or_404(Interview, pk=pk).delete()
        return redirect('interviews:list')


def _save_questions(interview, post):
    texts = post.getlist('question_text')
    for i, text in enumerate(texts):
        text = text.strip()
        if text:
            Question.objects.create(interview=interview, order=i + 1, text=text)


class InterviewDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        return render(request, 'interviews/detail.html', {'interview': interview})


class SessionStartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        session   = InterviewSession.objects.create(interview=interview, user=request.user)
        return redirect('interviews:session_room', session_pk=session.pk)


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
        return JsonResponse({'ok': True, 'result_url': f'/mock/interviews/session/{session_pk}/result/'})


class SessionResultView(LoginRequiredMixin, View):
    def get(self, request, session_pk):
        session = get_object_or_404(InterviewSession, pk=session_pk, user=request.user)
        return render(request, 'interviews/result.html', {'session': session})

    def post(self, request, session_pk):
        """Store AI-generated feedback (POSTed from browser after Puter call)."""
        import json
        session  = get_object_or_404(InterviewSession, pk=session_pk, user=request.user)
        try:
            feedback = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'bad json'}, status=400)
        session.feedback = feedback
        session.save(update_fields=['feedback'])
        return JsonResponse({'ok': True})
