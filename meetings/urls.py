from django.conf.urls import url

from meetings.views import MeetingsView

app_name = 'meetings'
urlpatterns = [
    url(r'', MeetingsView.as_view())
]