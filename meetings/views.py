from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.http import HttpResponse

from meetings.models import Meeting

class MeetingsView(ListView):
    model = Meeting
    template_name = 'meetings/meetings.html'

class MeetingCreate(CreateView):
    model = Meeting

class MeetingUpdate(UpdateView):
    model = Meeting

class MeetingDelete(DeleteView):
    model = Meeting
# TODO: remove view, must be used for testing purposes only
class MeetingsIcsView(View):
    def get(self, request):
        calendar = Meeting.objects.as_icalendar()
        return HttpResponse(calendar.to_ical(), content_type="text/calendar")
