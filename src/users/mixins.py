from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from users.models import User


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Restrict a view to users with specific roles.

    Usage — declare `allowed_roles` on the view class:

        class MyCourseAdminView(RoleRequiredMixin, View):
            allowed_roles = [User.Role.TRAINER, User.Role.ADMIN]
    """
    allowed_roles: list = []
    raise_exception = True

    def test_func(self):
        return self.request.user.role in self.allowed_roles


class ActiveStudentRequiredMixin(LoginRequiredMixin):
    """
    Allow only students whose status is ACTIVE.
    Pending/inactive/banned students are sent to the pending-approval page.

    Use this on any view that students can access only after approval.
    """
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role == User.Role.STUDENT and request.user.status != User.Status.ACTIVE:
            return redirect('dashboard:pending_approval')
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Allow only admins (role=admin or is_superuser).

    Use this on admin-only views instead of the superuser-specific
    SuperuserRequiredMixin when role-level admins should also have access.
    """
    raise_exception = True

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == User.Role.ADMIN


class TrainerOrAboveRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Allow trainers, staff, admins, and superusers.
    Block students.
    """
    raise_exception = True

    def test_func(self):
        allowed = {User.Role.TRAINER, User.Role.STAFF, User.Role.ADMIN}
        return self.request.user.is_superuser or self.request.user.role in allowed
