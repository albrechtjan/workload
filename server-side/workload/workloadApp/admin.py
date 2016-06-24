"""Defines the admin interface for the worklaod app

The admin.py files are documented here: 
https://docs.djangoproject.com/en/1.9/intro/tutorial02/#introducing-the-django-admin
This configuration is very close to the default configuration. 
"""

from django.contrib import admin
from workloadApp.models import Lecture, Student, WorkingHoursEntry


class LectureAdmin(admin.ModelAdmin):
	""" The only custom ModelAdmin we define.
	It modifies the way the Lecture model is displayed.
	"""
	# show the name and the semester for each lecture
    list_display = ('name', 'semester')
    # Sort by starting date, most recent first.
    ordering = ["-startDay"]

admin.site.register(Lecture, LectureAdmin)
admin.site.register(Student)
admin.site.register(WorkingHoursEntry)
