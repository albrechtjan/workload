from django.contrib.auth.decorators import login_required, user_passes_test
from workloadApp.models import privacy_agreement
from workloadApp.models import WorkingHoursEntry, Lecture, Student
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

from datetime import date, timedelta
from objects import Week, Semester




# @login_required
# def weeks(request):
#     if request.method == "GET":
#         weeks = request.user.student.getWeeks()
#         data = Semester.groupWeeksBySemester(weeks)
#         for entry in data: 
#             entry[0] = entry[0].__dict__ # small hack to make the semester object json-serializable, for lack of better understanding from my side
#         return JsonResponse(data, safe=False)
#     else:
#         return HttpResponseNotAllowed(['GET'])


@login_required
@user_passes_test(privacy_agreement)
def workload_entries(request, year=None, week=None, lecture__id=None):
    student = request.user.student
    isoweek = None
    kwargs = {}
    if lecture__id:
        kwargs["lecture__id"] = lecture__id
    if year and week:
        kwargs["week"] = Week(int(year), int(week))
    if request.method == "GET":
        query_set = WorkingHoursEntry.objects.filter(student=student, **kwargs)
        dicts =  [ entry.toDict() for entry in query_set.all()]
        
        return JsonResponse( dicts, safe=False)
    # TODO:
    # elif request.method == "POST" or request.method == "PATCH":
    #     lectureDict = json.loads(request.body)
    #     # POST creates a new entry
    #     #takes a json-dict similar to what is returned by the GET method when called with a lecture_id
    #     if request.method == "POST":
    #         lecture = Lecture.objects.get(id=lectureDict['lectureId'])
    #         dataEntry = WorkingHoursEntry(week=isoweek.monday(), student=student , lecture=lecture)
    #     else: #if request.method == "PATCH"
    #         if lecture_id:
    #             lecture = Lecture.objects.get(id=lecture_id)
    #             dataEntry = WorkingHoursEntry.objects.get( week=isoweek.monday() , student=student , lecture=lecture)
    #         else:
    #             raise Exception

    #     dataEntry.hoursInLecture   = float(request.POST["hoursInLecture"])
    #     dataEntry.hoursForHomework = float(request.POST["hoursForHomework"])
    #     dataEntry.hoursStudying    = float(request.POST["hoursStudying"])
    #     dataEntry.semesterOfStudy = request.user.student.semesterOfStudy # the semester of study of the student at the time when the dataEntry is created
    #     dataEntry.save()
    #     return 
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PATCH'])


@login_required
def menu_lectures_all(request, lecture_id=None):
    if request.method == "GET":
        for lecture in Lecture.objects.all():
            lectureDict = lecture.toDict()
            lectureDict["isActive"] = lecture in student.lectures.all()
        lectureDicts = [lecture.toDict() for lecture in Lecture.objects.all()]
        return JsonResponse(lectureDicts, safe=False)
    elif request.method == "PATCH":
        raise HttpResponseNotAllowed('not yet implemented')
    else:
        return HttpResponseNotAllowed(['GET', 'PATCH'])


@login_required
def menu_privacy_agree(request):
    pass


@login_required
@user_passes_test(privacy_agreement)
def blank(request):
    return HttpResponse("done")
