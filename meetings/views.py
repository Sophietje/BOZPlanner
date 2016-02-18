from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.http import HttpResponse

from meetings.models import Meeting

class MeetingsView(ListView):
    model = Meeting
    template_name = 'meetings/meetings.html'

class MeetingCreate(CreateView):
    model = Meeting
    fields = ['place', 'begin_time', 'end_time', 'organization']

class MeetingUpdate(UpdateView):
    model = Meeting
    fields = ['place', 'begin_time', 'end_time', 'secretary', 'organization']

class MeetingDelete(DeleteView):
    model = Meeting
    success_url = reverse_lazy('meetings:meetings-list')

# TODO: remove view, must be used for testing purposes only
class MeetingsIcsView(View):
    def get(self, request):
        calendar = Meeting.objects.as_icalendar()
        return HttpResponse(calendar.to_ical(), content_type="text/calendar")
