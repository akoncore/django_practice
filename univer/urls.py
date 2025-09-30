
from django.urls import path,include
from rest_framework import routers
from .views import DeanView,RegisterView,FacultyView,LessonsView,TeacherView


router = routers.DefaultRouter()
router.register(r'dean',DeanView,basename='dean')
router.register(r'register',RegisterView)
router.register(r'faculty',FacultyView)
router.register(r'lessons',LessonsView)
router.register(r'teacher',TeacherView)


urlpatterns=[
    path('',include(router.urls)),
    
]


