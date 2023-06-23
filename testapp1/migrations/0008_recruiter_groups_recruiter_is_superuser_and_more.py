# Generated by Django 4.0.5 on 2023-06-13 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('testapp1', '0007_remove_recruiter_r_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiter',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='recruiters', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='recruiter',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='recruiter',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='recruiters', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
