from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<payment_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^person/new/$', views.person_new, name='person_new'),
    url(r'^meeting/new/$', views.meeting_new, name='meeting_new'),
]
