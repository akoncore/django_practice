from django.contrib import admin

from .models import Dean,Faculty,Lessons,Student,Teacher,Lectures,Practice,Post,Schedule

# Register your models here# .

@admin.register(Dean) # type: ignore
class DeanAdmin(admin.ModelAdmin):
    list_display = ("id","name","education",)
    list_display_links = ("name",)
    list_filter = ("education",)

    

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display=("id","name","dean",)
    list_display_links=("name",)
    list_editable =("dean",)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id","name","education","experience","teacher_type",)
    list_display_links = ("name",)
    list_filter = ("name",)
    
@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ("title","description","faculty",)
    list_display_links = ("title",)


@admin.register(Lectures)
class LecturesAdmin(admin.ModelAdmin):
    list_display = ("lessons_name","teacher","day","time","room",)
    list_display_links = ("lessons_name",)
    list_editable = ("time","room",)
    list_filter = ("day","lessons_name",)
    ordering = ("time",)
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name","type_of_student","faculty",)
    list_display_links = ("name",)
    list_filter = ("name",)

@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ("lesson_name","teacher","day","time","room",)
    list_display_links = ("lesson_name",)
    list_filter = ("day","lesson_name",)
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","content","author_type",)
    list_filter = ("author_type",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("get_practice","get_lecture",)
    
    def get_practice(self,obj):
        return " ".join([f"{p.lesson_name} {p.teacher} П {p.room} ({p.day},{p.time})" for p in obj.practice.all()])
    get_practice.short_description = "Practices"
    
    def get_lecture(self,obj):
        return " ".join([f"{p.lessons_name} {p.teacher} Л{p.room} ({p.day},{p.time})" for p in obj.lecture.all()])
    get_lecture.short_description = "Lectures"
    