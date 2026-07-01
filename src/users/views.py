from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from utils.view_helper import redirect_to
from .models import User
from .service import UserService


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_superuser


_ROLE_CONFIG = {
    'students': {'value': User.Role.STUDENT, 'singular': 'Student',     'plural': 'Students'},
    'trainers': {'value': User.Role.TRAINER, 'singular': 'Trainer',     'plural': 'Trainers'},
    'staff':    {'value': User.Role.STAFF,   'singular': 'Staff member', 'plural': 'Staff'},
    'admins':   {'value': User.Role.ADMIN,   'singular': 'Admin',        'plural': 'Admins'},
}


class UserManageView(SuperuserRequiredMixin, View):
    def get(self, request):
        return redirect_to(request, 'users:students')


class UserRoleView(SuperuserRequiredMixin, View):
    def get(self, request, role_slug):
        config = _ROLE_CONFIG.get(role_slug)
        if not config:
            return redirect_to(request, 'users:students')
        users = User.objects.filter(role=config['value']).order_by('-created_at')
        ctx = {
            'users':        users,
            'role_slug':    role_slug,
            'role_value':   config['value'],
            'role_singular': config['singular'],
            'role_plural':  config['plural'],
        }
        if request.headers.get('HX-Request'):
            return render(request, 'users/partials/user_table.html', ctx)
        return render(request, 'users/manage.html', ctx)


class UserCreateView(SuperuserRequiredMixin, View):
    def get(self, request):
        role = request.GET.get('role', User.Role.STUDENT)
        return render(request, 'users/partials/user_form_modal.html', {
            'role':      role,
            'user_obj':  None,
            'form_data': {'first_name': '', 'last_name': '', 'email': ''},
        })

    def post(self, request):
        email      = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        role       = request.POST.get('role', User.Role.STUDENT)
        status     = request.POST.get('status', User.Status.ACTIVE)
        password   = request.POST.get('password', '').strip()

        error = None
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif User.objects.filter(email=email).exists():
            error = 'A user with this email already exists.'

        if error:
            return render(request, 'users/partials/user_form_modal.html', {
                'role':      role,
                'user_obj':  None,
                'error':     error,
                'form_data': {
                    'first_name': first_name,
                    'last_name':  last_name,
                    'email':      email,
                },
            })

        User.objects.create_user(
            email=email, password=password,
            first_name=first_name, last_name=last_name,
            role=role, status=status,
        )
        name = f'{first_name} {last_name}'.strip() or email
        messages.success(request, f'User "{name}" created.')
        resp = HttpResponse()
        resp['HX-Trigger'] = 'closeModal'
        return resp


class UserUpdateView(SuperuserRequiredMixin, View):
    def get(self, request, pk):
        user_obj = get_object_or_404(User, pk=pk)
        all_courses, selected_ids = UserService.courses_for_user(user_obj)
        return render(request, 'users/partials/user_form_modal.html', {
            'role':                user_obj.role,
            'user_obj':            user_obj,
            'all_courses':         all_courses,
            'selected_course_ids': selected_ids,
            'form_data': {
                'first_name': user_obj.first_name,
                'last_name':  user_obj.last_name,
                'email':      user_obj.email,
            },
        })

    def post(self, request, pk):
        user_obj = get_object_or_404(User, pk=pk)
        user_obj.first_name = request.POST.get('first_name', '').strip()
        user_obj.last_name  = request.POST.get('last_name', '').strip()
        user_obj.status     = request.POST.get('status', User.Status.ACTIVE)
        new_password = request.POST.get('password', '').strip()
        if new_password:
            user_obj.set_password(new_password)
        user_obj.save()

        # Update course assignments based on role
        selected_course_ids = request.POST.getlist('courses')
        UserService.update_course_assignments(user_obj, selected_course_ids)

        name = user_obj.get_full_name() or user_obj.email
        messages.success(request, f'User "{name}" updated.')
        resp = HttpResponse()
        resp['HX-Trigger'] = 'closeModal'
        return resp


class UserDeleteView(SuperuserRequiredMixin, View):
    def get(self, request, pk):
        user_obj = get_object_or_404(User, pk=pk)
        return render(request, 'users/partials/user_delete_modal.html', {
            'user_obj': user_obj,
        })

    def post(self, request, pk):
        user_obj = get_object_or_404(User, pk=pk)
        name = user_obj.get_full_name() or user_obj.email
        user_obj.delete()
        messages.success(request, f'User "{name}" deleted.')
        resp = HttpResponse()
        resp['HX-Trigger'] = 'closeModal'
        return resp
