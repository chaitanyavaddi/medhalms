from django.conf import settings
from django.db import models

from courses.models import Course
from ide.models import Lab


class Quiz(models.Model):
    class Type(models.TextChoices):
        MCQ    = 'mcq',    'MCQ Only'
        CODING = 'coding', 'Coding Only'
        MIXED  = 'mixed',  'MCQ + Coding'

    class Difficulty(models.TextChoices):
        BEGINNER     = 'beginner',     'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED     = 'advanced',     'Advanced'

    class Status(models.TextChoices):
        DRAFT     = 'draft',     'Draft'
        PUBLISHED = 'published', 'Published'

    title             = models.CharField(max_length=255)
    description       = models.TextField(blank=True)
    quiz_type         = models.CharField(max_length=10, choices=Type.choices, default=Type.MCQ)
    difficulty        = models.CharField(max_length=15, choices=Difficulty.choices, default=Difficulty.BEGINNER)
    status            = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    courses           = models.ManyToManyField(Course, related_name='quizzes', blank=True)
    created_by        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_quizzes')
    time_limit        = models.PositiveIntegerField(null=True, blank=True, help_text='Minutes. Null = no limit.')
    start_date        = models.DateTimeField(null=True, blank=True, help_text='When the quiz becomes available. Null = immediately.')
    expiry_date       = models.DateTimeField(null=True, blank=True)
    max_retries       = models.PositiveIntegerField(null=True, blank=True, help_text='Null = unlimited.')
    passing_score     = models.PositiveIntegerField(default=70, help_text='Percentage required to pass.')
    shuffle_questions = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def total_points(self):
        return self.questions.aggregate(t=models.Sum('points'))['t'] or 0


class Question(models.Model):
    class Type(models.TextChoices):
        SINGLE   = 'single',   'Single Correct'
        MULTIPLE = 'multiple', 'Multiple Correct'
        TF       = 'tf',       'True / False'
        OPEN     = 'open',     'Open Text'
        CODING   = 'coding',   'Coding'

    quiz          = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=10, choices=Type.choices, default=Type.SINGLE)
    text          = models.TextField()
    order         = models.PositiveIntegerField(default=0)
    points        = models.PositiveIntegerField(default=1)
    lab           = models.ForeignKey(Lab, on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz_questions')

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'Q{self.order}: {self.text[:60]}'


class Choice(models.Model):
    question   = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text       = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text[:60]


class QuizAttempt(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        SUBMITTED   = 'submitted',   'Submitted'
        GRADED      = 'graded',      'Graded'

    quiz           = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    attempt_number = models.PositiveIntegerField(default=1)
    status         = models.CharField(max_length=15, choices=Status.choices, default=Status.IN_PROGRESS)
    score          = models.FloatField(null=True, blank=True)
    passed         = models.BooleanField(null=True, blank=True)
    started_at     = models.DateTimeField(auto_now_add=True)
    submitted_at   = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        unique_together = [('quiz', 'student', 'attempt_number')]

    def __str__(self):
        return f'{self.student} — {self.quiz} attempt #{self.attempt_number}'


class QuizAnswer(models.Model):
    attempt          = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question         = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_choices = models.ManyToManyField(Choice, blank=True)
    text_answer      = models.TextField(blank=True)
    code_answer      = models.TextField(blank=True)
    points_earned    = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = [('attempt', 'question')]

    def __str__(self):
        return f'Answer: attempt#{self.attempt_id} q#{self.question_id}'
