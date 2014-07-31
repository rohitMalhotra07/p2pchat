from django.conf.urls import patterns, include, url
from supernode.views import *
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'supernode.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'supernode.views.user_registration'),
    url(r'^checkvalidemail$', 'supernode.views.ajax'),
    url(r'^checkvalidemail','supernode.views.checkValidEmail'),
    url(r'^logincheck','supernode.views.logincheck')
)