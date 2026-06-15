from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_managers_alter_user_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_prefix',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
