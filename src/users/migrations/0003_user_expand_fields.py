from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(
                blank=True,
                choices=[
                    ('male', 'Male'),
                    ('female', 'Female'),
                    ('non_binary', 'Non-binary'),
                    ('prefer_not_say', 'Prefer not to say'),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(
                choices=[
                    ('active', 'Active'),
                    ('inactive', 'Inactive'),
                    ('pending', 'Pending'),
                ],
                default='active',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('student', 'Student'),
                    ('trainer', 'Trainer'),
                    ('admin', 'Admin'),
                ],
                default='student',
                max_length=20,
            ),
        ),
    ]
