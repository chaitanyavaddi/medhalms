from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('subdomain', models.CharField(max_length=100, unique=True)),
                ('bio', models.TextField(blank=True, default='')),
                ('brand_primary', models.CharField(blank=True, default='#3730a3', max_length=20)),
                ('brand_secondary', models.CharField(blank=True, default='#2a6e96', max_length=20)),
                ('custom_domain', models.CharField(blank=True, max_length=255)),
                ('custom_domain_verified', models.BooleanField(default=False)),
                ('avatar', models.URLField(blank=True)),
                ('logo_display', models.CharField(
                    choices=[('avatar', 'Avatar'), ('avatar_name', 'Avatar + Name'), ('name', 'Name')],
                    default='name', max_length=20,
                )),
                ('nav_sticky', models.CharField(
                    choices=[('none', 'No sticky'), ('always', 'Sticky'), ('desktop', 'Desktop only'), ('mobile', 'Mobile only')],
                    default='always', max_length=20,
                )),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrgMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(
                    choices=[('owner', 'Owner'), ('editor', 'Editor'), ('viewer', 'Viewer')],
                    default='owner', max_length=20,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='orgs.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('org', 'user')},
            },
        ),
        migrations.AddIndex(
            model_name='orgmember',
            index=models.Index(fields=['org', 'role'], name='orgmember_org_role_idx'),
        ),
        migrations.AddIndex(
            model_name='orgmember',
            index=models.Index(fields=['user', 'org'], name='orgmember_user_org_idx'),
        ),
    ]
