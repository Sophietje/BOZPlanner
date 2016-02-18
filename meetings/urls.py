from django.conf.urls import url

from meetings.views import MeetingsView, MeetingsIcsView

urlpatterns = [
    url(r'ics/all', MeetingsIcsView.as_view()),
    url(r'', MeetingsView.index),
]