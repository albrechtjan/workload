from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required


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
    context = RequestContext(request, {
        "year" : request.GET['year'],
        "week" : request.GET['week']
    })
    return HttpResponse(template.render(context))

