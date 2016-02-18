from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView

from meetings.models import Meeting


class MeetingsView(TemplateView):
    def index(request):
        template = loader.get_template('meetings.html')
        context = {
            'all_meetings': Meeting.objects.all(),
        }
        return HttpResponse(template.render(context, request))