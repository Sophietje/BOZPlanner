from django.conf.urls import url

from meetings.views import MeetingsView, MeetingsIcsView, MeetingUpdate, MeetingDelete, MeetingCreate

app_name = 'meetings'
urlpatterns = [
    url(r'^$', MeetingsView.as_view(), name="meetings-list"),
    url(r'^add/$', MeetingCreate.as_view(), name="meeting-add"),
    url(r'^(?P<pk>[0-9]+)/$', MeetingUpdate.as_view(), name='meeting-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', MeetingDelete.as_view(), name='meeting-delete'),
    url(r'^ics/all', MeetingsIcsView.as_view(), name='meetings-ics')
]