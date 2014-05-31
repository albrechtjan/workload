from django.conf.urls import patterns, url
from workloadApp import views


urlpatterns = patterns('',
    url(r'^$', views.calendar, name='calendar')
)