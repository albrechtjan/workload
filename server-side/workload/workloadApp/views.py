from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader



def calendar(request):

    if not request.user.is_authenticated(): # If the user is not logged in, make him log in :)
        return HttpResponse("Not logged in. TODO: Redirect to login page")

    if not request.user.student.lectures:   # If the user 
        return HttpResponse("No lectures chosen. TODO: Redirect to page where lectures can be chosen")

    else:
        template = loader.get_template('workloadApp/calendar.html')
        context = RequestContext(request, {
        })
        return HttpResponse(template.render(context))
