from django.shortcuts import render
from rest_framework import permissions, viewsets

from .serializers import UserSerializer, WeekSerializer, AssignmentSerializer, NoticeSerializer
from .models import User, Week, Assignment, Notice

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # User 객체를 생성한 후 Week 객체를 연결
        user_instance = serializer.save()
        week_data = [{"week_id": i, "student_id": user_instance.id} for i in range(1, user_instance.week_count + 1)]
        Week.objects.bulk_create([user_instance.week_set.create(**entry) for entry in week_data])

    def get_serializer_class(self):
        # POST 요청 시에는 UserSerializer를 사용
        if self.action == 'create':
            return UserSerializer
        # 나머지 요청 시에는 기본 UserSerializer를 사용
        return UserSerializer

class WeekViewset(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer

class AssignmentViewset(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    
class NoticeViewset(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
