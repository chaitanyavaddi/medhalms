from interviews.models import InterviewSession
from quizzes.models import QuizAttempt
from users.models import User


class TrainerDashboardService:
    @staticmethod
    def get_context(user):
        """Return dashboard context dict for a trainer user."""
        courses = user.assigned_courses.prefetch_related('students').filter(is_deleted=False)

        student_ids = (
            User.objects
            .filter(enrolled_courses__in=courses)
            .distinct()
            .values_list('pk', flat=True)
        )
        student_count = len(student_ids)

        pending_count = (
            User.objects
            .filter(enrolled_courses__in=courses, status=User.Status.PENDING)
            .distinct()
            .count()
        )

        recent_attempts = (
            QuizAttempt.objects
            .filter(student__in=student_ids, quiz__courses__in=courses)
            .select_related('quiz', 'student')
            .order_by('-submitted_at')[:10]
        )

        recent_sessions = (
            InterviewSession.objects
            .filter(user__in=student_ids, interview__courses__in=courses)
            .select_related('interview', 'user')
            .order_by('-started_at')[:10]
        )

        return {
            'courses':         courses,
            'course_count':    courses.count(),
            'student_count':   student_count,
            'pending_count':   pending_count,
            'recent_attempts': recent_attempts,
            'recent_sessions': recent_sessions,
        }
