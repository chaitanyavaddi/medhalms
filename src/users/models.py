from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extras):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user  = self.model(email=email, **extras)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extras):
        extras.setdefault("is_staff", True)
        extras.setdefault("is_superuser", True)
        return self.create_user(email, password, **extras)


class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TRAINER = 'trainer', 'Trainer'
        ADMIN   = 'admin',   'Admin'

    class Gender(models.TextChoices):
        MALE           = 'male',           'Male'
        FEMALE         = 'female',         'Female'
        NON_BINARY     = 'non_binary',     'Non-binary'
        PREFER_NOT_SAY = 'prefer_not_say', 'Prefer not to say'

    class Status(models.TextChoices):
        ACTIVE   = 'active',   'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING  = 'pending',  'Pending'
        BANNED   = 'banned', 'Banned'

    email         = models.EmailField(unique=True)
    first_name    = models.CharField(max_length=100, blank=True)
    last_name     = models.CharField(max_length=100, blank=True)
    gender        = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    avatar        = models.URLField(blank=True)
    phone_prefix  = models.CharField(max_length=10, blank=True)
    phone         = models.CharField(max_length=20, blank=True)
    role          = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    status        = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []
    objects         = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
