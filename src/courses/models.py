from django.db import models

from users.models import User


class Course(models.Model):
    class Status(models.TextChoices):
        DRAFT     = 'draft',     'Draft'
        PUBLISHED = 'published', 'Published'

    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail   = models.URLField(blank=True)
    trainers    = models.ManyToManyField(
        User, related_name='assigned_courses', blank=True,
        limit_choices_to={'role': 'trainer'},
    )
    created_by  = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='created_courses',
    )
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_deleted  = models.BooleanField(default=False)
    deleted_at  = models.DateTimeField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def initials(self):
        words = self.name.split()
        if len(words) >= 2:
            return (words[0][0] + words[1][0]).upper()
        return self.name[:2].upper()

    @property
    def thumb_color(self):
        palette = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#0ea5e9', '#ef4444', '#14b8a6']
        return palette[self.pk % len(palette)]

    @property
    def total_chapters(self):
        return Chapter.objects.filter(module__course=self).count()

    @property
    def first_chapter(self):
        return (
            Chapter.objects
            .filter(module__course=self)
            .order_by('module__order', 'module__created_at', 'order', 'created_at')
            .first()
        )


class Module(models.Model):
    course     = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title      = models.CharField(max_length=255)
    order      = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.course.name} — {self.title}"


class Chapter(models.Model):
    module     = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='chapters')
    title      = models.CharField(max_length=255)
    content    = models.TextField(blank=True)
    order      = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.module.title} — {self.title}"
