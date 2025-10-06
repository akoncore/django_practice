
from rest_framework import serializers
from .models import Faculty,Student,Teacher,Dean,Lectures,Lessons,Practice,Post,Schedule,DAY_CHOICES
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
    lessons_name = serializers.PrimaryKeyRelatedField(
        queryset = Lessons.objects.all(),
        source = 'leacture_name',
        write_only = True,
        allow_null=True,
        required = False
    )
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset = Teacher.objects.all(),
        source = 'teacher_name',
        write_only=True,
        allow_null = True,
        required = False
    )
    class Meta:
        model=Lectures
        fields=["teacher_name","lesson_name","time","room","day","lessons_name","teacher_id"]
        

class StudentSerializers(serializers.ModelSerializer):
    faculty = serializers.CharField(source = "faculty.name",read_only=True)
    faculties = FacultySerializers(read_only = True)
    class Meta:
        model = Student
        fields = ["name","type_of_student","faculty","faculties"]

class PracticeSerializers(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only=True)
    teacher_name = serializers.CharField(source = "teacher.name",read_only=True)
    practices_name = serializers.CharField(source = "lesson_name.title", read_only = True)
    practice_name = LessonsSerializers(read_only=True)
    practice_id = serializers.PrimaryKeyRelatedField(
        queryset = Lessons.objects.all(),
        source = 'practice_name',
        write_only = True,
        allow_null=True,
        required = False
    )
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset = Teacher.objects.all(),
        source = 'teacher_name',
        write_only=True,
        allow_null = True,
        required = False
    )
    class Meta:
        model=Practice
        fields = ["teacher_name","practices_name","time","room","day","practice_name","practice_id","teacher_id","day_display"]

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = '__all__'
        
 


class ScheduleSerializer(serializers.ModelSerializer):
    weekly_schulde = serializers.SerializerMethodField()
    
    class Meta:
        model = Schedule
        fields = ["weekly_schulde"]
        
    def get_weekly_schulde(self,obj):
        week_days = dict(DAY_CHOICES)
        schulde_by_day = {}
        
        for key,lavel in week_days.items():
            practices = obj.practice.filter(day = key)
            lectures = obj.lecture.filter(day=key)
            if practices.exists() or lectures.exists():
                schulde_by_day[lavel] = {
                    "practices":PracticeSerializers(practices,many=True).data,
                    "lectures": LecturesSerializers(lectures,many=True).data
                }
        return schulde_by_day
    
        
 