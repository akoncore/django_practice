from django.shortcuts import render
from rest_framework import viewsets,status
from .models import Faculty,Student,Teacher,Dean,Lectures,Lessons,Practice,Post
from rest_framework import permissions
from .serializers import (RegisterSerializers, DeanSerializers,FacultySerializers,PostSerializers,
FacultySerializers,LessonsSerializers,TeacherSerializers,TeacherLessonsSerializers)

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
        data = [{"id": p.id, "title": p.title,"content":p.content} for p in posts]
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
    
        for lesson in lessons:
            lesson.counter += 1
            lesson.save()
            total_counter +=1
        
        
        return Response(total_counter)
        
        
    
    

        
    
    
    

    
