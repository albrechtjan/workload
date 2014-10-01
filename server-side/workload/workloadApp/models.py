from django.db import models
from django.contrib.auth.models import User
from objects import Week, Semester

class Lecture(models.Model):
    semester = models.CharField(max_length=9) #e.g. WS2014/15 or SS2018
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
    lectures = models.ManyToManyField(Lecture,blank=True)
    user = models.OneToOneField(User)

    def __unicode__(self):  # Python 3: def __str__(self):
        return "student id "+str(self.pk);

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


    def hasData(self,week):
        for lectureIterator in self.lectures.all():
            if lectureIterator.isActive(week.monday()) or lectureIterator.isActive(week.sunday()): 
                # if an ongoing lecture has not data for the week, the week is considered to be missing data
                if not WorkingHoursEntry.objects.filter(week=week.monday(),student=self,lecture=lectureIterator): 
                    return False
        return True


    def getWeeksWithLectures(self):
        #returns all weeks between and including the week of the first and the last lecture associated with the student
        start = Week.withdate(self.startOfLectures())
        end = Week.withdate(self.endOfLectures())
        return [start+x for x in range(end-start+1)]

    def getSemestersWithLectures(self):
        semesters = []
        current = Semester.withdate(self.startOfLectures())
        while(current<=Semester.withdate(self.endOfLectures())):
            semesters.append(current)
            current = current.getNextSemester();
        return semesters


    def getHoursSpent(self, lecture): # returns dictionary with times for "inLecture, forHomework, studying"

        workingHours =  WorkingHoursEntry.objects.filter(lecture=lecture,student=self)
        totalHours = { 
            "inLecture"    : sum( [entry.hoursInLecture   for entry in workingHours ]),
            "forHomework"  : sum( [entry.hoursForHomework for entry in workingHours ]),
            "studying"     : sum( [entry.hoursStudying    for entry in workingHours ])
        }
        return totalHours


class WorkingHoursEntry(models.Model):
    hoursInLecture=models.FloatField(default=0)
    hoursForHomework=models.FloatField(default=0) 
    hoursStudying=models.FloatField(default=0)
    lecture = models.ForeignKey(Lecture)
    student = models.ForeignKey(Student)
    week = models.DateField() # A datetime.date object. The Monday (!!!) of the week for which the working hours are entered

    def getTotalHours(self):
        return self.hoursStudying+self.hoursForHomework+self.hoursInLecture
        
    def __unicode__(self):  # Python 3: def __str__(self):
        return "student" + str(self.student.id) + "in week number" + str(self.week.isocalendar()[1])

    

