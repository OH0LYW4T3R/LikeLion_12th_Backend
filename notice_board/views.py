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

        print(user_instance.student_id)

        # 모델 수정시 student -> user로 변경
        user_week = Week.objects.filter(user_id=user_instance)

        #Week.student_id(User로 상승)
        week_data = [{"week_id": Week.id, "week" : Week.weeks, "student_id": user_instance.student_id} for Week in user_week]
        Week.objects.bulk_create([user_instance.week_set.create(**entry) for entry in week_data])


        user_notices = Notice.objects.filter(user_id=user_instance)
        notice_data = [
            {
                "id": notice.id, 
                "user_id" : notice.user_id.id,
                "student_id" : notice.user_id.student_id,
                "notice_title" : notice.notice_title,
                "notice_comment" : notice.notice_comment,
                "notice_time" : notice.notice_time,
                "file" : notice.file
            } 
            for notice in user_notices
        ]
        Notice.objects.bulk_create([user_instance.notice_set.create(**entry) for entry in notice_data])


    def get_serializer_class(self):
        # POST 요청 시에는 UserSerializer를 사용
        if self.action == 'create':
            return UserSerializer
        # 나머지 요청 시에는 기본 UserSerializer를 사용
        return UserSerializer

class WeekViewset(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer

    def perform_create(self, serializer):
        #이부분 고쳐야함
        #학번이랑 주차정보 있어야함
        week_instance = serializer.save()
        #week_id를 동적으로 찾을 수 잇어야함
        user_assignment = Assignment.objects.filter(week_id=week_instance.week_id)
        
        assignment_data = [
            {
                "weeks" : assignment.weeks,
                "student_id" : assignment.week_id.user_id.student_id, # 학번도 내가 찾아서 넣어줘야함.
                "assignment_id" : assignment.assignment_id,
                "assignment_title" : assignment.assignment_title,
                "submission_status" : assignment.submission_status,
                "file" : assignment.file,
                "submission_time" : assignment.submission_time
            }
            for assignment in user_assignment
        ]

        Assignment.objects.bulk_create([week_instance.assignment_set.create(**entry) for entry in assignment_data])

class AssignmentViewset(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    
class NoticeViewset(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
