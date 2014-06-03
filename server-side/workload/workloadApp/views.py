from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from datetime import date
from isoweek import Week # I should have a close look at this class when refactoring
from workloadApp.models import WorkingHoursEntry, Lecture

@login_required # For making this work properly seehttps://docs.djangoproject.com/en/1.5/topics/auth/default/#the-login-required-decorator
def calendar(request):

    if not request.user.student.lectures:   # If the user 
        return HttpResponse("No lectures chosen. TODO: Redirect to page where lectures can be chosen")

    template = loader.get_template('workloadApp/calendar.html')
    context = RequestContext(request, {
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
            "lectures" : Lecture.objects.exclude(student=request.user.student)
        })
        return HttpResponse(template.render(context))
    else:
        template = loader.get_template('workloadApp/addLecture/selectSemester.html')
        context = RequestContext(request,{
            "allSemesters" : Lecture.objects.all().values_list("semester", flat=True).distinct()

            })
        return HttpResponse(template.render(context))

@login_required
def options(request):
    return HttpResponse("<a href='chosenLectures/''>show chosen lectures</a>")



@login_required
def chosenLectures(request):
    return HttpResponse("List of Lectures that the user has chosen, with a button to add a new one and the possibility to remove one </br> <a href='addLecture/'>Add A lecture </a>")