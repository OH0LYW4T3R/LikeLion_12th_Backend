# Generated by Django 5.0 on 2023-12-19 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice_board', '0011_alter_week_weeks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='student_id',
        ),
    ]
