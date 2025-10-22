
from django.urls import path,include
from rest_framework import routers
from .views import DeanView,RegisterView,FacultyView,LessonsView,TeacherView,StudentView,PracticeView,LecturesView,ScheduleView


router = routers.DefaultRouter()
router.register(r'dean',DeanView,basename='dean')
router.register(r'register',RegisterView)
router.register(r'faculty',FacultyView)
router.register(r'lessons',LessonsView)
router.register(r'teacher',TeacherView)
router.register(r'student',StudentView)
router.register(r'practice',PracticeView)
router.register(r'lecture',LecturesView)
router.register(r'schedule',ScheduleView)


urlpatterns=[
    path('',include(router.urls)),
    
]


