# from django.db import models

# # Create your models here.


from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_id = models.IntegerField(help_text="Student ID", unique=True)
    name = models.CharField(help_text="Name", max_length=100)
    email = models.EmailField()
    division = models.CharField(help_text="front or back or admin", max_length=100)

class Week(models.Model):
    user_id = models.ForeignKey(User, related_name="weeks", on_delete=models.CASCADE, db_column="user_id")
    week_id = models.AutoField(primary_key=True)
    weeks = models.IntegerField(help_text="Weeks")

def upload_to_assignments(instance, filename):
    return f'assignments/{instance.week_id.user_id.student_id}/{instance.week_id.weeks}/{filename}'

class Assignment(models.Model):
    # week_id = models.ForeignKey(Week, related_name="assignments", on_delete=models.CASCADE, db_column="week_id")
    student_id = models.IntegerField(help_text="Student ID")
    week_id = models.ForeignKey(Week, related_name="assignments", on_delete=models.CASCADE, db_column="week_id") # related_name => 역참조시 필요
    weeks = models.IntegerField(help_text="Weeks")
    assignment_id = models.AutoField(primary_key=True)
    assignment_title = models.CharField(help_text="assignment_title", max_length=100)
    # 추후 submission_status == "Submitted"로 사용
    submission_status = models.CharField(max_length=1, choices=[('T', 'Submitted'), ('F', 'Not Submitted'), ('L', 'Late')])
    file = models.FileField(upload_to=upload_to_assignments)
    submission_time = models.DateTimeField()

class Notice(models.Model):
    user_id = models.ForeignKey(User, related_name="notices", on_delete=models.CASCADE, db_column="user_id")
    student_id = models.IntegerField(help_text="Student ID", unique=True)
    notice_title = models.CharField(help_text="notice_title", max_length=100)
    notice_comment = models.TextField(help_text="notice_comment")
    notice_time = models.DateTimeField()
    file = models.FileField(upload_to='notice/')
