from django.conf.urls import patterns, url

urlpatterns = patterns('web.views',
    url(r'^test/$', 'test'),
    url(r'^login/$', 'login', name='web_login'),
    url(r'^register/$', 'register', name='web_register'),
    url(r'^infor/$', 'infor', name='web_user_infor'),
    url(r'^logout/$', 'logout', name='web_logout'),
)
