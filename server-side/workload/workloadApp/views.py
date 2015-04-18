from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from datetime import date, timedelta
from workloadApp.models import WorkingHoursEntry, Lecture, Student
from django.views.decorators.cache import patch_cache_control
from functools import wraps
from django.contrib.auth import logout
from objects import Week, Semester
from copy import deepcopy



#Helper functions

# I would like to extend this to support an arbitrary number of notifications 
# It should also treat the notifications from multiple sources equally
# The InoreData - Thing should come as a normal notification from a helper function
# the base.html would have to be updated accordingly
def decorateWithNotification(request):
    moreContext = { "ignoreData" : request.user.student.ignoreData }
    params = dict(list(request.GET.items()) + list(request.POST.items()))
    if "notification" in params:
        moreContext.update({"hasNotification" : True , "notification" : params["notification"]})
        return moreContext
    else:
        moreContext.update({"hasNotification" : False})
        return moreContext

def privacy_agreement(user):
    if user:
        return user.groups.filter(name='has_agreed_to_privacy_agreement').count() != 0
    return False

def never_ever_cache(decorated_function):
    """Like Django @never_cache but sets more valid cache disabling headers.

    @never_cache only sets Cache-Control:max-age=0 which is not
    enough. For example, with max-axe=0 Firefox returns cached results
    of GET calls when it is restarted.
    """
    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        response = decorated_function(*args, **kwargs)
        patch_cache_control(
            response, no_cache=True, no_store=True, must_revalidate=True,
            max_age=0)
        return response
    return wrapper





@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
@method_decorator(never_ever_cache) # Apparently since I added this, the other views seem to be updating nicely as well. Coincidence?
def calendar(request):
    student = request.user.student    
    weeks = student.getWeeksWithLectures()
    weeksHaveData = zip(weeks, [ "green" if student.hasData(week) else "red" for week in weeks], ["isCurrentWeek" if week.isCurrentWeek() else "" for week in weeks])

    #subdivide the list of student-hasData tuples into a list of lists where the sublists contain only events of a certain year
    shaped = []
    semesters = sorted(list(set([Semester.withDate(x[0].friday()) for x in weeksHaveData ]))) # If the friday is in the new semester then the whole week is counted as being in the new semester
    for semester in semesters:
        shaped.append([semester,[x for x in weeksHaveData if Semester.withDate(x[0].friday()) == semester]])

    context = RequestContext(request, {
        "semesters" : shaped
    })

    tst = decorateWithNotification(request)
    context.update(decorateWithNotification(request))
    template = loader.get_template('workloadApp/calendar.html')
    return HttpResponse(template.render(context))



@login_required # For making this work properly seehttps://docs.djangoproject.com/en/1.5/topics/auth/default/#the-login-required-decorator
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def selectLecture(request):

    student = request.user.student
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

    context.update(decorateWithNotification(request))
    return HttpResponse(template.render(context))

@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def enterWorkloadData(request):

    #TODO: Sourround the next lines with a try-catch and handle the case that the url parameters are not given properly
    week = Week(int(request.GET['year']),int(request.GET['week'])) # create isoweek object
    lecture = Lecture.objects.get(id=int(request.GET['lectureId'])) 
    dataEntry, hasBeenCreated = WorkingHoursEntry.objects.get_or_create( week=week.monday() , student=request.user.student , lecture=lecture)

    template = loader.get_template('workloadApp/enterWorkloadData.html')

    context = RequestContext(request,{
        "week" : week,
        "lecture" : lecture,
        # it is probably smarter to simply return the full dataEntry object
        "hoursInLecture" : dataEntry.hoursInLecture,
        "hoursForHomework" : dataEntry.hoursForHomework,
        "hoursStudying" : dataEntry.hoursStudying,

    })

    return HttpResponse(template.render(context))

@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def postWorkloadDataEntry(request):
    #TODO: Make sure ALL post variables are set

    year = int(request.POST['year'])
    lecture = Lecture.objects.get(id=request.POST['lectureId']) 

    dataEntry, hasBeenCreated = WorkingHoursEntry.objects.get_or_create( week=Week(int(request.POST['year']),int(request.POST['week'])).monday() , student=request.user.student , lecture=lecture)

    dataEntry.hoursInLecture   = float(request.POST["hoursInLecture"])
    dataEntry.hoursForHomework = float(request.POST["hoursForHomework"])
    dataEntry.hoursStudying    = float(request.POST["hoursStudying"])
    dataEntry.semesterOfStudy = request.user.student.semesterOfStudy # the semester of study of the student at the time when the dataEntry is created
    dataEntry.save()
    return HttpResponse("success")


@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def addLecture(request):

    student = request.user.student
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

        context.update(decorateWithNotification(request))
        return HttpResponse(template.render(context))
    else:

        template = loader.get_template('workloadApp/addLecture/selectSemester.html')
        context = RequestContext(request,{
            "allSemesters" : Lecture.objects.all().values_list("semester", flat=True).distinct(),
            })
        context.update(decorateWithNotification(request))
        return HttpResponse(template.render(context))

@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def options(request):
    template = loader.get_template('workloadApp/options.html')

    context = RequestContext(request,{

        })

    context.update(decorateWithNotification(request))
    return HttpResponse(template.render(context))

@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def settings(request):
    template = loader.get_template('workloadApp/options/settings.html')
    context = RequestContext(request,{
        "studentID" : request.user.student.id,
        "semesterOfStudy" : request.user.student.semesterOfStudy
        })
    context.update(decorateWithNotification(request))
    return HttpResponse(template.render(context))

@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def permanentDelete(request):
    template = loader.get_template('workloadApp/options/settings/permanentDelete.html')

    context = RequestContext(request,{
        "allLectures" : list(set(Lecture.objects.filter(workinghoursentry__student=request.user.student)))
        })
    context.update(decorateWithNotification(request))
    return HttpResponse(template.render(context))

@login_required
def doPermanentDelete(request):
    lectureToRemove = Lecture.objects.get(id=request.POST["lectureId"])
    request.user.student.lectures.remove(lectureToRemove)
    WorkingHoursEntry.objects.filter(lecture__id=request.POST["lectureId"],student=request.user.student).delete()
    return HttpResponse("success")




@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def chosenLectures(request):
    
    if "lectureId" in request.GET: # TODO: Move this function into API. use ajax post for this
        lectureToRemove = Lecture.objects.get(id=request.GET["lectureId"])
        request.user.student.lectures.remove(lectureToRemove)
        return HttpResponseRedirect("/app/workload/options/chosenLectures/?notification=Lecture removed from list")

     # TODO: Move this function into API. Somehow use ajax post for this
    if "addLecture" in request.GET.keys():
        lecture = Lecture.objects.get(pk=request.GET["addLecture"])
        request.user.student.lectures.add(lecture)
        request.user.student.save()


    template = loader.get_template('workloadApp/options/chosenLectures.html')    

    context = RequestContext(request,{
        "chosenLectures" : list(request.user.student.lectures.all())
        })
    context.update(decorateWithNotification(request))
    return HttpResponse(template.render(context))

def logoutView(request):
    #this is pretty broken and probably does not work with shibboleth
    logout(request)
    return HttpResponseRedirect("/app/workload/?notification=You have been logged out.")


@login_required
# here, agreemetn to the privacy agreement is obviously not required
def privacyAgreement(request):

    if request.method =="POST":  #the user has responed to the form
        if "privacy" in request.POST:
            g = Group.objects.get(name='has_agreed_to_privacy_agreement')
            g.user_set.add(request.user)
            return HttpResponseRedirect("/app/workload/calendar?notification=You have agreed to the privacy agreement")
        else:
            return HttpResponseRedirect("./?notification=You must check the checkbox.")


    template = loader.get_template('workloadApp/privacyAgreement.html')

    context = RequestContext(request,{ # it would be a good idea to pass here the users insitution
         "has_agreed_to_privacy_agreement" : privacy_agreement(request.user)
        })
    context.update(decorateWithNotification(request))
    return HttpResponse(template.render(context))



@login_required
@user_passes_test(privacy_agreement, login_url='/app/workload/privacyAgreement/?notification=Please confirm the privacy policy.')
def visualizeData(request):
    student = request.user.student

    #gathering data for first diagram
    weeks = student.getWeeksWithLectures()
    weekData = []
    for lecture in student.lectures.all():
        dictionary = { "name": lecture.name, "data":[]} 
        for week in weeks:
            try:
                hours = WorkingHoursEntry.objects.get(week=week.monday(),student=request.user.student,lecture=lecture).getTotalHours()
            except WorkingHoursEntry.DoesNotExist:
                hours = 0
            dictionary["data"].append(hours)
        weekData.append(dictionary)

    diagram1 = {
        "categories" : [week.monday().strftime('%b') for week in weeks],
        "series" : weekData
    }

    # #gathering data for second diagram

    categories = student.lectures.all()
    series = [
        {"name": "attending", "data": [student.getHoursSpent(lecture)["inLecture"] for lecture in categories] }, 
        {"name": "homework" , "data": [student.getHoursSpent(lecture)["forHomework"] for lecture in categories]},
        {"name": "studies"  , "data": [student.getHoursSpent(lecture)["studying"] for lecture in categories]}]

    diagram2={
        "categories" :  [lecture.name for lecture in categories], #hack to prevent a crash
        "series" : series
    }
   
    template = loader.get_template('workloadApp/visualizeData.html')

    #gathering data for first pie chart
    totalhours = deepcopy(series) # we re-use what we collected above
    for activity in totalhours:
        activity["y"] = sum(activity["data"])
        activity.pop("data")

    #gathering data for second pie chart
    pie2 = [{"name" : lecture.name, "y" : sum(student.getHoursSpent(lecture).values())} for lecture in student.lectures.all()]


    context = RequestContext(request,{
        "diagram1" : diagram1,
        "diagram2" : diagram2,
        "pie1" : totalhours,
        "pie2" : pie2

        })


    context.update(decorateWithNotification(request))
    return HttpResponse(template.render(context))



