from audioop import reverse
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Dean(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField( max_length=50)
    education = models.CharField( max_length=50)
    is_teacher = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name 
    


class Faculty(models.Model):

    name = models.CharField(max_length=255)
    dean = models.OneToOneField(Dean,on_delete=models.CASCADE,related_name="faculty")
    

    class Meta:
        verbose_name = ("")
        verbose_name_plural = ("Faculty")

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    LECTOR = 'Lector'
    PRACTICE = 'Practicant'
    
    teacher_type_choices = [
        (LECTOR,"lector"),
        (PRACTICE,"practicant")
    ]
    name = models.CharField( max_length=50)
    education = models.CharField( max_length=50)
    experience = models.IntegerField()
    teacher_type=models.CharField( max_length=50,choices=teacher_type_choices,default=LECTOR)
    
    class Meta:
        verbose_name = ("")
        verbose_name_plural = ("Teacher")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    

    
class Lessons(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    faculty = models.ForeignKey(Faculty,related_name="facultyLess", on_delete=models.CASCADE)
    
    

    class Meta:
        verbose_name = ("")
        verbose_name_plural = ("Lessons")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
    
TIME_CHOICES = [
     ("08:00-08:50", "08:00 - 08:50"),
    ("09:00-09:50", "09:00 - 09:50"),
    ("10:00-10:50", "10:00 - 10:50"),
    ("11:00-11:50", "11:00 - 11:50"),
    ("12:00-12:50", "12:00 - 12:50"),
    ("13:00-13:50", "13:00 - 13:50"),
    ("14:00-14:50", "14:00 - 14:50"),
    ("15:00-15:50", "15:00 - 15:50"),
    ("16:00-16:50", "16:00 - 16:50"),
    ("17:00-17:50", "17:00 - 17:50"),
    ("18:00-18:50", "18:00 - 18:50"),
    ("19:00-19:50", "19:00 - 19:50"),
    ("20:00-20:50", "20:00 - 20:50"),
    
]
    
DAY_CHOICES = [ 
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    
class Lectures(models.Model):
    
    lessons_name=models.ForeignKey(Lessons,related_name="lessons_name", on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,related_name="lecture", on_delete=models.CASCADE)
    time = models.CharField( max_length=50,choices = TIME_CHOICES)
    room = models.IntegerField()
    day = models.CharField(choices = DAY_CHOICES,max_length = 3)
    

    class Meta:
        verbose_name = ("")
        verbose_name_plural = ("Lectures")

    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    

    
class Student(models.Model):
    
    Bachelor='Bachelor'
    Master = 'Master'
    PhDstudent = 'PhDstudent'
    
    type_choices=[
        (Bachelor,"Bachelor"),
        (Master,"Master"),
        (PhDstudent,"phdstudent")
    ]
    
    name = models.CharField( max_length=50)
    type_of_student=models.CharField( max_length=50,choices = type_choices)
    faculty = models.ForeignKey(Faculty,related_name="facultyies", on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name = ("")
        verbose_name_plural = ("Student")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Practice(models.Model):
    lesson_name = models.ForeignKey(Lessons,related_name="practices", on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name="practice", on_delete=models.CASCADE)
    time = models.CharField( max_length=50,choices=TIME_CHOICES)
    room = models.IntegerField()
    students = models.ManyToManyField(Student, related_name = 'studentes')
    day = models.CharField(max_length = 3, choices = DAY_CHOICES)
    

    class Meta:
        verbose_name = ("")
        verbose_name_plural = ("Practice")

    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
    def clean(self):
        if Lectures.objects.filter(time=self.time ,day = self.day).exists():
            raise ValidationError("TIME ERROR")
        if Lectures.objects.filter(room=self.room).exists():
            raise ValidationError("Romm number error")
    def __str__(self):
        return self.lesson_name.title


class Post(models.Model):
    AUTHOR_CHOICES = [
        ("teacher","Teacher"),
        ("dean","Dean")
    ]
    
    title=models.CharField(max_length=100)
    content = models.TextField()
    
    author_type = models.CharField(max_length=155,choices = AUTHOR_CHOICES)
    
   
     
   
    def __str__(self):
        return self.title
            

class Schedule(models.Model):
   
    practice = models.ManyToManyField(Practice,related_name = "schulde")
    lecture = models.ManyToManyField(Lectures,related_name =  "schulde1")
    
    
    
    