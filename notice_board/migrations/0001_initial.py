# Generated by Django 4.2.1 on 2023-12-18 04:57

from django.db import migrations, models
import django.db.models.deletion
import notice_board.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(help_text='Student ID', unique=True)),
                ('name', models.CharField(help_text='Name', max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('division', models.CharField(help_text='front or back or admin', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('week_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, related_name='weeks', to='notice_board.user')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_title', models.CharField(help_text='notice_title', max_length=100)),
                ('notice_comment', models.TextField(help_text='notice_comment')),
                ('notice_time', models.DateTimeField()),
                ('file', models.FileField(upload_to='notice/')),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, related_name='notices', to='notice_board.user')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment_title', models.CharField(help_text='assignment_title', max_length=100)),
                ('submission_status', models.CharField(choices=[('T', 'Submitted'), ('F', 'Not Submitted'), ('L', 'Late')], max_length=1)),
                ('file', models.FileField(upload_to=notice_board.models.upload_to_assignments)),
                ('submission_time', models.DateTimeField()),
                ('week_id', models.ForeignKey(db_column='week_id', on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='notice_board.week')),
            ],
        ),
    ]