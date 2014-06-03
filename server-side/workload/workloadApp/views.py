from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from datetime import date
from isoweek import Week # I should have a close look at this class when refactoring
from workloadApp.models import WorkingHoursEntry

@login_required # For making this work properly seehttps://docs.djangoproject.com/en/1.5/topics/auth/default/#the-login-required-decorator
def calendar(request):

    # How can I avoid duplicate code here?
    if not request.user.student.lectures:   # If the user 
        return HttpResponse("No lectures chosen. TODO: Redirect to page where lectures can be chosen")

    template = loader.get_template('workloadApp/calendar.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

@login_required # For making this work properly seehttps://docs.djangoproject.com/en/1.5/topics/auth/default/#the-login-required-decorator
def selectLecture(request):
    # How can I avoid duplicate code here?
    if not request.user.student.lectures:   # If the user 
        return HttpResponse("No lectures chosen. TODO: Redirect to page where lectures can be chosen")

    template = loader.get_template('workloadApp/selectLecture.html')

    week = int(request.GET['week'])
    year = int(request.GET['year'])

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

