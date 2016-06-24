""" This module collects a few python classes (should have been called classes.py)
that have turned out to be useful
"""

import isoweek
import datetime
from django.conf import settings


class NoLecturesFound(Exception):
    """ Custom exception used in the Student model """
    pass


class Week(isoweek.Week):
    """Extends the isoweek.Week with a method that
    adds two useful fields.

    Has a bit of a code smell to it.
    """

    def loadStudentInfo(self, student):
        self.hasData = student.hasData(self)
        self.isCurrentWeek = (self == isoweek.Week.thisweek())


class Semester:
    """ Represents a semester such as Summer Semester 2020
    """
    startSS = datetime.date(2000,
                            settings.SUMMER_SEMESTER_START_MONTH,
                            settings.SUMMER_SEMESTER_START_DAY_OF_MONTH
                            )
    startWS = datetime.date(2000,
                            settings.WINTER_SEMESTER_START_MONTH,
                            settings.WINTER_SEMESTER_START_DAY_OF_MONTH
                            )

    @classmethod
    def groupWeeksBySemester(cls, weeks):
        """ Subdivides the list of weeks into a list of lists where the sublists contain
        only events of a certain semester
        """
        shaped = []
        # If the friday is in the new semester then the whole week is counted as being in the new semester
        semesters = sorted(list(set([Semester.withDate(week.friday()) for week in weeks])))
        for semester in semesters:
            shaped.append([semester, [week for week in weeks if Semester.withDate(week.friday()) == semester]])
        return shaped

    @classmethod
    def withDate(cls, date):
        """Returns the obejct of the seemster which is taking place during the
        date"""
        monthAndDay = datetime.date(cls.startSS.year, date.month, date.day)
        if (monthAndDay < cls.startSS):
            return Semester(date.year - 1, "WS")
        elif (cls.startSS <= monthAndDay < cls.startWS):
            return Semester(date.year, "SS")
        else:  # (cls.startWS <= date):
            return Semester(date.year, "WS")

    def __init__(self, year, semesterType):
        self.year = year  # the year in which the semester begins
        self.semesterType = semesterType  # "SS" for summer semester or "WS" for winter semester

    def __unicode__(self):  # Python 3: def __str__(self):
        if(self.semesterType == "SS"):
            return "summer term "+str(self.year)
        else:
            return "winter term "+str(self.year)+"/"+str(self.year+1)

    def __repr__(self):
        return "semester of type "+str(self.semesterType)+" in year "+str(self.year)

    def __cmp__(self, other):
        """ Implementing the comparison operator.
        This allows for easy sorting.
        """
        if (self.year < other.year):
            return -1
        elif (self.year > other.year):
            return 1
        else:
            if (self.semesterType == other.semesterType):
                return 0
            elif (self.semesterType == "SS"):
                return -1
            else:
                return 1

    def __hash__(self):
        return hash((self.year, self.semesterType))

    def name(self):
        return self.__unicode__()
