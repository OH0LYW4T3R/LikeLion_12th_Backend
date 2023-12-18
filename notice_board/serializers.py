from django.contrib.auth.models import Group

from .models import User, Week, Assignment, Notice
from rest_framework import serializers

class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    week = WeekSerializer(many=True, read_only=True, source='weeks')

    class Meta:
        model = User
        fields = ['id', 'student_id', 'name', 'email', 'division', 'week']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"
    
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"