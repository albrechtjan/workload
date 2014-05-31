from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader



def calendar(request):

    if not request.user.is_authenticated():
        return HttpResponse("Not logged in. TODO: Redirect to login page")
    else:
        template = loader.get_template('workloadApp/calendar.html')
        context = RequestContext(request, {
        })
        return HttpResponse(template.render(context))