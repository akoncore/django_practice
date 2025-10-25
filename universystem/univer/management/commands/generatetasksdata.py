from datetime import datetime
from typing import Any
import random

from random import choice,choices,randint,sample
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from univer.models import (Dean,Faculty
,Teacher,Lessons,Lectures)

class Command(BaseCommand):
    
    EMAIL_DOMAINS = (
        "email.com",
        "mail.ru"
    )
    
    NAME_WORDS = (
        "Болат Алтынбек",
        "Талгат Данияр",
        "Ерлан Алан",
        "Ерлан Асылым"
    )
    FACULTY = (
        "CS",
        "MKM",
        "BIS",
    )
    TEACHER_NAME = (
        "Болат Алтынбек",
        "Талгат Данияр",
        "Ерлан Алан",
        "Ерлан Асылым",
        "Айгерім Нұрлан",
        "Дастан Еркін",
        "Алия Ербол",
        "Самат Жандос",
        "Динара Саясат",
        "Жанель Бекзат",
        "Руслан Әсет",
        "Аружан Мұрат",
        "Мадина Нұрхат",
        "Қайрат Аман",
        "Айдана Талғат",
        "Бекзат Арман",
        "Гүлнұр Ержан",
        "Асқар Бауыржан",
        "Меруерт Самат",
        "Нұрлан Қайрат"
    )
    EDUCATION = (
        "KBTU & SDU",
        "AITU",
        "MUIT",
        "NU"
    )
    
    def __generate_users(self, user_count=20):
        USER_PASSWORD = make_password("12345")
        created_user:list[User] = []
        
        for i in range(user_count):
            username:str = f"user{i+1}"
            email:str =f"user{i+1}@{choice(self.EMAIL_DOMAINS)}"
            created_user.append(
                User(
                    username = username,
                    email = email,
                    password = USER_PASSWORD,
                )
            ) 
        User.objects.bulk_create(created_user,ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Created user"
            )
        )
        
        
    def __generate_dean(self,dean_count = 20):
        created_dean:list[Dean] = []
        
        i:int
        for i in range(dean_count):
            name = " ".join(choices(self.NAME_WORDS,k=1,))
            education = randint(10,15)
            is_teacher = True
            created_dean.append(
                Dean(
                    name = name,
                    education = education,
                    is_teacher = is_teacher
                )
            )
            
            
        Dean.objects.bulk_create(created_dean,ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Created dean"
            )
        )
    
    
    def __generate_faculty(self,faculty_count):
        created_faculty:list[Faculty] = []
        exited_faculty:QuerySet[Dean]=Dean.objects.all()
        
        for i in range(faculty_count):
            name = " ".join(choices(self.FACULTY)).capitalize()
            dean:Dean = choice(exited_faculty)
            created_faculty.append(
                Faculty(
                    name = name,
                    dean = dean
                )
            )
        Faculty.objects.bulk_create(created_faculty,ignore_conflicts=True,unique_fields=["dean",])
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created faculty"
            )
        )
        
    
    def __generate_teacher(self,teacher_count = 20)->None:
        created_teacher:list[Teacher] = []
        
        if teacher_count > len(self.TEACHER_NAME):
            teacher_count = len(self.TEACHER_NAME)
            
        teacher_names = sample(self.TEACHER_NAME , k=teacher_count)
        
        for name in teacher_names:
            education = " ".join(choices(self.EDUCATION,k=1))
            experience = randint(1,20)
            teacher_type = random.choice([choice[0] for choice in Teacher.teacher_type_choices])

            created_teacher.append(
                Teacher(
                    name=name,
                    education = education,
                    experience =experience,
                    teacher_type =teacher_type
                )
            )
        Teacher.objects.bulk_create(created_teacher,ignore_conflicts=True,unique_fields=["name"])
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(teacher_names)} teacher"
            )
        )

    def __generate_lessons(self,lesson_count = 12)->None:
        LESSONS = {
            "Calculus": "Covers differential and integral calculus concepts.",
            "Calculus 2": "Focuses on advanced integration techniques, sequences, and series.",
            "Linear Algebra": "Introduces matrices, determinants, and vector spaces.",
            "Discrete Mathematics": "Studies logic, sets, combinatorics, and graph theory fundamentals.",
            "Probability and Statistics": "Explores data analysis, probability distributions, and hypothesis testing.",
            "Computer Architecture": "Examines CPU structure, memory organization, and low-level hardware design.",
            "Operating Systems": "Covers process management, threads, scheduling, and memory handling.",
            "Data Structures": "Introduces arrays, linked lists, trees, graphs, and algorithmic complexity.",
            "Algorithms": "Focuses on algorithm design paradigms such as divide and conquer and dynamic programming.",
            "Database Systems": "Teaches relational models, SQL queries, and normalization principles.",
            "Software Engineering": "Explains software development lifecycle, design patterns, and testing.",
            "Artificial Intelligence": "Covers search algorithms, neural networks, and machine learning basics."
        }

        
        created_lessons:list[Lessons] = []
        exited_faculty:QuerySet[Faculty] = Faculty.objects.all()
        exited_teacher:QuerySet[Teacher] = Teacher.objects.all()
        
        titles = list(LESSONS.keys())[:lesson_count]
        
        for title in titles:
            description = LESSONS[title]
            faculty:Faculty = choice(exited_faculty)
            teacher:Teacher = choice(exited_teacher)
            
            created_lessons.append(
                Lessons(
                    title = title,
                    description = description,
                    faculty = faculty,
                    teacher = teacher
                )
            )
        Lessons.objects.bulk_create(created_lessons,ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Created lessons"
            )
        )
    
    
    #def __generate_lectors(self,lector_count =12)->None:
        #created_lectors:list[Lectures] = []
        #xited_lesson_name:QuerySet[Lectures] = Lectures.objects.all()
        
    
    def handle(self, *args:tuple[Any,...], **kwargs:dict[str,Any])->None:
        start_time:datetime = datetime.now()
        
        #self.__generate_dean(dean_count=4)
        #self.__generate_users(user_count=20)
        #self.__generate_faculty(faculty_count=3)
        #self.__generate_teacher(teacher_count=20)
        self.__generate_lessons(lesson_count=12)
        
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                    (datetime.now() - start_time).total_seconds()
                )
        )