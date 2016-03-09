import os
from time import strftime
from uuid import uuid4

import datetime
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View, FormView
from django.http import HttpResponse

from bozplanner import settings
from meetings.models import Meeting, Minutes

class MeetingsView(ListView):
    model = Meeting
    template_name = 'meetings/meetings.html'

    def get_queryset(self):
        return Meeting.objects.filter(begin_time__gt = datetime.date.today())

class MeetingCreate(CreateView):
    model = Meeting
    fields = ['place', 'begin_time', 'end_time', 'organization']

class MeetingUpdate(UpdateView):
    model = Meeting
    fields = ['place', 'begin_time', 'end_time', 'secretary', 'organization']

class MeetingDelete(DeleteView):
    model = Meeting
    success_url = reverse_lazy('meetings:meetings-list')

class MeetingAddSecretary(UpdateView):
    model = Meeting
    fields = ['secretary']
    success_url = reverse_lazy('meetings:meetings-list')

# TODO: remove view, must be used for testing purposes only
class MeetingsIcsView(View):
    def get(self, request):
        calendar = Meeting.objects.as_icalendar()
        return HttpResponse(calendar.to_ical(), content_type="text/calendar")

class MinutesView(ListView):
    model = Minutes
    template_name = 'meetings/minutes.html'

class MinuteUploadView(View):
    model = Minutes
    succes_url = reverse_lazy('meetings')
    template_name = 'meetings/upload_minutes.html'


    def update_filename(self, minutes):
        initial_path = minutes.file.path
        minutes.file.name = '{}-{}'.format(minutes.meeting.begin_time.date(), minutes.meeting.organization)
        if minutes.meeting.organization.parent_organization != None:
            minutes.file.name += '-{}'.format(minutes.meeting.organization.parent_organization)
        new_path = settings.MEDIA_ROOT + '/' + minutes.file.name

        # Check if file name is unique
        if os.path.isfile(new_path):
            print ('isFile '+new_path)
            path = new_path
            i = 1
            while (os.path.isfile(new_path)):
                print('i='+i.__str__()+': '+new_path)
                i += 1
                new_path = path + '-Version{}'.format(i)

        os.rename(initial_path, new_path)
        minutes.file = new_path
        minutes.save()
        return

    def post(self, request, *args, **kwargs):
        form = request.POST
        file = request.FILES['minutes']
        meeting = Meeting.objects.get(id=form.get('meeting'))
        minutes = Minutes.objects.create(file=file, meeting=meeting)
        minutes.save()

        # Rename minutes file that has been uploaded, should be done AFTER the minutes have been 'saved'
        self.update_filename(minutes)

        return HttpResponse('Minutes have been added.')

