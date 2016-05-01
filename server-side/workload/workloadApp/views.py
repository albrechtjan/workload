"""
The Django view functions for the Website

The workload project provides a public-facing website which can be used by the students to enter
their data. This file contains the view functions that make up the website. It uses the same
models as the the view functions of the API, which are located in the api_views.py file.

Above the view functions, this file also contains a number of relevant helpter functions.
"""

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.cache import patch_cache_control
from objects import Week, Semester
from datetime import date, timedelta
from workloadApp.models import WorkingHoursEntry, Lecture, Student
from functools import wraps
from copy import deepcopy



#Helper functions and view function wrappers


def require_privacy_agreement(view_function):
    """ View wrapper that checks if the user has agreed to the privacy agreement

    More specifically, it checks if the user belongs to the 
    'has_agreed_to_privacy_agreement' group
    """
    def checking_view(request, *args, **kwargs):
        if request.user.groups.filter(name='has_agreed_to_privacy_agreement').exists():
            return view_function(request, *args, **kwargs)
        else:
            target = ( "/app/workload/privacyAgreement/"
                       "?notification=Please confirm the privacy policy.")
            return HttpResponseRedirect(target)
    return checking_view


def decorateWithNotification(request):
    """ This method allows to show the user a notification based on a POST or GET parameter

    Unfortunately only a single notification per request is supported. It must be passed with key
    "notification" in the GET or POST dictionary. 
    """
    params = dict(list(request.GET.items()) + list(request.POST.items()))
    if "notification" in params:
        return {"hasNotification" : True , "notification" : params["notification"]}
    else:
        return {"hasNotification" : False}


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

def add_info(context, request):
    """ Updates the context dictionary with the notification information and test account info """
    context.update(decorateWithNotification(request))
    context.update({ "ignoreData" : request.user.student.ignoreData })
    return context


# View functions

@login_required
@require_privacy_agreement
@method_decorator(never_ever_cache) 
# Apparently since I added never_ever_cache this here, 
# the other views seem to be updating nicely as well. Coincidence?
def calendar(request):
    """ The view function for the calendar on the start page """
    weeks = request.user.student.getWeeks()
    context = RequestContext(request, {
        "semesters" : Semester.groupWeeksBySemester(weeks)
    })
    template = loader.get_template('workloadApp/calendar.html')
    return HttpResponse(template.render(add_info(context, request)))



@login_required
@require_privacy_agreement
def selectLecture(request):
    student = request.user.student
    # Build the week object
    weekNumber = int(request.GET['week']) # number of week in the year
    yearNumber = int(request.GET['year'])
    week = Week(yearNumber, weekNumber)

    template = loader.get_template('workloadApp/selectLecture.html')
    
    lecturesThisWeek = student.getLectures(week)
    lectureHasData = [ WorkingHoursEntry.objects.filter(
                            week=week.monday(),
                            student=student,
                            lecture=lecture).exists() for lecture in lecturesThisWeek]

    context = RequestContext(request, {
        "year" : yearNumber,
        "week" : weekNumber,
        "lecturesToDisplay" : zip(lecturesThisWeek, lectureHasData)
    })
    return HttpResponse(template.render(add_info(context, request)))

@login_required
@require_privacy_agreement
def enterWorkloadData(request):

    """ View function for the page where the user actually enters his work data"""

    week = Week(int(request.GET['year']),int(request.GET['week'])) # create isoweek object
    lecture = Lecture.objects.get(id=int(request.GET['lectureId'])) 
    dataEntry, _ = WorkingHoursEntry.objects.get_or_create( week=week.monday() , student=request.user.student , lecture=lecture)

    template = loader.get_template('workloadApp/enterWorkloadData.html')

    context = RequestContext(request,{
        "week" : week,
        "lecture" : lecture,
        # it is probably smarter to simply return the full dataEntry object
        "hoursInLecture" : dataEntry.hoursInLecture,
        "hoursForHomework" : dataEntry.hoursForHomework,
        "hoursStudying" : dataEntry.hoursStudying,
    })
    return HttpResponse(template.render(add_info(context, request)))

@login_required
@require_privacy_agreement
def postWorkloadDataEntry(request):
    """ This view function allows to post the workload data entry.

    It is for POST only and overlaps in functionality with api_views.workload_entries.
    However, we can not call the latter from the website because it is not csrf protected and
    therefore requires a special user agent string.
    There might be ways to improve code sharing betwene the two methods though.
    """

    year = int(request.POST['year'])
    lecture = Lecture.objects.get(id=request.POST['lectureId'])
    dataEntry, _ = WorkingHoursEntry.objects.get_or_create( week=Week(int(request.POST['year']),int(request.POST['week'])).monday() , student=request.user.student , lecture=lecture)
    dataEntry.hoursInLecture   = float(request.POST["hoursInLecture"])
    dataEntry.hoursForHomework = float(request.POST["hoursForHomework"])
    dataEntry.hoursStudying    = float(request.POST["hoursStudying"])
    dataEntry.semesterOfStudy = request.user.student.semesterOfStudy # the semester of study of the student at the time when the dataEntry is created
    dataEntry.save()
    return HttpResponse("success")


@login_required
@require_privacy_agreement
def addLecture(request):

    """ View function for the page where the student can edit the list of lectures for which 
    he wants to collect data.

    Lectures are sorted by semester. The user must first select the semester. This view handles
    both the page where the user selects the semester and where he is shown the available lectures
    in the semester.
    However, this view does not actually activate or deactivate the lectures for the user. That
    happens in the views.chosenLectures function.
    """

    # If the reach of the application is extended, one can introduce more hierarchies here

    context = RequestContext(request,{})
    if "semester" in request.GET.keys():
        template = loader.get_template('workloadApp/addLecture/choose.html')
        context.update({"lectures" : Lecture.objects.filter(semester=request.GET["semester"]).exclude(student=request.user.student)})
    else:
        template = loader.get_template('workloadApp/addLecture/selectSemester.html')
        context.update({"allSemesters" : Lecture.objects.all().values_list("semester", flat=True).distinct()})
    return HttpResponse(template.render(add_info(context, request)))

@login_required
@require_privacy_agreement
def options(request):
    """ Displays the options page
    """
    template = loader.get_template('workloadApp/options.html')
    context = RequestContext(request)
    return HttpResponse(template.render(add_info(context, request)))

@login_required
@require_privacy_agreement
def settings(request):
    """ Displays the settings page
    """
    template = loader.get_template('workloadApp/options/settings.html')
    context = RequestContext(request,{
        "studentID" : request.user.student.id,
        "semesterOfStudy" : request.user.student.semesterOfStudy
        })
    return HttpResponse(template.render(add_info(context, request)))

@login_required
@require_privacy_agreement
def permanentDelete(request):
    """ View function for the page where user can permanently delete his data
    """
    template = loader.get_template('workloadApp/options/settings/permanentDelete.html')

    # all lectures for which a working hour entry exists by the user
    # this includes lectures which the user has un-selected before
    all_user_lectures = list(set(Lecture.objects.filter(workinghoursentry__student=request.user.student)))
    context = RequestContext(request,{
        "allLectures" : all_user_lectures
        })
    context.update(decorateWithNotification(request))
    context.update({ "ignoreData" : request.user.student.ignoreData })
    return HttpResponse(template.render(context))

@login_required
def doPermanentDelete(request):
    """ This function deletes all information associated with one lecture.

    It only works for POST requests that contain the "lectureId" in the POST dictionary.
    """
    lectureToRemove = Lecture.objects.get(id=int(request.POST["lectureId"]))
    request.user.student.lectures.remove(lectureToRemove)
    before = WorkingHoursEntry.objects.filter(lecture__id=request.POST["lectureId"],student=request.user.student).count()
    WorkingHoursEntry.objects.filter(lecture__id=request.POST["lectureId"],student=request.user.student).delete()
    after = WorkingHoursEntry.objects.filter(lecture__id=request.POST["lectureId"],student=request.user.student).count()
    return HttpResponseRedirect("/app/workload/options/settings/permanentDelete/")




@login_required
@require_privacy_agreement
def chosenLectures(request):
    """ Display (and modify) the lectures selected by the user.

    Before displaying the currently selected lectures of the user,  we delete or add lectures 
    the the user's selected lectures if the keys in the GET request dict tell us to.
    """
    context = RequestContext(request)
    context = add_info(context, request)

    if "lectureId" in request.GET.keys():
        # remove the lecture form the list of selected lectures
        lectureToRemove = Lecture.objects.get(id=request.GET["lectureId"])
        request.user.student.lectures.remove(lectureToRemove)
        context.update({"hasNotification" : True , "notification" : "Lecture removed from list"})

    if "addLecture" in request.GET.keys():
        # add the lecture to the list of selected lectures
        lecture = Lecture.objects.get(pk=request.GET["addLecture"])
        request.user.student.lectures.add(lecture)
        request.user.student.save()
        context.update({"hasNotification" : True , "notification" : "Lecture added to list"})


    template = loader.get_template('workloadApp/options/chosenLectures.html')    

    context.update({"chosenLectures" : list(request.user.student.lectures.all())})
    # do not views.add_info to the context here because it will overwrite the notification.
    return HttpResponse(template.render(context)) 



@login_required
# here, the agreement to the privacy agreement is obviously not required
def privacyAgreement(request):

    if request.method =="POST":  #the user has responed to the form
        if "privacy" in request.POST:
            g = Group.objects.get(name='has_agreed_to_privacy_agreement')
            g.user_set.add(request.user)
            return HttpResponseRedirect("/app/workload/calendar?"
                                        "notification=You have agreed to the privacy agreement")
        else:
            return HttpResponseRedirect("./?notification=You must check the checkbox.")


    template = loader.get_template('workloadApp/privacyAgreement.html')
    context = RequestContext(request,{ # it would be a good idea to pass here the users insitution
         "has_agreed_to_privacy_agreement" : privacy_agreement(request.user)
        })
    return HttpResponse(template.render(add_info(context, request)))



@login_required
@require_privacy_agreement
def visualizeData(request):
    student = request.user.student

    #gathering data for first diagram
    weeks = student.getWeeks()
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
        {"name": "attending", 
         "data": [student.getHoursSpent(lecture)["inLecture"] for lecture in categories] }, 
        {"name": "homework" , 
         "data": [student.getHoursSpent(lecture)["forHomework"] for lecture in categories]},
        {"name": "studies"  , "data": [student.getHoursSpent(lecture)["studying"] for lecture in categories]}
        ]

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

    return HttpResponse(template.render(add_info(context, request)))


def logoutView(request):
    #this is pretty broken and probably does not work with shibboleth
    logout(request)
    return HttpResponseRedirect("/app/workload/?notification=You have been logged out.")

