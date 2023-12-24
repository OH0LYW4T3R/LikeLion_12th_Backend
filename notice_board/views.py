from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

import os
import shutil
from django.conf import settings

from .serializers import UserSerializer, WeekSerializer, AssignmentSerializer, NoticeSerializer
from .models import User, Week, Assignment, Notice

from datetime import datetime

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        queryset = User.objects.filter(student_id=student_id)

        if queryset.exists():
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail : Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

class WeekViewset(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer

    def retrieve(self, request, *args, **kwargs):
        print(request.data.get('student_id'))
        #나중엔 세션아이디로
        user = User.objects.filter(student_id=request.data.get('student_id'))

        if user.exists():
            user_division = user[0].division
            user_id = user[0].id

            if user_division == "front admin" or user_division == "back admin":
                weekset = Week.objects.filter(weeks=kwargs.get('pk'))
                serializer = self.get_serializer(weekset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                weekset = Week.objects.filter(weeks=kwargs.get('pk'), user_id=user_id)
                serializer = self.get_serializer(weekset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail : User not Found or User Logout"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *arg, **kwargs):
        #테스트 시에만 사용
        user = User.objects.filter(student_id=request.data.get('student_id'))

        #실사용시 세션을 넘겨받고 세션디비에서 찾고 학번 얻어야함.
        if user.exists():
            user_division = user[0].division
            assignment_type = request.data.get('assignment_type')

            if user_division == "front admin":
                if(assignment_type == "C"):
                    all_user = User.objects.exclude(division__in=["front admin", "back admin"])
                elif(assignment_type == "F"):
                    all_user = User.objects.exclude(division__in=["front admin", "back admin", 'back'])
                else:
                    return Response({"detail : Your not back admin"}, status=status.HTTP_401_UNAUTHORIZED)
                weeks = request.data.get('weeks')
                assignment_title = request.data.get('assignment_title')
                deadline = request.data.get('deadline')
                week_check = Week.objects.filter(weeks=weeks, assignment_type=assignment_type)

                if not week_check.exists():
                    for u in all_user:
                        Week.objects.create(user_id=u, weeks=weeks, assignment_title = assignment_title, assignment_type=assignment_type, deadline = deadline, submission_status="F")
                    return Response({"detail : Create Week"}, status=status.HTTP_200_OK) 
                else:
                    return Response({"detail : Already Create Week"}, status=status.HTTP_400_BAD_REQUEST) 
            elif user_division == "back admin":
                if(assignment_type == "C"):
                    all_user = User.objects.exclude(division__in=["front admin", "back admin"])
                elif(assignment_type == "B"):
                    all_user = User.objects.exclude(division__in=["front admin", "back admin", 'front'])
                else:
                    return Response({"detail : Your not front admin"}, status=status.HTTP_401_UNAUTHORIZED)
                weeks = request.data.get('weeks')
                assignment_title = request.data.get('assignment_title')
                deadline = request.data.get('deadline')
                week_check = Week.objects.filter(weeks=weeks, assignment_type=assignment_type)

                if not week_check.exists():
                    for u in all_user:
                        Week.objects.create(user_id=u, weeks=weeks, assignment_title = assignment_title, assignment_type=assignment_type, deadline = deadline, submission_status="F")
                    return Response({"detail : Create Week"}, status=status.HTTP_200_OK) 
                else:
                    return Response({"detail : Already Create Week"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail : Your not admin"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail : User not Found or User Logout"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, *args, **kwargs):
        # week_id = kwargs.get('pk')  # 동적 세그먼트 값 가져오기
        user = User.objects.filter(student_id=request.data.get('student_id'))

        #실사용시 세션을 넘겨받고 세션디비에서 찾고 학번 얻어야함.

        if user.exists():
            user_division = user[0].division

            # 여기서 프론트엔드에서 
            if user_division == "front admin" or user_division == "back admin":
                weeks = kwargs.get('pk')

                if user_division == "front admin":
                    week_check = Week.objects.filter(weeks=weeks, assignment_type__in=["F", "C"])

                    if week_check.exists():
                        Week.objects.filter(weeks=weeks, assignment_type__in=["F", "C"]).delete()
                        return Response({"detail : Delete Week"}, status=status.HTTP_200_OK) 
                    else:
                        return Response({"detail : Already Delete Week or Your not same type"}, status=status.HTTP_400_BAD_REQUEST) 
                elif user_division == "back admin":
                    week_check = Week.objects.filter(weeks=weeks, assignment_type__in=["B", "C"])
                   
                    if week_check.exists():
                        Week.objects.filter(weeks=weeks, assignment_type__in=["B", "C"]).delete()
                        return Response({"detail : Delete Week"}, status=status.HTTP_200_OK) 
                    else:
                        return Response({"detail : Already Delete Week or Your not same type"}, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({"detail : Your not admin"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail : User not Found or User Logout"}, status=status.HTTP_404_NOT_FOUND)


class AssignmentViewset(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def retrieve(self, request, *args, **kwargs):
        #나중엔 세션아이디로
        user = User.objects.filter(student_id=request.data.get('student_id'))

        if user.exists():
            user_id = user[0].id
            assignmentset = Assignment.objects.filter(weeks=kwargs.get('pk'), student_id=request.data.get('student_id'))

            if assignmentset.exists():
                serializer = self.get_serializer(assignmentset, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail : Not exist Assignment in week"}, status=status.HTTP_404_NOT_FOUND)    
        else:
            return Response({"detail : User not Found or User Logout"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *arg, **kwargs):
        #week_id 정해줘야함
        user = User.objects.filter(student_id=request.data.get('student_id'))

        if user.exists():
            user_id = user[0].id #id 추출
            weeks = request.data.get('weeks')

            week = Week.objects.filter(user_id=user_id, weeks=weeks)

            if week.exists():
                week_id = week[0].week_id

                use_data = {
                    "student_id" : request.data.get('student_id'),
                    "week_id" : week_id,
                    "weeks" : week[0].weeks,
                    "assignment_title" : request.data.get('assignment_title'),
                    "file" : request.data.get('file')
                }

                serializer = self.get_serializer(data=use_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)

                submission_time = serializer.data.get('submission_time')
                week_deadline = week[0].deadline

                assignment_count = Assignment.objects.filter(week_id=week_id).count()
                
                if(assignment_count > 0):
                    if datetime.fromisoformat(str(submission_time)) > datetime.fromisoformat(str(week_deadline)):
                        week.update(submission_status="L")
                    else:
                        week.update(submission_status="T")

                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({"detail": "Week not Create"}, status=status.HTTP_404_NOT_FOUND)    
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    #update 어차피 과제 업데이트는 사용자가 해당 과제를 눌렀을때 프론트에서 과제 아이디를 알고있기 때문에
        
    # 세션 받아서 학번알고, 프론트에서 weeks 받아야함
    def destroy(self, request, *args, **kwargs):
        # 그리고 url에 주차가 들어가야함
        # 로그인된 사람의 학번과 주차를 넘겨받아야함.
        # instance = self.get_object()
        # 그냥 instance시 -> Assignment Object
        # instance.week_id -> 한칸 상승 Week Object
        # week_id = instance.week_id.week_id

        #예외처리 해야함 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print("call")
        weeks = kwargs.get('pk')
        student_id=request.data.get('student_id')

        assignment_instance = Assignment.objects.filter(weeks=weeks, student_id=student_id)

        if assignment_instance.exists():
            week_id = assignment_instance[0].week_id.week_id
            file_name = str(assignment_instance[0].file)
            Assignment.objects.filter(week_id=week_id).delete()

            file_path = os.path.join(settings.MEDIA_ROOT, f'assignments\{student_id}\{weeks}')

            if os.path.exists(file_path):
                print(file_path)
                shutil.rmtree(file_path)

            week = Week.objects.filter(week_id=week_id)
            # self.perform_destroy(instance)

            assignment_count = Assignment.objects.filter(week_id=week_id).count()

            if(assignment_count < 1):
                week.update(submission_status="F")

            return Response({"detail": "Delete Success"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail : Already Delete or Not found Assignment"}, status=status.HTTP_404_NOT_FOUND)

class NoticeViewset(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    
    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)
        # Request Data: <QueryDict: {'student_id': ['20201919'], 'notice_title': ['test'], 'notice_comment': ['test'], 'file': ['test.txt']}>
        # 사용법 : student_id = request.data.get('student_id') 추출

        # 나중엔 세션값으로 넘겨받을거라 세션으로 유저를 추출하는 로직으로 짜야함

        user = User.objects.filter(student_id=request.data.get('student_id'))

        if user.exists():
            student_id = request.data.get('student_id')
            user_id = user[0].id #id 추출
            division = user[0].division

            if division == "front admin" or division == "back admin": # 운영진만 공지사항 쓰도록 함.

                if not request.FILES.get('file'):
                    use_data = {
                        "user_id" : user_id,
                        "notice_title" : request.data.get('notice_title'),
                        "notice_comment" : request.data.get('notice_comment'),
                    }
                else:
                    use_data = {
                        "user_id" : user_id,
                        "notice_title" : request.data.get('notice_title'),
                        "notice_comment" : request.data.get('notice_comment'),
                        "file" : request.data.get('file')
                    }

                serializer = self.get_serializer(data=use_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)

                use_data['student_id'] = student_id

                return Response({'detail : Save Success'}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({"detail : Your not admin"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, *args, **kwargs):
        user = User.objects.filter(student_id=request.data.get('student_id'))

        if user.exists():
            use_data = {
                "user_id" : user[0].id,
                "notice_title" : request.data.get('notice_title'),
                "notice_comment" : request.data.get('notice_comment'),
                "file" : request.data.get('file')
            }
            partial = kwargs.pop('partial', False)
            instance = self.get_object()

            file_path = os.path.join(settings.MEDIA_ROOT, str(instance.file))

            if os.path.exists(file_path):
                os.remove(file_path)

            serializer = self.get_serializer(instance, data=use_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, *args, **kwargs):
        user = User.objects.filter(student_id=request.data.get('student_id'))

        if user.exists():
            division = user[0].division

            if(division == "front admin" or division == "back admin"):
                instance = self.get_object()
                self.perform_destroy(instance)
                file_path = os.path.join(settings.MEDIA_ROOT, str(instance.file))

                if os.path.exists(file_path) and (file_path != (settings.MEDIA_ROOT + '\\')):
                    os.remove(file_path)

                return Response({"detail : Success deletion"}, status=status.HTTP_204_NO_CONTENT) 
            else:
                return Response({"detail : Your not admin"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)