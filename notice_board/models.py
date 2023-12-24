# from django.db import models

# # Create your models here.
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_id = models.IntegerField(help_text="Student ID", unique=True)
    name = models.CharField(help_text="Name", max_length=100)
    email = models.EmailField()
    division = models.CharField(help_text="front or back or admin(front admin or back admin)", max_length=100)

class Week(models.Model):
    user_id = models.ForeignKey(User, related_name="weeks", on_delete=models.CASCADE, db_column="user_id")
    week_id = models.AutoField(primary_key=True)
    weeks = models.IntegerField(help_text="Weeks")
    assignment_title = models.CharField(help_text="assignment_title", max_length=100)
    assignment_type = models.CharField(max_length=1, choices=[('C', 'Common'), ('F', 'Frontend'), ('B', 'Backend')])
    deadline = models.DateTimeField() # default=timezone.now
    submission_status = models.CharField(max_length=1, choices=[('T', 'Submitted'), ('F', 'Not Submitted'), ('L', 'Late')])

def upload_to_assignments(instance, filename):
    return f'assignments/{instance.week_id.user_id.student_id}/{instance.week_id.weeks}/{filename}'

class Assignment(models.Model):
    # week_id = models.ForeignKey(Week, related_name="assignments", on_delete=models.CASCADE, db_column="week_id")
    student_id = models.IntegerField(help_text="Student ID")
    week_id = models.ForeignKey(Week, related_name="assignments", on_delete=models.CASCADE, db_column="week_id") # related_name => 역참조시 필요
    weeks = models.IntegerField(help_text="Weeks")
    assignment_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=upload_to_assignments, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'hwp'])])
    submission_time = models.DateTimeField(default=timezone.now) # default=timezone.now

class Notice(models.Model):
    user_id = models.ForeignKey(User, related_name="notices", on_delete=models.CASCADE, db_column="user_id")
    notice_title = models.CharField(help_text="notice_title", max_length=100)
    notice_comment = models.TextField(help_text="notice_comment")
    notice_time = models.DateTimeField(default=timezone.now) # default=timezone.now
    file = models.FileField(upload_to='notice/')
