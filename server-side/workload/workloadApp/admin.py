from django.contrib import admin
from workloadApp.models import Lecture, Student, WorkingHoursEntry

# Register your models here.
class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester')
    ordering = ["-startDay"]
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Student)
admin.site.register(WorkingHoursEntry)
