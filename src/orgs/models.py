from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Organization(models.Model):
    name            = models.CharField(max_length=200)
    subdomain       = models.CharField(max_length=100, unique=True)
    bio             = models.TextField(blank=True, default='')
    brand_primary   = models.CharField(max_length=20, blank=True, default='#3730a3')
    brand_secondary = models.CharField(max_length=20, blank=True, default='#2a6e96')
    custom_domain        = models.CharField(max_length=255, blank=True)
    custom_domain_verified = models.BooleanField(default=False)
    avatar          = models.URLField(blank=True)
    logo_display    = models.CharField(max_length=20, default='name', choices=[
        ('avatar',      'Avatar'),
        ('avatar_name', 'Avatar + Name'),
        ('name',        'Name'),
    ])
    nav_sticky      = models.CharField(max_length=20, default='always', choices=[
        ('none',    'No sticky'),
        ('always',  'Sticky'),
        ('desktop', 'Desktop only'),
        ('mobile',  'Mobile only'),
    ])
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrgMember(models.Model):
    class Role(models.TextChoices):
        OWNER  = "owner",  "Owner"
        EDITOR = "editor", "Editor"
        VIEWER = "viewer", "Viewer"

    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="org_memberships")
    org        = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    role       = models.CharField(max_length=20, choices=Role.choices, default=Role.OWNER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("org", "user")
        indexes = [
            models.Index(fields=['org', 'role'], name='orgmember_org_role_idx'),
            models.Index(fields=['user', 'org'], name='orgmember_user_org_idx'),
        ]

    def __str__(self):
        return f"{self.user} → {self.org} ({self.role})"


@receiver(post_save, sender=Organization)
def _on_org_save(sender, instance, **kwargs):
    from core.cloudflare import purge_org_cache
    purge_org_cache(instance)
