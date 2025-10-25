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
    list_display = ("title","description","faculty","teacher",)
    list_display_links = ("title",)
