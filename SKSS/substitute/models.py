from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Course(models.Model):
    day = models.CharField(max_length=64)
    grade = models.CharField(max_length=64)
    level = models.CharField(max_length=64)
    subject = models.CharField(max_length=64)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.day}: {self.name}'

class ClassLeader(models.Model):
    staffID = models.CharField(max_length=64)
    password = models.CharField(validators=[MinLengthValidator(4)], max_length=128)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    grade = models.CharField(max_length=64)
    courses = models.ManyToManyField(Course, blank=True, related_name='Cls')

    def __str__(self):
        return f'{self.grade}: {self.name}'

class Condition(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class SubstituteAsk(models.Model):
    date = models.DateField()
    client = models.ForeignKey(to=ClassLeader, on_delete=models.CASCADE)
    extra = models.TextField(blank=True, null=True)
    conditions = models.ManyToManyField(Condition, blank=True, related_name='asks')
    
    def __str__(self):
        return f'{self.date}: {self.client}'

class Entry(models.Model):
    date = models.DateField()
    state = models.CharField(max_length=64)
    CL = models.ForeignKey(to=ClassLeader, on_delete=models.CASCADE)
    ask = models.ForeignKey(to=SubstituteAsk, related_name='entries')

    def __str__(self):
        return f'{self.date}: {self.CL}'