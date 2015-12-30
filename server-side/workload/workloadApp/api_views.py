from django.contrib.auth.decorators import login_required, user_passes_test
from workloadApp.models import privacy_agreement
from workloadApp.models import WorkingHoursEntry, Lecture, Student
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

from datetime import date, timedelta
from objects import Week, Semester
from django.views.decorators.csrf import csrf_exempt




@login_required
# @user_passes_test(privacy_agreement) The API does not check for the privacy agreement. The clients should do that themselves. 
# There is no need to enforce the priavcy agreement against a rogue client. 
@csrf_exempt
def workload_entries(request, year=None, week=None, lecture__id=None):
    # require the full url in all cases
    student = request.user.student
    kwargs = {}
    isoweek = None
    if year and week:
        isoweek = Week(int(year), int(week))
        kwargs["week"] = isoweek.monday() # the week in the WorkingHoursEntry is a datetime entry of the monday of the corresponding isoweek
    if lecture__id:
        kwargs["lecture__id"] = lecture__id
        

    if request.method == "GET":
        query_set = WorkingHoursEntry.objects.filter(student=student, **kwargs)
        dicts =  [ entry.toDict() for entry in query_set.all()]    
        return JsonResponse( dicts, safe=False)
    
    elif request.method == "POST":
        if not (year and week and lecture__id):
            raise Exception
        # we make no diference between POST and PUT
        #takes a json-dict similar to what is returned by the GET method when called with a lecture_id
        lecture = Lecture.objects.get(id=lecture__id)
        dataEntry, has_been_created = WorkingHoursEntry.objects.get_or_create(week=isoweek.monday(), student=student , lecture=lecture) 
        dataEntry.hoursInLecture   = request.POST["hoursInLecture"]
        dataEntry.hoursForHomework = request.POST["hoursForHomework"]
        dataEntry.hoursStudying    = request.POST["hoursStudying"]
        dataEntry.semesterOfStudy  = student.semesterOfStudy # the semester of study of the student at the time when the dataEntry is created
        dataEntry.save()
        return HttpResponse(status=204) #resource update successfully, no content returned
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
@csrf_exempt
def menu_lectures_all(request, lecture_id=None):
    if request.method == "GET":
        lectureDicts = []
        for lecture in Lecture.objects.all():
            lectureDict = lecture.toDict()
            lectureDict["isActive"] = lecture in request.user.student.lectures.all()
            lectureDicts.append(lectureDict)
        return JsonResponse(lectureDicts, safe=False)
    elif request.method == "POST":
        if not lecture_id:
            raise HttpResponseNotAllowed("you must specify the lecture id when activating/deactivating a lecture")
        lecture = Lecture.objects.get(id=lecture_id)
        if request.POST["isActive"]=="true":
            # In case add is called on a lecture that has already been added,
            # nothing should happen. (According to the stuff I am reading online.)
            # This is what I want here.
            request.user.student.lectures.add(lecture)
        elif request.POST["isActive"]=="false":
            request.user.student.lectures.remove(lecture)
        else:
            return HttpResponse(status=400)
        request.user.student.save()
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])





@login_required
@csrf_exempt
def privacy_agree(request):
    if request.method == "GET":
        return HttpResponse(privacy_agreement(request.user))
    elif request.method == "POST":
        g = Group.objects.get(name='has_agreed_to_privacy_agreement')
        g.user_set.add(request.user)
        return HttpResponse(status=204) #resource update successfully, no content returned
    else:
        return HttpResponseNotAllowed(['GET','POST'])


@login_required
def blank(request):
    return HttpResponse("done")

