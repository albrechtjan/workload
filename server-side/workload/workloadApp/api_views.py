"""
The Django view functions for the API

The workload project provides an API which is used by the workload Android app to read and write
data to the database. This file contains the view functions that make up the API. It uses the same
models as the the view functions of the website, which are located in the views.py file.
"""

from django.contrib.auth.decorators import login_required
from workloadApp.models import WorkingHoursEntry, Lecture, Student
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from datetime import date, timedelta
from objects import Week, Semester
from django.views.decorators.csrf import csrf_exempt


def require_app_user_agent(view_function):
    """
    Requires the user-agent string to be set to a hard-coded value.

    Wrapper that checks for the apps user agent string to be set and
    otherwise refuses access to the api.
    This is important because we exempt the API from CSRF protection
    """
    def checking_view(request, *args, **kwargs):
        if "Workload_App_Android_CSRF_EXCEMPT" in request.META['HTTP_USER_AGENT']:
            return view_function(request, *args, **kwargs)
        else:
            return HttpResponse(status=403)
    return checking_view


@login_required
@csrf_exempt
@require_app_user_agent  # should prevent csrf attacks
# There is no need to enforce the priavcy agreement against a rogue client.
def workload_entries(request, year=None, week=None, lecture__id=None):
    """
    This API view can be used to GET and POST the contents of a WorkingHoursEntry model.

    If the request.method is GET, this view will return a list of WorkingHoursEntry objects in json
    format. The three arguments year, week and lecture__id are optional and are used to query the
    WorkingHoursEntries from the database.

    If the request.method is POST, this view is intended to write a single WorkingHoursEntry to the
    database. The function then expects the following keys to be set in the POST dictionary:
    hoursInLecture, hoursForHomework and hoursStudying. The function arguments year, week
    and lecture__id are then mandatory and select the database entry which will either be created
    or, if existing, be overwritten.
    """
    student = request.user.student
    kwargs = {}
    isoweek = None
    if year and week:
        isoweek = Week(int(year), int(week))
        # The week in the WorkingHoursEntry is defined by
        # a datetime entry which points to the Monday of the week.
        kwargs["week"] = isoweek.monday()
    if lecture__id:
        kwargs["lecture__id"] = lecture__id

    if request.method == "GET":
        query_set = WorkingHoursEntry.objects.filter(student=student, **kwargs)
        dicts = [entry.toDict() for entry in query_set.all()]
        return JsonResponse(dicts, safe=False)

    elif request.method == "POST":
        if (year is None or week is None or lecture__id is None):
            raise Exception("If the request.method is POST, no argument can be None.")
        # we make no diference between POST and PUT
        # takes a json-dict similar to what is returned by the GET method when called with a lecture_id
        lecture = Lecture.objects.get(id=lecture__id)
        dataEntry, _ = WorkingHoursEntry.objects.get_or_create(
                                        week=isoweek.monday(), student=student, lecture=lecture)
        dataEntry.hoursInLecture = float(request.POST["hoursInLecture"])
        dataEntry.hoursForHomework = float(request.POST["hoursForHomework"])
        dataEntry.hoursStudying = float(request.POST["hoursStudying"])
        dataEntry.semesterOfStudy = student.semesterOfStudy
        # We note the current semester of study of the student
        dataEntry.save()
        return HttpResponse(status=204)
        # resource update successfully, no content returned
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
@csrf_exempt
@require_app_user_agent  # should prevent csrf attacks
# There is no need to enforce the priavcy agreement against a rogue client.
def menu_lectures_all(request, lecture_id=None):
    """
    This API view provides a list of all lectures
    and allows to update the "active" status of a lecture.

    If the request method is GET, this method will ignore the lecture_id argument and always
    return a json-encoded list of all Lecture objects in the Lectures database. The lecture
    dictionaries also contain an entry "isActive" which indicates if the student has selected this
    lecture for as a lecture he visits.

    If the request method is POST, this method requires the lecture_id argument to be set and
    and requires the "isActive" key to be included in the POST dictionary. Depending on the value
    of "isActive" it will either add or remove the lecture from the lists of lectures that the
    student vists.
    """
    if request.method == "GET":
        lectureDicts = []
        for lecture in Lecture.objects.all():
            lectureDict = lecture.toDict()
            lectureDict["isActive"] = lecture in request.user.student.lectures.all()
            lectureDicts.append(lectureDict)
        return JsonResponse(lectureDicts, safe=False)
    elif request.method == "POST":
        if lecture_id is None:
            raise Exception(
                "you must specify the lecture id when activating/deactivating a lecture")
        lecture = Lecture.objects.get(id=lecture_id)
        if request.POST["isActive"] == "true":
            # In case add is called on a lecture that has already been added,
            # nothing should happen. (According to the stuff I am reading online.)
            # This is what I want here.
            request.user.student.lectures.add(lecture)
        elif request.POST["isActive"] == "false":
            request.user.student.lectures.remove(lecture)
        else:
            return HttpResponse(status=400)
        request.user.student.save()
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def blank(request):
    return HttpResponse("done")
