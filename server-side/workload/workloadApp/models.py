from datetime import timedelta
from django.db import models
from classes import StudentWeek

from django.contrib.auth.models import User

class Lecture(models.Model):
    semester = models.CharField(max_length=6) #e.g. WS2014
    name = models.CharField(max_length=200)
    startDay = models.DateField() # The day of the first lecture event. Or the monday of the week when the lecture starts.
    endDay = models.DateField()   # The day of the last lecture event. Or the day of the exam. Something like this.

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


# The Student model is possibly going to be written as an extension of the user model once the shibboleth login has been implemented
class Student(models.Model):
    permanentId = models.IntegerField()
    lectures = models.ManyToManyField(Lecture,blank=True)
    user = models.OneToOneField(User)

    def __unicode__(self):  # Python 3: def __str__(self):
        return "student id "+str(self.permanentId);

    def startOfLectures(self):
        # returns a datetime.date a day in the first week of lectures
        if not self.lectures:
            raise Exception("no lectures found")
        return min([lecture.startDay for lecture in list(self.lectures.all())])

    def endOfLectures(self):
        # returns a datetime.date of a day in the last week of lectures
        if not self.lectures.all():
            raise Exception("no lectures found")
        return min([lecture.endDay for lecture in list(self.lectures.all())])

    def getCalendarWeeks(self):
        startDate = self.startOfLectures();
        weekMondayIterator = startDate - timedelta(days=startDate.weekday())
        weeks = []
        while weekMondayIterator <= self.endOfLectures():
            weeks.append(StudentWeek(mondaydate=weekMondayIterator, hasdata=True))
            for lectureIterator in self.lectures.all():
                if not WorkingHoursEntry.objects.filter(week=weekMondayIterator,student=self,lecture=lectureIterator): 
                    weeks[-1].hasData = False
                    continue
            weekMondayIterator = weekMondayIterator + timedelta(weeks=1)
        return weeks




class WorkingHoursEntry(models.Model):
    hoursInLecture=models.IntegerField(default=0)
    hoursForHomework=models.IntegerField(default=0) 
    hoursStudying=models.IntegerField(default=0)
    lecture = models.ForeignKey(Lecture)
    student = models.ForeignKey(Student)
    week = models.DateField() # A datetime.date object. The Monday (!!!) of the week for which the working hours are entered 

    def __unicode__(self):  # Python 3: def __str__(self):
        return "student" + str(self.student.permanentId) + "in week number" + str(self.week.isocalendar()[1])