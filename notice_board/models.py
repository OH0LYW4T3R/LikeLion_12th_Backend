# from django.db import models

# # Create your models here.

# class User(models.Model):
#     student_id = models.IntegerField(help_text="Student ID", unique=True)
#     name = models.CharField(help_text="Name", max_length=100)
#     email = models.EmailField()
#     division = models.CharField(help_text="front or back or admin", max_length=100)
#     # week_id = models.BigAutoField(help_text="Week ID")
#     # post_id = models.BigAutoField(help_text="Post ID")
#     # notice_id = models.BigAutoField(help_text="Notice ID")

# class Notice(models.Model):
#     student_id = models.ForeignKey("User", related_name="week", on_delete=models.CASCADE, db_column="student_id")
#     notice_id = models.AutoField()
#     notice_title = models.CharField(help_text="notice_title", max_length=100)
#     notice_comment = models.TextField(help_text="notice_comment")
#     notice_time = models.DateTimeField()
#     file = models.FileField(upload_to='notice/')

# class Week(models.Model): # 주차 DB
#     student_id = models.ForeignKey("User", related_name="week", on_delete=models.CASCADE, db_column="student_id")

#     week_id = models.AutoField(primary_key=True)

# def upload_to_assignments(instance, filename):
#     return f'assignments/{instance.week_id.student_id.student_id}/{instance.week_id.week_id}/{filename}'

# class Assignment(models.Model): # 과제 DB
#     week_id = models.ForeignKey(Week, related_name="assignment", on_delete=models.CASCADE, db_column="week_id")

#     assignment_id = models.AutoField(primary_key=True)
#     assignment_title = models.CharField(help_text="assignment_title", max_length=100)
#     submission_status = models.CharField(max_length=1, choices=[('T', 'Submitted'), ('F', 'Not Submitted'), ('L', 'Late')]) # submission_status == 'Submitted'
#     file = models.FileField(upload_to=upload_to_assignments)
#     submission_time = models.DateTimeField()

from django.db import models

class User(models.Model):
    student_id = models.IntegerField(help_text="Student ID", unique=True)
    name = models.CharField(help_text="Name", max_length=100)
    email = models.EmailField()
    division = models.CharField(help_text="front or back or admin", max_length=100)

class Week(models.Model):
    student_id = models.ForeignKey(User, related_name="weeks", on_delete=models.CASCADE, db_column="student_id")
    week_id = models.AutoField(primary_key=True)

def upload_to_assignments(instance, filename):
    return f'assignments/{instance.week_id.student_id.student_id}/{instance.week_id.week_id}/{filename}'

class Assignment(models.Model):
    week_id = models.ForeignKey(Week, related_name="assignments", on_delete=models.CASCADE, db_column="week_id")
    assignment_id = models.AutoField(primary_key=True)
    assignment_title = models.CharField(help_text="assignment_title", max_length=100)
    submission_status = models.CharField(max_length=1, choices=[('T', 'Submitted'), ('F', 'Not Submitted'), ('L', 'Late')])
    file = models.FileField(upload_to=upload_to_assignments)
    submission_time = models.DateTimeField()

class Notice(models.Model):
    student_id = models.ForeignKey(User, related_name="notices", on_delete=models.CASCADE, db_column="student_id")
    notice_title = models.CharField(help_text="notice_title", max_length=100)
    notice_comment = models.TextField(help_text="notice_comment")
    notice_time = models.DateTimeField()
    file = models.FileField(upload_to='notice/')
