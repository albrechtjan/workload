from django.contrib import admin
from workloadApp.models import Lecture, Student, WorkingHoursEntry

# Register your models here.
admin.site.register(Lecture)
admin.site.register(Student)
admin.site.register(WorkingHoursEntry)
