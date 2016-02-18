from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView, View

from meetings.models import Meeting


class MeetingsView(TemplateView):
    def index(request):
        template = loader.get_template('meetings.html')
        context = {
            'all_meetings': Meeting.objects.all(),
        }
        return HttpResponse(template.render(context, request))

# TODO: remove view, must be used for testing purposes only
class MeetingsIcsView(View):
    def get(self, request):
        calendar = Meeting.objects.as_icalendar()
        return HttpResponse(calendar.to_ical(), content_type="text/calendar")