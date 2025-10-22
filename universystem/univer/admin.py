from django.contrib import admin

from .models import Dean,Faculty,Lessons,Student,Teacher,Lectures,Practice,Post,Schedule

# Register your models here# .
@admin.register(Dean)
class DeanAdmin(admin.ModelAdmin):
    list_display = ("name","education",)
    list_display_links = ("name",)
    list_filter = ("education",)

