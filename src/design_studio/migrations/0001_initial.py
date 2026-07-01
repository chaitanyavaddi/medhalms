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
            name='DesignProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Full brief shown to the student in the workspace.')),
                ('tags', models.CharField(blank=True, help_text='Comma-separated e.g. landing-page, ecommerce', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='design_projects_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DesignSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grapes_data', models.JSONField(default=dict)),
                ('html_snapshot', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('in_progress', 'In Progress'), ('submitted', 'Submitted')], default='in_progress', max_length=15)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('submitted_at', models.DateTimeField(null=True, blank=True)),
                ('last_saved_at', models.DateTimeField(null=True, blank=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='design_studio.designproject')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='design_submissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-started_at'],
                'unique_together': {('project', 'student')},
            },
        ),
    ]
