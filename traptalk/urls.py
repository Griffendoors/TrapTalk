from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import traptalk.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url('signup/$', views.signup, name='signup'),
    url(r'^admin/', include(admin.site.urls)),
]
