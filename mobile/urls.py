from django.conf.urls import patterns, url


urlpatterns = patterns('mobile.views',
    # Examples:
    # url(r'^$', 'base.views.home', name='home'),
    # url(r'^base/', include('base.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login/$', 'login'),
    url(r'^register/$', 'register'),
    url(r'^logout/$', 'logout'),
)
