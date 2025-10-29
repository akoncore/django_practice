from django.shortcuts import render
from rest_framework import viewsets,status
from .models import Faculty,Student,Teacher,Dean,Lectures,Lessons,Practice,Post,Schedule,DAY_CHOICES
from rest_framework import permissions
from .serializers import (RegisterSerializers, DeanSerializers,FacultySerializers,PostSerializers,
FacultySerializers,LessonsSerializers,TeacherSerializers,TeacherLessonsSerializers,LecturesSerializers,
PracticeSerializers,StudentSerializers,ScheduleSerializer)

from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
# Create your views here.

class RegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeanView(viewsets.ModelViewSet):
    queryset = Dean.objects.all()
    serializer_class = DeanSerializers
    
    @action(detail=True, methods=['get'])
    def teacher_or_not(self,request,pk=None):
        dean=self.get_object()
        return Response({"id":dean.id, "is_teacher":dean.is_teacher})
    
    @action(detail=True, methods=["get"])
    def posts(self, request, pk=None):
        dean = self.get_object()
        posts = dean.dean_posts.all() 
        data = [{"id": p.id, "title": p.title,} for p in posts]
        return Response(data)
    
    @action(detail=True,methods=["get"])
    def faculty(self,request,pk=None):
        dean = self.get_object()
        faculty = dean.faculty
        return Response({"name":faculty.name})
  
        
class FacultyView(viewsets.ModelViewSet):
    queryset=Faculty.objects.all()
    serializer_class = FacultySerializers
    
    
    @action(detail=True,methods=["get"])
    def dean(self,request,pk=None):
        faculty = self.get_object()
        dean = faculty.dean
        return Response({"dean_name":dean.name})


class LessonsView(viewsets.ModelViewSet):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializers
    
    @action(detail=True,methods=["get"])
    def teacher(self, request, pk=None):
        lessons = self.get_object()
        teacher = lessons.teacher
        return Response({
        "About teacher": teacher.name,
        "teacher education": teacher.education})
        
        
class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializers
    
    @action(detail = True , methods = ["get"])
    def lessons(self,request,pk=None):
        teacher = self.get_object()
        lessons = teacher.lessons.all()
        serializer = TeacherLessonsSerializers(lessons,many=True)
        return Response(serializer.data)
    
    
    @action(detail = True , methods = ["get"])
    def counter(self,request,pk=None):
        counter = 0
        total_counter = 0
        teacher = self.get_object()
        lessons = teacher.lessons.all()
    
        total_counter = lessons.count()
        
        return Response({"You have":total_counter})
        
    
    @action(detail = True, methods = ["get"])
    def schedule(self,request,pk=None):
        teachers = self.get_object()
        lecture = teachers.lecture.all()
        practice = teachers.practice.all()
        serializer = LecturesSerializers(lecture,many=True)
        serializer1 = PracticeSerializers(practice,many=True)
        
        return Response({
            "lecture":serializer.data,
            "practice":serializer1.data
        })
        

class StudentView (viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializers
    
    
class PracticeView(viewsets.ModelViewSet):
    queryset = Practice.objects.all()
    serializer_class = PracticeSerializers
    
    def list(self,request):
        week_days = dict(DAY_CHOICES)
        week_schulde = {}
        
        all_practices = Practice.objects.all()
        
        for key,lavel in week_days.items():
            practices = all_practices.filter(day = key)
            
            if practices.exists():
                week_schulde[lavel]={
                    "Practices":PracticeSerializers(practices,many=True).data
                }
        return Response(week_schulde)      
    
    @action(detail=True , methods = ["get"])
    def students(self,request,pk=None):
        practices = self.get_object()
        students = practices.students.all()
        serializer = StudentSerializers(students, many=True)
        return Response(serializer.data)
    
   
class LecturesView(viewsets.ModelViewSet):
    queryset = Lectures.objects.all()
    serializer_class = LecturesSerializers
    

class ScheduleView(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    
    def list(self,request,*args,**kwargs):
        week_days = dict(DAY_CHOICES)
        week_schedule = {}
        
        all_practice = Practice.objects.all()
        all_lectures = Lectures.objects.all()
        
        for key,lavel in week_days.items():
            practices = all_practice.filter(day=key)
            lectures = all_lectures.filter(day=key)
            
            if practices.exists() or lectures.exists():
                week_schedule[lavel]={
                    "practices":PracticeSerializers(practices,many=True).data,
                    "lectures":LecturesSerializers(lectures,many=True).data
                }
        return Response(week_schedule)
    
    