# Generated by Django 4.0.5 on 2023-06-23 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0008_recruiter_groups_recruiter_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissions',
            name='S_ConsultantId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp1.consultant'),
        ),
    ]
