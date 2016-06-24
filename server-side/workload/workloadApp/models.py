""" Models are python classes with corresponding database tables.
    
    When a model is defined, Django creates a database for it.
    An instance of the model class is a represenation of a single row
    in the corresponding database table. This is one of the core
    features of Django.
"""

from django.db import models
from django.contrib.auth.models import User
from objects import Week, Semester, NoLecturesFound

class Lecture(models.Model):
    """ Defines the model for a lecture

    A lecture object is defined by its name and semester.
    For example, Analysis in summer semester 2018 is a different table
    entry than Analysis in winter semester 2019.
    """
    semester = models.CharField(max_length=9) #e.g. WS2014/15 or SS2018
    name = models.CharField(max_length=200)
    startDay = models.DateField() # The day of the first lecture event. Or the monday of the week when the lecture starts.
    endDay = models.DateField()   # The day of the last lecture event. Or the day of the exam. Something like this.

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    def isActive(self,date):
        return (self.startDay<=date and date <=self.endDay)

    def toDict(self):
        lectureDict = self.__dict__
        lectureDict.pop("_state")
        return lectureDict


class Student(models.Model):
    """ Defines the model for a student.

    For every row in the user table, there is exactly one 
    corresponding row in the Student table,
    An alternative would have been to simply extend the native Django
    user model. This was disfavoured due its complexity.
    "Composition over inheritance, yada yada yada.."
    """
    lectures = models.ManyToManyField(Lecture,blank=True)
    # one-to-one relationship between user and student.
    user = models.OneToOneField(User)
    semesterOfStudy = models.IntegerField(default=0) # default 0 means the semester has not been set. # should have used none for that. oh well.
    ignoreData = models.BooleanField(default=False) # users accounts for testing who's data entries we should ignore during evaluation

    def __unicode__(self):  # Python 3: def __str__(self):
        return "student id "+str(self.pk);

    def startOfLectures(self):
        # returns a datetime.date a day in the first week of lectures
        if not self.lectures.all():
            raise NoLecturesFound
        return min([lecture.startDay for lecture in list(self.lectures.all())])

    def endOfLectures(self):
        # returns a datetime.date of a day in the last week of lectures
        if not self.lectures.all():
            raise NoLecturesFound
        return max([lecture.endDay for lecture in list(self.lectures.all())])

    def getLectures(self, week):
        return self.lectures.filter(startDay__lte=week.sunday(),endDay__gte=week.monday())


    def hasData(self, week):
        """ Returns true if the student has entered data for all his selected lectures in the week.
        """
        for lectureIterator in self.lectures.all():
            if lectureIterator.isActive(week.monday()) or lectureIterator.isActive(week.sunday()): 
                # if an ongoing lecture has no data for the week, the week is considered to be missing data
                if not WorkingHoursEntry.objects.filter(week=week.monday(),student=self,lecture=lectureIterator): 
                    return False
        return True


    def getWeeks(self):
        """ Returns all weeks between and including the week of the first and the last lecture associated with the student
        """
        try:
            start = Week.withdate(self.startOfLectures())
            end = Week.withdate(self.endOfLectures())
            weeks = [start+x for x in range(end-start+1)]
        except NoLecturesFound:
            weeks = []
        for week in weeks:
            week.loadStudentInfo(self)
        return weeks

    def getHoursSpent(self, lecture): 
        """  Returns dictionary with times for "inLecture, forHomework, studying"
        """
        workingHours =  WorkingHoursEntry.objects.filter(lecture=lecture,student=self)
        totalHours = { 
            "inLecture"    : sum( [entry.hoursInLecture   for entry in workingHours ]),
            "forHomework"  : sum( [entry.hoursForHomework for entry in workingHours ]),
            "studying"     : sum( [entry.hoursStudying    for entry in workingHours ])
        }
        return totalHours



class WorkingHoursEntry(models.Model):
    """ Defines the model for the working hours entry.

    Each entry belongs to a specific combination of
    studenht, lecture and week.
    """
    hoursInLecture=models.FloatField(default=0)
    hoursForHomework=models.FloatField(default=0) 
    hoursStudying=models.FloatField(default=0)
    lecture = models.ForeignKey(Lecture)
    student = models.ForeignKey(Student)
    week = models.DateField() 
    # Week is a  datetime.date object. The Monday (!!!) of the week for which the working hours are entered
    # I chose a datetime over isoweek.week for a reason I forgot. Maybe you can't save datatime.week as a model entry?
    semesterOfStudy = models.IntegerField(default=0)


    def toDict(self):
        entryDict = self.__dict__
        entryDict.pop("_state")
        return entryDict

    def getTotalHours(self):
        return self.hoursStudying+self.hoursForHomework+self.hoursInLecture
        
    def __unicode__(self):  # Python 3: def __str__(self):
        return "student" + str(self.student.id) + "in week number" + str(self.week.isocalendar()[1])


