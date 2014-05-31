from django.db import models

from django.contrib.auth.models import User

class Lecture(models.Model):
    semester = models.CharField(max_length=6) #e.g. WS2014
    name = models.CharField(max_length=200)
    startweek = models.DateField()
    endweek = models.DateField()


# The Student model is going to be written as an extension of the user model once the shibboleth login has been implemented
class Student(models.Model):
    permanentId = models.IntegerField()
    lectures = models.ManyToManyField(Lecture,blank=True)
    user = models.OneToOneField(User)


class WorkingHoursEntry(models.Model):
    hoursInLecture=models.IntegerField(default=0)
    hoursForHomework=models.IntegerField(default=0)
    hoursStudying=models.IntegerField(default=0)
    lecture = models.ForeignKey(Lecture)
    student = models.ForeignKey(Student)
    week = models.DateField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return "working hours for student" + student.permanentId + "in week number" + week.isocalendar()