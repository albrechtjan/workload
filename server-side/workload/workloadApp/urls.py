from django.conf.urls import patterns, url
from workloadApp import views
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(r'^calendar/', views.calendar, name='calendar'),
    url(r'^selectLecture/', views.selectLecture,name='selectLecture'),
    url(r'^enterWorkloadData/', views.enterWorkloadData,name='enterWorkloadData'),
    url(r'postWorkloadDataEntry', views.postWorkloadDataEntry,name='postWorkloadDataEntry'),
    url(r'options/chosenLectures/addLecture/', views.addLecture,name='addLecture'),
    url(r'options/chosenLectures/', views.chosenLectures, name="chosenLectures"),
    url(r'options/logout/', views.logoutView, name="logoutView"),
    url(r'options/', views.options, name="options"),
    url(r'^$', RedirectView.as_view(url='calendar/',permanent=False), name='index')
)