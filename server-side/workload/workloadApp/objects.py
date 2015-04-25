import isoweek
import datetime


class Week(isoweek.Week):

    def loadStudentInfo(self, student):
        self.hasData = student.hasData(self)
        self.isCurrentWeek = (self==isoweek.Week.thisweek())




class Semester:
    #Hardcoded semester starting days. Change as necessary
    startSS = datetime.date(2000,4,1)
    startWS = datetime.date(2000,10,1)

    @classmethod
    def groupWeeksBySemester(self, weeks):
        # subdivide the list of weeks into a list of lists where the sublists contain only events of a certain semester
        shaped = []
        semesters = sorted(list(set([Semester.withDate(week.friday()) for week in weeks ]))) # If the friday is in the new semester then the whole week is counted as being in the new semester
        for semester in semesters:
            shaped.append([semester,[week for week in weeks if Semester.withDate(week.friday()) == semester]])
        return shaped


    @classmethod
    def withDate(self,date):
        monthAndDay = datetime.date(self.startSS.year,date.month,date.day)
        if (monthAndDay < self.startSS):
            return Semester(date.year -1 , "WS")
        elif (self.startSS <= monthAndDay < self.startWS):
            return Semester(date.year, "SS")
        else: #(self.startWS <= date):
            return Semester(date.year, "WS")

    def __init__(self,year,semesterType):
        self.year=year # the year in which the semester begins
        self.semesterType=semesterType

    def __unicode__(self):  # Python 3: def __str__(self):
        if(self.semesterType=="SS"):
            return "summer term "+str(self.year)
        else:
            return "winter term "+str(self.year)+"/"+str(self.year+1)

    def __repr__(self):
        return "semester of type "+str(self.semesterType)+" in year "+str(self.year)


    def __cmp__(self,other):
        if (self.year < other.year):
            return -1;
        elif (self.year>other.year):
            return 1;
        else:
            if (self.semesterType==other.semesterType):
                return 0
            elif (self.semesterType=="SS"):
                return -1
            else:
                return 1

    def __hash__(self):
        return hash((self.year,self.semesterType))

    # def getNextSemester(self):
    #     if (self.semesterType == "WS"):
    #         return Semester(self.year,"SS")
    #     else:
    #         return Semester(self.year+1,"WS")

    def name(self):
        return self.__unicode__()
