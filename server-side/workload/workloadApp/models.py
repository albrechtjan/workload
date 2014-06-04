from django.db import models
from django.contrib.auth.models import User

class Lecture(models.Model):
    #TODO: Add Lecture ID
    semester = models.CharField(max_length=6) #e.g. WS2014
    name = models.CharField(max_length=200)
    startDay = models.DateField() # The day of the first lecture event. Or the monday of the week when the lecture starts.
    endDay = models.DateField()   # The day of the last lecture event. Or the day of the exam. Something like this.

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    def isActive(self,date):
        return (self.startDay<=date and date <=self.endDay)


# The Student model is possibly going to be written as an extension of the user model once the shibboleth login has been implemented
# But in fact it works pretty well to associate user and student by a one-to-one relationship
class Student(models.Model):
    permanentId = models.IntegerField()
    lectures = models.ManyToManyField(Lecture,blank=True)
    user = models.OneToOneField(User)

    def __unicode__(self):  # Python 3: def __str__(self):
        return "student id "+str(self.permanentId);

    def startOfLectures(self):
        # returns a datetime.date a day in the first week of lectures
        if not self.lectures.all():
            raise Exception("no lectures found")
        return min([lecture.startDay for lecture in list(self.lectures.all())])

    def endOfLectures(self):
        # returns a datetime.date of a day in the last week of lectures
        if not self.lectures.all():
            raise Exception("no lectures found")
        return max([lecture.endDay for lecture in list(self.lectures.all())])


class WorkingHoursEntry(models.Model):
    hoursInLecture=models.IntegerField(default=0)
    hoursForHomework=models.IntegerField(default=0) 
    hoursStudying=models.IntegerField(default=0)
    lecture = models.ForeignKey(Lecture)
    student = models.ForeignKey(Student)
    week = models.DateField() # A datetime.date object. The Monday (!!!) of the week for which the working hours are entered 

    def __unicode__(self):  # Python 3: def __str__(self):
        return "student" + str(self.student.permanentId) + "in week number" + str(self.week.isocalendar()[1])