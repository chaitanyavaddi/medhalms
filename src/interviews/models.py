from django.db import models
from django.conf import settings


class Interview(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER     = 'beginner',     'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED     = 'advanced',     'Advanced'

    title          = models.CharField(max_length=200)
    persona_prompt = models.TextField(
        help_text='Describe the interviewer persona and focus area.'
    )
    difficulty     = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.INTERMEDIATE)
    max_duration   = models.PositiveIntegerField(default=30, help_text='Max session length in minutes')
    courses        = models.ManyToManyField('courses.Course', blank=True, related_name='interviews')
    created_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_interviews')
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='questions')
    order     = models.PositiveSmallIntegerField(default=0)
    text      = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Q{self.order}: {self.text[:60]}'


class InterviewSession(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED   = 'completed',   'Completed'
        ABANDONED   = 'abandoned',   'Abandoned'

    interview  = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='sessions')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interview_sessions')
    status     = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at   = models.DateTimeField(null=True, blank=True)
    feedback   = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.user} — {self.interview} ({self.status})'


class InterviewAnswer(models.Model):
    session          = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='answers')
    question         = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    transcript       = models.TextField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    answered_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['question__order']

    def __str__(self):
        return f'Answer to Q{self.question.order} by {self.session.user}'
