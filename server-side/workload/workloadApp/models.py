from django.db import models

from django.contrib.auth.models import User

class Lecture(models.Model):
    semester = models.CharField(max_length=6) #e.g. WS2014
    name = models.CharField(max_length=200)
    startDay = models.DateField() # The day of the first lecture event. Or the monday of the week when the lecture starts.
    endDay = models.DateField()   # The day of the last lecture event. Or the day of the exam. Something like this.


# The Student model is going to be written as an extension of the user model once the shibboleth login has been implemented
class Student(models.Model):
    permanentId = models.IntegerField()
    lectures = models.ManyToManyField(Lecture,blank=True)
    user = models.OneToOneField(User)

    def startOfLectures(self):
        if not self.lectures:
            raise Exception("no lectures found")
        min(self.lectures.all().startDay)

    def endOfLectures(self):
        if not self.lectures:
            raise Exception("no lectures found")
        min(self.lectures.all().endDay)


class WorkingHoursEntry(models.Model):
    hoursInLecture=models.IntegerField(default=0)
    hoursForHomework=models.IntegerField(default=0)
    hoursStudying=models.IntegerField(default=0)
    lecture = models.ForeignKey(Lecture)
    student = models.ForeignKey(Student)
    week = models.DateField() # The Monday of the week for which the working hours are entered

    def __unicode__(self):  # Python 3: def __str__(self):
        return "working hours for student" + student.permanentId + "in week number" + week.isocalendar()