from django.conf.urls import patterns, include, url
from supernode.views import *
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'supernode.views.user_registration'),
    url(r'^checkvalidusername','supernode.views.checkvalidusername'),
    url(r'^logincheck','supernode.views.logincheck'),
    url(r'^logout','supernode.views.logoutServer'),
    url(r'^recieveonlinelist','supernode.views.recieveonlinelist'),
    url(r'^connectedcheck','supernode.views.connectedcheck'),
    url(r'^friendship/',include('friendship.urls')),
)
