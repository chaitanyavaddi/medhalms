from dataclasses import dataclass

from django.conf import settings
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from users.models import User


@dataclass
class LoginSchema:
    email:    str
    password: str

    @classmethod
    def from_post(cls, request) -> "LoginSchema":
        p = request.POST
        return cls(
            email    =p.get('email', '').strip().lower(),
            password =p.get('password', ''),
        )

    def is_valid_credentials(self, request) -> bool:
        if not self.email or not self.password:
            messages.error(request, 'All fields are required')
            return False
        return True

    def is_valid(self, request) -> bool:
        return self.is_valid_credentials(request)


@dataclass
class SignupSchema:
    first_name: str
    last_name:  str
    email:      str
    password:   str
    password1:  str

    @classmethod
    def from_post(cls, request) -> "SignupSchema":
        p = request.POST
        return cls(
            first_name =p.get('first_name', '').strip().title(),
            last_name  =p.get('last_name',  '').strip().title(),
            email      =p.get('email',      '').strip().lower(),
            password   =p.get('password',   ''),
            password1  =p.get('password1',  ''),
        )

    def is_valid_name(self, request) -> bool:
        min_len, max_len = settings.NAME_LENGTH_RANGE
        if not self.first_name:
            messages.error(request, 'First name is required')
            return False
        if not (min_len <= len(self.first_name) <= max_len):
            messages.error(request, f'First name must be {min_len}–{max_len} characters')
            return False
        return True

    def is_valid_email(self, request) -> bool:
        if not self.email:
            messages.error(request, 'Email is required')
            return False
        try:
            validate_email(self.email)
        except ValidationError:
            messages.error(request, 'Enter a valid email address')
            return False
        if User.objects.filter(email=self.email).exists():
            messages.error(request, 'Email already registered')
            return False
        return True

    def is_valid_password(self, request) -> bool:
        min_len, max_len = settings.PASSWORD_LENGTH_RANGE
        if not self.password or not self.password1:
            messages.error(request, 'Password is required')
            return False
        if not (min_len <= len(self.password) <= max_len):
            messages.error(request, f'Password must be {min_len}–{max_len} characters')
            return False
        if self.password != self.password1:
            messages.error(request, "Passwords don't match")
            return False
        return True

    def is_valid(self, request) -> bool:
        return (
            self.is_valid_name(request)
            and self.is_valid_email(request)
            and self.is_valid_password(request)
        )
