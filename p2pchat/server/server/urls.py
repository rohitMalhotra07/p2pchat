from django.conf.urls import patterns, include, url
from supernode.views import *
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'supernode.views.user_registration'),
    url(r'^checkvalidemail','supernode.views.checkvalidemail'),
    url(r'^logincheck','supernode.views.logincheck'),
)