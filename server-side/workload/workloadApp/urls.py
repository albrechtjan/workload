from django.conf.urls import patterns, url
from workloadApp import views


urlpatterns = patterns('',
    url(r'^calendar/', views.calendar, name='calendar'),
    url(r'^selectLecture/', views.selectLecture,name='selectLecture')
)