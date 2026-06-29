import json
import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views import View

from courses.models import Course
from ide.models import Lab
from users.models import User
from utils.view_helper import redirect_to

from .models import Choice, Question, Quiz, QuizAnswer, QuizAttempt

OC_PARAMS = (
    "hideLanguageSelection=true&hideRun=true&hideNew=true&hideTitle=true"
    "&hideEditorOptions=true&hideNewFileOption=true&listenToEvents=true"
    "&codeChangeEvent=true&theme=dark"
)


def _can_manage(user):
    return user.is_superuser or user.role == 'trainer'


def _embed_url(lab):
    return f"https://onecompiler.com/embed/{lab.oc_slug}?{OC_PARAMS}"


def _autograde_attempt(attempt):
    """Grade all MCQ/TF answers and compute total score. Open/coding left as pending."""
    total_points = 0
    earned_points = 0.0

    for answer in attempt.answers.select_related('question').prefetch_related('selected_choices', 'question__choices'):
        q = answer.question
        total_points += q.points

        if q.question_type in (Question.Type.SINGLE, Question.Type.MULTIPLE, Question.Type.TF):
            correct_ids = set(q.choices.filter(is_correct=True).values_list('id', flat=True))
            selected_ids = set(answer.selected_choices.values_list('id', flat=True))
            if correct_ids == selected_ids:
                answer.points_earned = q.points
                earned_points += q.points
            else:
                answer.points_earned = 0
            answer.save(update_fields=['points_earned'])
        # open/coding: points_earned stays null (pending manual review)

    if total_points > 0:
        attempt.score = round((earned_points / total_points) * 100, 1)
    else:
        attempt.score = 0

    quiz = attempt.quiz
    # Only mark passed if no pending answers exist
    has_pending = attempt.answers.filter(points_earned__isnull=True).exclude(
        question__question_type__in=[Question.Type.OPEN, Question.Type.CODING]
    ).exists()
    if not has_pending:
        attempt.passed = attempt.score >= quiz.passing_score

    attempt.status = QuizAttempt.Status.GRADED
    attempt.submitted_at = timezone.now()
    attempt.save(update_fields=['score', 'passed', 'status', 'submitted_at'])


# ── Quiz list ────────────────────────────────────────────────────────────────

class QuizListView(LoginRequiredMixin, View):
    def get(self, request):
        if _can_manage(request.user):
            quizzes = Quiz.objects.prefetch_related('courses').all()
        else:
            quizzes = Quiz.objects.filter(status=Quiz.Status.PUBLISHED).prefetch_related('courses')
        return render(request, 'quizzes/list.html', {
            'quizzes': quizzes,
            'can_manage': _can_manage(request.user),
        })


# ── Quiz create / edit ───────────────────────────────────────────────────────

_FDATA_DEFAULTS = {
    'title': '', 'description': '', 'quiz_type': Quiz.Type.MCQ,
    'difficulty': Quiz.Difficulty.BEGINNER, 'status': Quiz.Status.DRAFT,
    'time_limit': '', 'start_date': '', 'expiry_date': '',
    'max_retries': '', 'passing_score': '70',
    'shuffle_questions': False, 'courses': [],
}


class QuizCreateView(LoginRequiredMixin, View):
    TEMPLATE = 'quizzes/form.html'

    def _ctx(self, fdata=None):
        return {
            'quiz': None,
            'courses': Course.objects.filter(is_deleted=False).order_by('name'),
            'selected_course_ids': set(),
            'fdata': {**_FDATA_DEFAULTS, **(fdata or {})},
        }

    def get(self, request):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        return render(request, self.TEMPLATE, self._ctx())

    def post(self, request):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        fdata = {
            'title':             request.POST.get('title', '').strip(),
            'description':       request.POST.get('description', '').strip(),
            'quiz_type':         request.POST.get('quiz_type', Quiz.Type.MCQ),
            'difficulty':        request.POST.get('difficulty', Quiz.Difficulty.BEGINNER),
            'status':            request.POST.get('status', Quiz.Status.DRAFT),
            'time_limit':        request.POST.get('time_limit', '').strip(),
            'start_date':        request.POST.get('start_date', '').strip(),
            'expiry_date':       request.POST.get('expiry_date', '').strip(),
            'max_retries':       request.POST.get('max_retries', '').strip(),
            'passing_score':     request.POST.get('passing_score', '70').strip(),
            'shuffle_questions': bool(request.POST.get('shuffle_questions')),
            'courses':           request.POST.getlist('courses'),
        }
        if not fdata['title']:
            messages.error(request, 'Quiz title is required.')
            return render(request, self.TEMPLATE, self._ctx(fdata))
        quiz = Quiz.objects.create(
            title=fdata['title'],
            description=fdata['description'],
            quiz_type=fdata['quiz_type'],
            difficulty=fdata['difficulty'],
            status=fdata['status'],
            time_limit=int(fdata['time_limit']) if fdata['time_limit'].isdigit() else None,
            start_date=parse_datetime(fdata['start_date']) if fdata['start_date'] else None,
            expiry_date=parse_datetime(fdata['expiry_date']) if fdata['expiry_date'] else None,
            max_retries=int(fdata['max_retries']) if fdata['max_retries'].isdigit() else None,
            passing_score=int(fdata['passing_score']) if fdata['passing_score'].isdigit() else 70,
            shuffle_questions=fdata['shuffle_questions'],
            created_by=request.user,
        )
        if fdata['courses']:
            quiz.courses.set(fdata['courses'])
        messages.success(request, f'Quiz "{quiz.title}" created.')
        return redirect_to(request, reverse('quizzes:builder', kwargs={'pk': quiz.pk}))


class QuizUpdateView(LoginRequiredMixin, View):
    TEMPLATE = 'quizzes/form.html'

    def _ctx(self, quiz, fdata=None):
        selected_ids = set(quiz.courses.values_list('pk', flat=True)) if quiz else set()
        return {
            'quiz': quiz,
            'courses': Course.objects.filter(is_deleted=False).order_by('name'),
            'selected_course_ids': selected_ids,
            'fdata': {**_FDATA_DEFAULTS, **(fdata or {})},
        }

    def get(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz = get_object_or_404(Quiz, pk=pk)
        return render(request, self.TEMPLATE, self._ctx(quiz))

    def post(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz = get_object_or_404(Quiz, pk=pk)
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, 'Quiz title is required.')
            return render(request, self.TEMPLATE, self._ctx(quiz))
        quiz.title             = title
        quiz.description       = request.POST.get('description', '').strip()
        quiz.quiz_type         = request.POST.get('quiz_type', quiz.quiz_type)
        quiz.difficulty        = request.POST.get('difficulty', quiz.difficulty)
        quiz.status            = request.POST.get('status', quiz.status)
        tl = request.POST.get('time_limit', '').strip()
        quiz.time_limit        = int(tl) if tl.isdigit() else None
        sd = request.POST.get('start_date', '').strip()
        quiz.start_date        = parse_datetime(sd) if sd else None
        ed = request.POST.get('expiry_date', '').strip()
        quiz.expiry_date       = parse_datetime(ed) if ed else None
        mr = request.POST.get('max_retries', '').strip()
        quiz.max_retries       = int(mr) if mr.isdigit() else None
        ps = request.POST.get('passing_score', '70').strip()
        quiz.passing_score     = int(ps) if ps.isdigit() else 70
        quiz.shuffle_questions = bool(request.POST.get('shuffle_questions'))
        quiz.save()
        quiz.courses.set(request.POST.getlist('courses'))
        messages.success(request, f'Quiz "{quiz.title}" updated.')
        return redirect_to(request, reverse('quizzes:builder', kwargs={'pk': quiz.pk}))


class QuizDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz = get_object_or_404(Quiz, pk=pk)
        name = quiz.title
        quiz.delete()
        messages.success(request, f'Quiz "{name}" deleted.')
        resp = HttpResponse()
        resp['HX-Redirect'] = reverse('quizzes:list')
        return resp


# ── Quiz wizard ──────────────────────────────────────────────────────────────

class QuizWizardView(LoginRequiredMixin, View):
    def get(self, request):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        return render(request, 'quizzes/partials/wizard.html', {
            'step': 1, 'quiz_types': Quiz.Type.choices,
        })

    def post(self, request):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        step = request.POST.get('step', '1')
        if step == '1':
            quiz_type = request.POST.get('quiz_type', '').strip()
            if not quiz_type:
                return render(request, 'quizzes/partials/wizard.html', {
                    'step': 1, 'quiz_types': Quiz.Type.choices,
                    'error': 'Please select a quiz type.',
                })
            return render(request, 'quizzes/partials/wizard.html', {
                'step': 2, 'quiz_type': quiz_type,
                'quiz_type_label': dict(Quiz.Type.choices).get(quiz_type, quiz_type),
                'difficulties': Quiz.Difficulty.choices,
                'fdata': {'title': '', 'description': '', 'time_limit': '',
                          'passing_score': '70', 'difficulty': Quiz.Difficulty.BEGINNER, 'max_retries': ''},
            })
        # Step 2 — create quiz
        title = request.POST.get('title', '').strip()
        quiz_type = request.POST.get('quiz_type', Quiz.Type.MCQ)
        if not title:
            return render(request, 'quizzes/partials/wizard.html', {
                'step': 2, 'quiz_type': quiz_type,
                'quiz_type_label': dict(Quiz.Type.choices).get(quiz_type, quiz_type),
                'difficulties': Quiz.Difficulty.choices,
                'error': 'Title is required.',
                'fdata': {
                    'title': title,
                    'description': request.POST.get('description', ''),
                    'time_limit': request.POST.get('time_limit', ''),
                    'passing_score': request.POST.get('passing_score', '70'),
                    'difficulty': request.POST.get('difficulty', Quiz.Difficulty.BEGINNER),
                    'max_retries': request.POST.get('max_retries', ''),
                },
            })
        tl = request.POST.get('time_limit', '').strip()
        mr = request.POST.get('max_retries', '').strip()
        ps = request.POST.get('passing_score', '70').strip()
        quiz = Quiz.objects.create(
            title=title,
            quiz_type=quiz_type,
            description=request.POST.get('description', '').strip(),
            difficulty=request.POST.get('difficulty', Quiz.Difficulty.BEGINNER),
            status=Quiz.Status.DRAFT,
            time_limit=int(tl) if tl.isdigit() else None,
            passing_score=int(ps) if ps.isdigit() else 70,
            max_retries=int(mr) if mr.isdigit() else None,
            created_by=request.user,
        )
        resp = HttpResponse()
        resp['HX-Redirect'] = reverse('quizzes:builder', args=[quiz.pk])
        return resp


# ── Question builder ─────────────────────────────────────────────────────────

class QuizBuilderView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz = get_object_or_404(Quiz, pk=pk)
        questions = quiz.questions.prefetch_related('choices', 'lab')
        return render(request, 'quizzes/builder.html', {
            'quiz': quiz,
            'questions': questions,
        })


def _render_question_card(request, quiz, question, mode='view', q_type=None, error=None):
    qt = q_type or (question.question_type if question else Question.Type.SINGLE)
    labs = Lab.objects.filter(is_embed=True).order_by('name') if qt == Question.Type.CODING else None
    return render(request, 'quizzes/partials/question_card.html', {
        'quiz': quiz, 'question': question, 'mode': mode, 'q_type': qt,
        'labs': labs, 'error': error,
    })


class QuestionAddView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz = get_object_or_404(Quiz, pk=pk)
        q_type = request.GET.get('type', Question.Type.SINGLE)
        return _render_question_card(request, quiz, None, mode='edit', q_type=q_type)

    def post(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz   = get_object_or_404(Quiz, pk=pk)
        q_type = request.POST.get('question_type', Question.Type.SINGLE)
        text   = request.POST.get('text', '').strip()
        if not text:
            return _render_question_card(request, quiz, None, mode='edit', q_type=q_type,
                                         error='Question text is required.')
        points   = int(request.POST.get('points', 1) or 1)
        lab_id   = request.POST.get('lab_id', '').strip()
        question = Question.objects.create(
            quiz=quiz, question_type=q_type, text=text,
            order=quiz.questions.count(), points=points,
            lab=Lab.objects.filter(pk=lab_id).first() if lab_id else None,
        )
        if q_type in (Question.Type.SINGLE, Question.Type.MULTIPLE, Question.Type.TF):
            for i, ct in enumerate(request.POST.getlist('choice_text')):
                ct = ct.strip()
                if ct:
                    Choice.objects.create(question=question, text=ct,
                                          is_correct=str(i) in request.POST.getlist('choice_correct'), order=i)
        return _render_question_card(request, quiz, question, mode='view')


class QuestionEditView(LoginRequiredMixin, View):
    def get(self, request, pk, qpk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz     = get_object_or_404(Quiz, pk=pk)
        question = get_object_or_404(Question, pk=qpk, quiz=quiz)
        mode = 'view' if request.GET.get('view') == '1' else 'edit'
        return _render_question_card(request, quiz, question, mode=mode)

    def post(self, request, pk, qpk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz     = get_object_or_404(Quiz, pk=pk)
        question = get_object_or_404(Question, pk=qpk, quiz=quiz)
        text = request.POST.get('text', '').strip()
        if not text:
            return _render_question_card(request, quiz, question, mode='edit',
                                         error='Question text is required.')
        question.text   = text
        question.points = int(request.POST.get('points', 1) or 1)
        if question.question_type == Question.Type.CODING:
            lab_id = request.POST.get('lab_id', '').strip()
            question.lab = Lab.objects.filter(pk=lab_id).first() if lab_id else None
        question.save(update_fields=['text', 'points', 'lab'])
        if question.question_type in (Question.Type.SINGLE, Question.Type.MULTIPLE, Question.Type.TF):
            question.choices.all().delete()
            for i, ct in enumerate(request.POST.getlist('choice_text')):
                ct = ct.strip()
                if ct:
                    Choice.objects.create(question=question, text=ct,
                                          is_correct=str(i) in request.POST.getlist('choice_correct'), order=i)
        return _render_question_card(request, quiz, question, mode='view')


class QuestionDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, qpk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz     = get_object_or_404(Quiz, pk=pk)
        question = get_object_or_404(Question, pk=qpk, quiz=quiz)
        question.delete()
        for i, q in enumerate(quiz.questions.order_by('order', 'id')):
            if q.order != i:
                Question.objects.filter(pk=q.pk).update(order=i)
        return HttpResponse('')


class QuestionReorderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        quiz  = get_object_or_404(Quiz, pk=pk)
        order = json.loads(request.body).get('order', [])
        for i, qid in enumerate(order):
            Question.objects.filter(pk=qid, quiz=quiz).update(order=i)
        return HttpResponse('')


class LabsPickerView(LoginRequiredMixin, View):
    def get(self, request):
        if not _can_manage(request.user):
            return HttpResponseForbidden()
        labs = Lab.objects.filter(is_embed=True).order_by('name')
        return render(request, 'quizzes/partials/labs_picker.html', {'labs': labs})


# ── Student take flow ────────────────────────────────────────────────────────

class QuizTakeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk, status=Quiz.Status.PUBLISHED)

        # Start date check
        if quiz.start_date and timezone.now() < quiz.start_date:
            messages.error(request, f'This quiz opens on {quiz.start_date.strftime("%b %d, %Y at %H:%M")}.')
            return redirect_to(request, reverse('quizzes:list'))

        # Expiry check
        if quiz.expiry_date and timezone.now() > quiz.expiry_date:
            messages.error(request, 'This quiz has expired.')
            return redirect_to(request, reverse('quizzes:list'))

        # Retries check
        past = QuizAttempt.objects.filter(quiz=quiz, student=request.user).count()
        if quiz.max_retries is not None and past >= quiz.max_retries:
            messages.error(request, 'You have used all your attempts for this quiz.')
            return redirect_to(request, reverse('quizzes:list'))

        # Resume in-progress attempt or create new one
        attempt = QuizAttempt.objects.filter(
            quiz=quiz, student=request.user, status=QuizAttempt.Status.IN_PROGRESS
        ).first()
        if not attempt:
            attempt = QuizAttempt.objects.create(
                quiz=quiz, student=request.user,
                attempt_number=past + 1,
            )

        questions = list(quiz.questions.prefetch_related('choices', 'lab'))
        if quiz.shuffle_questions:
            random.shuffle(questions)

        # Pre-build existing answers map
        answers = {a.question_id: a for a in attempt.answers.prefetch_related('selected_choices')}

        q_data = []
        for q in questions:
            embed_url = _embed_url(q.lab) if q.question_type == Question.Type.CODING and q.lab else None
            q_data.append({'q': q, 'answer': answers.get(q.pk), 'embed_url': embed_url})

        return render(request, 'quizzes/take.html', {
            'quiz': quiz,
            'attempt': attempt,
            'q_data': q_data,
        })


class QuizSubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        quiz    = get_object_or_404(Quiz, pk=pk, status=Quiz.Status.PUBLISHED)
        attempt = get_object_or_404(
            QuizAttempt, quiz=quiz, student=request.user, status=QuizAttempt.Status.IN_PROGRESS
        )

        for question in quiz.questions.prefetch_related('choices'):
            answer, _ = QuizAnswer.objects.get_or_create(attempt=attempt, question=question)

            if question.question_type in (Question.Type.SINGLE, Question.Type.TF):
                choice_id = request.POST.get(f'q_{question.pk}')
                answer.selected_choices.clear()
                if choice_id:
                    try:
                        answer.selected_choices.add(question.choices.get(pk=choice_id))
                    except Choice.DoesNotExist:
                        pass

            elif question.question_type == Question.Type.MULTIPLE:
                choice_ids = request.POST.getlist(f'q_{question.pk}')
                answer.selected_choices.set(question.choices.filter(pk__in=choice_ids))

            elif question.question_type == Question.Type.OPEN:
                answer.text_answer = request.POST.get(f'q_{question.pk}', '').strip()
                answer.save(update_fields=['text_answer'])

            elif question.question_type == Question.Type.CODING:
                answer.code_answer = request.POST.get(f'q_{question.pk}', '').strip()
                answer.save(update_fields=['code_answer'])

        _autograde_attempt(attempt)
        messages.success(request, 'Quiz submitted!')
        return redirect_to(request, reverse('quizzes:attempt_result', kwargs={'pk': pk, 'apk': attempt.pk}))


class AttemptResultView(LoginRequiredMixin, View):
    def get(self, request, pk, apk):
        quiz    = get_object_or_404(Quiz, pk=pk)
        attempt = get_object_or_404(QuizAttempt, pk=apk, quiz=quiz)
        if not _can_manage(request.user) and attempt.student != request.user:
            return HttpResponseForbidden()
        answers = attempt.answers.select_related('question').prefetch_related(
            'selected_choices', 'question__choices'
        ).order_by('question__order')
        return render(request, 'quizzes/result.html', {
            'quiz': quiz,
            'attempt': attempt,
            'answers': answers,
        })
