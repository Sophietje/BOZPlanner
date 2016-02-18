from django.conf.urls import url

from meetings.views import MeetingsView, MeetingsIcsView

app_name = 'meetings'
urlpatterns = [
    url(r'', MeetingsView.as_view()),
    url(r'ics/all', MeetingsIcsView.as_view())
]