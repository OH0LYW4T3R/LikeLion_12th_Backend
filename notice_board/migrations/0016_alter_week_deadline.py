# Generated by Django 5.0 on 2023-12-23 12:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice_board', '0015_week_deadline_alter_assignment_submission_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
