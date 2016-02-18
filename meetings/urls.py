from django.conf.urls import url

from meetings.views import MeetingsView

urlpatterns = [
    url(r'', MeetingsView.index)
]