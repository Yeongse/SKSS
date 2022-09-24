from django.contrib import admin
from .models import Course, ClassLeader, Condition, SubstituteAsk, Entry, Grade, Level, Day, Subject

# Register your models here.
admin.site.register(Course)
admin.site.register(ClassLeader)
admin.site.register(Condition)
admin.site.register(SubstituteAsk)
admin.site.register(Entry)
admin.site.register(Grade)
admin.site.register(Level)
admin.site.register(Day)
admin.site.register(Subject)