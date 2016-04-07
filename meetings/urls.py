from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from meetings.views import ListMeetingView, ChangeMeetingView, DeleteMeetingView, \
    UploadMinutesView, ListMinutesView, AddMeetingView, ToggleMeetingView, DownloadMinutesView, \
    AgendaMeetingView, DeleteMinutesView

app_name = 'meetings'

urlpatterns = [
    url(r'^$', ListMeetingView.as_view(), name="list_meeting"),
    url(r'^(?P<pk>[0-9]+)/toggle/$', ToggleMeetingView.as_view(), name="toggle_meeting"),
    url(r'^minutes/$', ListMinutesView.as_view(), name='list_minutes'),
    url(r'^minutes/upload/$', UploadMinutesView.as_view(), name='upload_minutes'),
    url(r'^add/$', AddMeetingView.as_view(), name="add_meeting"),
    url(r'^(?P<pk>[0-9]+)/$', ChangeMeetingView.as_view(), name='change_meeting'),
    url(r'^(?P<pk>[0-9]+)/delete/$', DeleteMeetingView.as_view(), name='delete_meeting'),
    url(r'^minutes/(?P<pk>[0-9]+)/download/$', DownloadMinutesView.as_view(), name='download_minutes'),
    url(r'^minutes/(?P<pk>[0-9]+)/delete/$', DeleteMinutesView.as_view(), name='delete_minutes'),
    url(r'^agenda/(?P<pk>[0-9]+)/(?P<token>[0-9a-f]{64})/$', AgendaMeetingView.as_view(), name='agenda_meeting'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
