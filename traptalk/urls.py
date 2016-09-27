from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import traptalkapp.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', traptalkapp.views.index, name='index'),
    url('signup$', traptalkapp.views.signup, name='signup'),
    url('signin$', traptalkapp.views.signin, name='signin'),
    url('signout$', traptalkapp.views.signout, name='signout'),
    url('main$', traptalkapp.views.main, name='main'),
    url(r'^admin/', include(admin.site.urls)),
]


#url(r'^main/(?P<string>[\w\-]+)/(?P<string>[\w\-]+)/$','traptalkapp.views.main', name='main'),