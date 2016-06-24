""" This is the url definition file for the workload project. 
It imports the detailed url configurations of the apps and
the admin interface which are part of the project.

The apps then define their detailed url configurations
in their app-specific urls.py which is contained in the respective
app folder.
"""

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^workload/', include('workloadApp.urls')),
    url(r'^shib/', include('shibboleth.urls', namespace='shibboleth'))
)

