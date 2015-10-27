from django.conf.urls import patterns, url
from workloadApp import views, api_views
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^selectLecture/$', views.selectLecture,name='selectLecture'),
    url(r'^enterWorkloadData/$', views.enterWorkloadData,name='enterWorkloadData'),
    url(r'postWorkloadDataEntry$', views.postWorkloadDataEntry,name='postWorkloadDataEntry'),
    url(r'options/chosenLectures/addLecture/$', views.addLecture,name='addLecture'),
    url(r'options/chosenLectures/$', views.chosenLectures, name="chosenLectures"),
    url(r'options/settings/$', views.settings, name="settings"),
    url(r'options/settings/permanentDelete/$', views.permanentDelete, name="permanentDelete"),
    url(r'options/settings/permanentDelete/doPermanentDelete/$', views.doPermanentDelete, name="doPermanentDelete"),
    url(r'options/logout/$', views.logoutView, name="logoutView"),
    url(r'options/$', views.options, name="options"),
    url(r'^privacyAgreement/$', views.privacyAgreement, name="privacyAgreement"),
    url(r'^visualizeData/$',views.visualizeData,name="visualizeData"),
    url(r'^$', RedirectView.as_view(url='calendar/',permanent=False), name='index'),

    # RESTful API

    url(r'^api/entries/active/$', api_views.workload_entries),
    url(r'^api/entries/active/year/(?P<year>[0-9]{4})/(?P<week>[0-9]+)/lectures/(?P<lecture_id>[0-9]+)/$', api_views.workload_entries),
    url(r'^api/lectures/all/$', api_views.menu_lectures_all),
    url(r'^api/lectures/all/(?P<lecture_id>[0-9]+)/$', api_views.menu_lectures_all),
    # url(r'^api/menu/statistics/$', api_views.menu_statistics),
    # url(r'^api/menu/privacy/$', api_views.menu_privacy),
    url(r'^api/privacy/agree/$', api_views.menu_privacy_agree),
    # url(r'^api/menu/settings/$', api_views.menu_settings),
    # url(r'^api/menu/settings/deletable_lectures/$', api_views.menu_settings_deletableLectures),
    # url(r'^api/menu/settings/deletable_lectures/(?P<lecture_id>[0-9]+)/$', api_views.menu_settings_deletableLectures),
    url(r'^api/blank/$', api_views.blank)

)
