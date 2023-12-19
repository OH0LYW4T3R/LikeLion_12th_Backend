from django.contrib.auth.models import Group

from .models import User, Week, Assignment, Notice
from rest_framework import serializers

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"

class WeekSerializer(serializers.ModelSerializer):
    # 이친구 이름을 필드에 넣어줘야함
    assignment = AssignmentSerializer(many=True, read_only=True, source='assignments')

    class Meta:
        model = Week
        fields = ['user_id', 'week_id', 'weeks', 'assignment']

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ["id", "user_id", "notice_title", "notice_comment", "notice_time", "file"]

class UserSerializer(serializers.ModelSerializer):
    week = WeekSerializer(many=True, read_only=True, source='weeks')
    notice = NoticeSerializer(many=True, read_only=True, source='notices')

    class Meta:
        model = User
        fields = ['id', 'student_id', 'name', 'email', 'division', 'week', 'notice']
    
