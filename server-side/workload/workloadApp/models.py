from django.db import models

class Student(models.Model):
    permanentId = 
    lectures = ManyToManyField(Lecture) # Not sure if it really should be this way around or if maybe the lectures should have students...

class Lecture(models.Model):
    semester = models.CharField(max_length=6) #e.g. WS2014
    name = models.CharField(max_length=200)
    startweek = models.DateField()
    endweek = models.DateField()

class WorkingHoursEntry(models.Model):
    hoursInLecture=models.IntegerField(default=0)
    hoursForHomework=models.IntegerField(default=0)
    hoursStudying=models.IntegerField(default=0)
    lecture = models.ForeignKey(Lecture)
    student = models.ForeignKey(Student)

