from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from isoweek import Week # I should have a close look at this class when refactoring
from workloadApp.models import WorkingHoursEntry, Lecture

@login_required # For making this work properly seehttps://docs.djangoproject.com/en/1.5/topics/auth/default/#the-login-required-decorator
def calendar(request):

    if not request.user.student.lectures.all():   # If the user 
        return HttpResponse("No lectures chosen. TODO: Show this as a notification and offer link to options page for choosing lectures")

    student = request.user.student

    weekIterator = Week.withdate(student.startOfLectures())
    endWeek   = Week.withdate(student.endOfLectures())

    weeks = []
    hasData = []
    while weekIterator <= endWeek:
        weeks.append(weekIterator)
        hasData.append(True)
        for lectureIterator in student.lectures.all():
            # check if lecture is ongoing at the current week
            if lectureIterator.isActive(weekIterator.monday()) or lectureIterator.isActive(weekIterator.sunday()): 
                # if an ongoing lecture has not data for the current week, the week is considered to be missing data
                if not WorkingHoursEntry.objects.filter(week=weekIterator.monday(),student=student,lecture=lectureIterator): 
                    hasData[-1] = False
                    continue
        weekIterator = weekIterator+1

    template = loader.get_template('workloadApp/calendar.html')
    context = RequestContext(request, {
        "weeksHaveData" : zip(weeks, hasData)
    })
    return HttpResponse(template.render(context))



@login_required # For making this work properly seehttps://docs.djangoproject.com/en/1.5/topics/auth/default/#the-login-required-decorator
def selectLecture(request):

    
    #TODO: Sourround the next two lines with a try-catch and handle the case that the url parameters are not given properly
    week = int(request.GET['week'])
    year = int(request.GET['year'])

    template = loader.get_template('workloadApp/selectLecture.html')

    lecturesThisWeek = list(request.user.student.lectures.all())
    for i in reversed([ i for (i,lecture) in enumerate(lecturesThisWeek) if not (lecture.isActive(Week(year,week).monday()) or lecture.isActive(Week(year,week).friday())) ]):
        # I got this from stackoverflow, not sure why the "reversed" is necessary, maybe it's supposed to speed things up?
        del lecturesThisWeek[i]

    lectureHasData = [ True if WorkingHoursEntry.objects.filter(week=Week(year,week).monday(),student=request.user.student,lecture=lecture) else False for lecture in lecturesThisWeek]


    context = RequestContext(request, {
        "year" : year,
        "week" : week,
        "lecturesToDisplay" : zip(lecturesThisWeek, lectureHasData)
    })
    return HttpResponse(template.render(context))

@login_required
def enterWorkloadData(request):

    #TODO: Sourround the next two lines with a try-catch and handle the case that the url parameters are not given properly
    week = int(request.GET['week'])
    year = int(request.GET['year'])
    lectureId = int(request.GET['lectureId'])

    template = loader.get_template('workloadApp/enterWorkloadData.html')

    context = RequestContext(request,{
        "year" : year,
        "week" : week,
        "lectureId" : lectureId
    })

    return HttpResponse(template.render(context))

@login_required
def postWorkloadDataEntry(request):

    #TODO: Make sure ALL post variables are set

    year = int(request.POST['year'])
    lecture = Lecture.objects.get(id=request.POST['lectureId']) 

    dataEntry, hasBeenCreated = WorkingHoursEntry.objects.get_or_create( week=Week(int(request.POST['year']),int(request.POST['week'])).monday() , student=request.user.student , lecture=lecture)

    dataEntry.hoursInLecture   = int(request.POST["hoursInLecture"])
    dataEntry.hoursForHomework = int(request.POST["hoursForHomework"])
    dataEntry.hoursStudying    = int(request.POST["hoursStudying"])
    dataEntry.save()

    return HttpResponseRedirect('selectLecture/?year='+request.POST['year']+'&week='+request.POST['week'])



@login_required
def addLecture(request):
    # Here the student can choose the list of lectures for which he wants to collect data
    #lectures are sorted by semester

    # If the reach of the application is extended, one can introduce greater hirachies here
    #if "studies" in request.GET.keys():
    #    # Can be "Master Physik" or "Bachelor Physik"

    if "semester" in request.GET.keys():
        template = loader.get_template('workloadApp/addLecture/choose.html')

        context = RequestContext(request,{
            # list of lectures which are given in the stated semester and which have not yet been selected by the user
            "lectures" : Lecture.objects.filter(semester=request.GET["semester"]).exclude(student=request.user.student)
        })
        return HttpResponse(template.render(context))
    else:
        addedLecture = False
        if "addLecture" in request.GET.keys():
            lecture = Lecture.objects.get(pk=request.GET["addLecture"])
            request.user.student.lectures.add(lecture)
            request.user.student.save()
            addedLecture = True

        template = loader.get_template('workloadApp/addLecture/selectSemester.html')
        context = RequestContext(request,{
            "allSemesters" : Lecture.objects.all().values_list("semester", flat=True).distinct(),
            "addedLecture" : addedLecture
            })
        return HttpResponse(template.render(context))

@login_required
def options(request):
    template = loader.get_template('workloadApp/options.html')

    context = RequestContext(request,{

        })

    return HttpResponse(template.render(context))



@login_required
def chosenLectures(request):

    template = loader.get_template('workloadApp/options/chosenLectures.html')    

    chosenLectures = list(request.user.student.lectures.all())
    context = RequestContext(request,{
        "chosenLectures" : chosenLectures
        })

    return HttpResponse(template.render(context))