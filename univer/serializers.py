
from rest_framework import serializers
from .models import Faculty,Student,Teacher,Dean,Lectures,Lessons,Practice,Post
from django.contrib.auth.models import User


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields = '__all__'
        
    def create(self,validated_date):
        user=User.objects.create_user(**validated_date)
        user.is_active=True
        user.save()
        return user

class DeanSerializers(serializers.ModelSerializer):
    class Meta:
        model=Dean
        fields = ["name","education"]
        
class FacultySerializers(serializers.ModelSerializer):
    dean = DeanSerializers(read_only=True)
    class Meta:
        model=Faculty
        fields=["name","dean"]
        
        
class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'    
            
class LessonsSerializers(serializers.ModelSerializer):
    '''teacher = TeacherSerializers(read_only=True)'''
    
    faculty = serializers.CharField(source="faculty.name",read_only=True)
    class Meta:
        model=Lessons
        fields=["title","description","faculty"]  
    '''def get_teacher_name(slef,obj):
        return obj.teacher.name'''
    '''def get_lessons(self,obj):
        return Teacherserializers(obj.Lessons.all(),many=True).data'''
           
class TeacherLessonsSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Lessons
        fields = ["title"]   


class LecturesSerializers(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source = "teacher.name",read_only=True)
    lesson_name = serializers.CharField(source = "lessons_name.title", read_only = True) 
    class Meta:
        model=Lectures
        fields=["teacher_name","lesson_name","time","room"]
class PracticeSerializers(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source = "teacher.name",read_only=True)
    practice_name = serializers.CharField(source = "lesson_name.title", read_only = True)
    class Meta:
        model=Practice
        fields = ["teacher_name","practice_name","time","room"]

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = '__all__'
        
 