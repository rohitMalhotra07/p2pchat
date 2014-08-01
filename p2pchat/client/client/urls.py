from django.conf.urls import patterns, include, url
from clientNode.views import *
 
urlpatterns = patterns('',
	url(r'^$',login),
    url(r'^register/$', register),
    url(r'^checkvalidemail',checkvalidemail),
)