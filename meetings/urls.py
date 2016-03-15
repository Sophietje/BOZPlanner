from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from meetings.views import MeetingsView, MeetingsIcsView, MeetingUpdate, MeetingDelete, \
    MinuteUploadView, MinutesView, MeetingAddSecretary, ScheduleAMeetingView, MeetingToggleView

app_name = 'meetings'

urlpatterns = [
    url(r'^$', MeetingsView.as_view(), name="meetings-list"),
    url(r'^(?P<pk>[0-9]+)/toggle/$', MeetingToggleView.as_view(), name="meeting-toggle"),
    url(r'^minutes/$', MinutesView.as_view(), name='minutes'),
    url(r'^minutes/upload/$', MinuteUploadView.as_view(), name='minutes-upload'),
    url(r'^add/$', ScheduleAMeetingView.as_view(), name="meeting-add"),
    url(r'^(?P<pk>[0-9]+)/$', MeetingUpdate.as_view(), name='meeting-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', MeetingDelete.as_view(), name='meeting-delete'),
    url(r'^secretary/(?P<pk>[0-9]+)/$', MeetingAddSecretary.as_view(), name='add-secretary'),
    url(r'^ics/all', MeetingsIcsView.as_view(), name='meetings-ics')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
