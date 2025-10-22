from datetime import datetime
from typing import Any

from random import choice,choices,randint
from django.core.management.base import BaseCommand
from django.db.models import QuerySet

from univer.models import Dean 

class Command(BaseCommand):
    
    NAME_WORDS = (
        "Болат Алтынбек",
        "Талгат Данияр",
        "Ерлан Алан",
        "Ерлан Асылым"
    )
    
    
    def __generate_dean(self,dean_count = 4):
        created_dean:list[Dean] = []
        
        i:int
        for i in range(dean_count):
            name = "".join(choice(self.NAME_WORDS))
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
        
    
    
    
    
    
    def handle(self, *args:tuple[Any,...], **kwargs:dict[str,Any])->None:
        start_time:datetime = datetime.now()
        
        self.__generate_dean(dean_count=4)
        
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                    (datetime.now() - start_time).total_seconds()
                )
        )