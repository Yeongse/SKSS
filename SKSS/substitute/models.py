from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Grade(models.Model):
    name = name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Day(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Course(models.Model):
    day = models.ForeignKey(to=Day, on_delete=models.CASCADE)
    grade = models.ForeignKey(to=Grade, on_delete=models.CASCADE)
    level = models.ForeignKey(to=Level, on_delete=models.CASCADE)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.day}: {self.name}'

class ClassLeader(models.Model):
    staffID = models.CharField(max_length=64)
    password = models.CharField(validators=[MinLengthValidator(4)], max_length=128)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    grade = models.ForeignKey(to=Grade, on_delete=models.CASCADE)
    qualifications = models.ManyToManyField(Condition, related_name='cls')
    courses = models.ManyToManyField(Course, related_name='cls')

    def __str__(self):
        return f'{self.grade}: {self.name}'

class SubstituteAsk(models.Model):
    date = models.DateField()
    day = models.ForeignKey(to=Day, on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(to=ClassLeader, related_name='ordered_asks', on_delete=models.CASCADE)
    contractor = models.ForeignKey(to=ClassLeader, related_name='contracted_asks', on_delete=models.CASCADE, blank=True, null=True)
    reason = models.TextField()
    extra = models.TextField(blank=True, null=True)
    conditions = models.ManyToManyField(Condition, blank=True, related_name='asks')
    
    def __str__(self):
        return f'{self.date}: {self.client}'

class Entry(models.Model):
    date = models.DateField()
    day = models.ForeignKey(to=Day, on_delete=models.CASCADE, blank=True, null=True)
    state = models.CharField(max_length=64)
    cl = models.ForeignKey(to=ClassLeader, related_name='entries', on_delete=models.CASCADE)
    ask = models.ForeignKey(to=SubstituteAsk, related_name='entries', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}: {self.cl}'