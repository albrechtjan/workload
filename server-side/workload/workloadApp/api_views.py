from django.contrib.auth.decorators import login_required, user_passes_test
from workloadApp.models import privacy_agreement
from workloadApp.models import WorkingHoursEntry, Lecture, Student
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

from datetime import date, timedelta
from objects import Week, Semester




@login_required
def weeks(request):
    if request.method == "GET":
        weeks = request.user.student.getWeeks()
        data = Semester.groupWeeksBySemester(weeks)
        for entry in data: 
            entry[0] = entry[0].__dict__ # small hack to make the semester object json-serializable, for lack of better understanding from my side
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
@user_passes_test(privacy_agreement)
def weeks_lectures(request, year, week, lecture_id=None):
    isoweek = Week(int(year), int(week) )
    student = request.user.student
    if request.method == "GET":
        if lecture_id:
            query_set = WorkingHoursEntry.objects.filter( week=isoweek.monday() , student=student , lecture__id=lecture_id)
            if query_set.exists():
                lecture_entry = query_set.get().toJson()
            else: 
                lecture_entry = None
            return JsonResponse(lecture_entry, safe=False)
        else:
            lectureDicts = [lecture.toJson() for lecture in student.getLectures(isoweek)]
            return JsonResponse(lectureDicts, safe=False)
    elif request.method == "POST" or request.method == "PATCH":
        lectureDict = json.loads(request.body)
        # POST creates a new entry
        #takes a json-dict similar to what is returned by the GET method when called with a lecture_id
        if request.method == "POST":
            lecture = Lecture.objects.get(id=lectureDict['lectureId'])
            dataEntry = WorkingHoursEntry(week=isoweek.monday(), student=student , lecture=lecture)
        else: #if request.method == "PATCH"
            if lecture_id:
                lecture = Lecture.objects.get(id=lecture_id)
                dataEntry = WorkingHoursEntry.objects.get( week=isoweek.monday() , student=student , lecture=lecture)
            else:
                raise Exception

        dataEntry.hoursInLecture   = float(request.POST["hoursInLecture"])
        dataEntry.hoursForHomework = float(request.POST["hoursForHomework"])
        dataEntry.hoursStudying    = float(request.POST["hoursStudying"])
        dataEntry.semesterOfStudy = request.user.student.semesterOfStudy # the semester of study of the student at the time when the dataEntry is created
        dataEntry.save()
        return 
    elif request.method == "PATCH":
        # PATCH updates an existing entry
        lectureDict = json.loads(request.body)
        lecture = Lecture.objects.get(id=request.PATCH['lectureId']) 
        return HttpResponse
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PATCH'])


@login_required
def menu_lectures_all(request):
    if request.method == "GET":
        lectureDicts = [lecture.toJson() for lecture in Lecture.objects.all()]
        return JsonResponse(lectureDicts, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])



@login_required
@user_passes_test(privacy_agreement)
def menu_lectures_active(request, lecture_id=None):
    student = request.user.student

    if request.method == "GET":
        lectureDicts = [lecture.toJson() for lecture in student.lectures.all()]
        return JsonResponse(lectureDicts, safe=False)

    elif request.method == "POST":
        lectureDict = json.loads(request.body)
        lecture = Lecture.objects.get(id=lectureDict["id"])
        student.lectures.add(lecture)
        student.save()
        return HttpResponse

    elif request.method == "DELTE":
        if lecture_id:
            lecture = Lecture.objects.get(id=lecture_id)
            student.lectures.remove(lecture)
            return HttpResponse
        else:
            raise Exception
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'DELTE'])

@login_required
def menu_statistics(request):
    pass

@login_required
def menu_privacy(request):
    pass

@login_required
def menu_privacy_agree(request):
    pass

@login_required
def menu_settings(request):
    pass

@login_required
def menu_settings_deletableLectures(request):
    pass

@login_required
@user_passes_test(privacy_agreement)
def blank(request):
    return HttpResponse("done")