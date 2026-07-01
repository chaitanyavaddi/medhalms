from courses.models import Course
from .models import User


class UserService:
    @staticmethod
    def courses_for_user(user_obj):
        """Return (all_courses queryset, selected_course_ids set) for the user form modal."""
        all_courses = Course.objects.filter(is_deleted=False).order_by('name')
        if user_obj is None:
            return all_courses, set()
        if user_obj.role == User.Role.TRAINER:
            selected_ids = set(user_obj.assigned_courses.values_list('pk', flat=True))
        elif user_obj.role == User.Role.STUDENT:
            selected_ids = set(user_obj.enrolled_courses.values_list('pk', flat=True))
        else:
            selected_ids = set()
        return all_courses, selected_ids

    @staticmethod
    def update_course_assignments(user_obj, selected_course_ids):
        """Sync course M2M for a trainer or student from a list of selected course PKs."""
        if user_obj.role == User.Role.TRAINER:
            for course in Course.objects.filter(is_deleted=False):
                if str(course.pk) in selected_course_ids:
                    course.trainers.add(user_obj)
                else:
                    course.trainers.remove(user_obj)
        elif user_obj.role == User.Role.STUDENT:
            for course in Course.objects.filter(is_deleted=False):
                if str(course.pk) in selected_course_ids:
                    course.students.add(user_obj)
                else:
                    course.students.remove(user_obj)
