from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from meetings.views import MeetingsView, MeetingsIcsView, MeetingUpdate, MeetingDelete, \
    MinuteUploadView, MinutesView, MeetingAddSecretary, ScheduleAMeetingView, MeetingToggleView, MinutesDownloadView, \
    AgendaView, MinutesDeleteView

app_name = 'meetings'


urlpatterns = [
    url(r'^/$', MeetingsView.as_view(), name="meetings-list"),
    url(r'^(?P<pk>[0-9]+)/toggle/$', MeetingToggleView.as_view(), name="meeting-toggle"),
    url(r'^minutes/$', MinutesView.as_view(), name='minutes'),
    url(r'^minutes/upload/$', MinuteUploadView.as_view(), name='minutes-upload'),
    url(r'^add/$', ScheduleAMeetingView.as_view(), name="meeting-add"),
    url(r'^(?P<pk>[0-9]+)/$', MeetingUpdate.as_view(), name='meeting-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', MeetingDelete.as_view(), name='meeting-delete'),
    url(r'^secretary/(?P<pk>[0-9]+)/$', MeetingAddSecretary.as_view(), name='add-secretary'),
    url(r'^ics/all', MeetingsIcsView.as_view(), name='meetings-ics'),
    url(r'^minutes/(?P<pk>[0-9]+)/download/$', MinutesDownloadView.as_view(), name='minutes-download'),
    url(r'^minutes/(?P<pk>[0-9]+)/delete/$', MinutesDeleteView.as_view(), name='minutes-delete'),
    url(r'^agenda/(?P<pk>[0-9]+)/(?P<token>[0-9a-f]{64})/$', AgendaView.as_view(), name='agenda'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
