import os
from time import strftime
from uuid import uuid4

import datetime
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View, TemplateView
from django.http import HttpResponse

from bozplanner import settings
from meetings.models import Meeting, Minutes
from members.auth import permission_required



@permission_required('meetings.list_meetings', 'meetings.view_all', 'meetings.view_organization')
class MeetingsView(TemplateView):
    model = Meeting
    template_name = 'meetings/meetings.html'

    def get_context_data(self, **kwargs):
        # First condition: Only upcoming meetings should be shown
        q1 = Q(begin_time__gt = datetime.datetime.now())
        context = super(MeetingsView, self).get_context_data()

        # If the user may only see meetings from his/her own organization, put all upcoming meetings of this organization in context
        if self.request.user.has_perm('meetings.view_organization'):
            print ('This user should only see meetings from own organization: '+str(self.request.user.organization))
            # Second condition: Only meetings from own organization should be shown
            q2 = Q(organization__in = self.request.user.organization.all())
            q1 = q1 & q2

        if self.request.user.has_perm('meetings.is_secretary'):
            print('This user should see meetings from which it is secretary')
            # TODO: Edit q2, organizations not yet correctly filtered
            # If the user is a secretary, the meetings for which he/she is a secretary, but not from their organization, should be shown
            q2 = Q(secretary=self.request.user) #& ~Q(organization__in = self.request.user.organization.all())
            q1 = q1 & q2

        context['object_list'] = filter_meetings(q1)

        return context

def filter_meetings(perms):
    return Meeting.objects.filter(perms)


    # # Deze queryset wordt gereturned als deze listview gebruikt wordt
    # def get_queryset(self):
    #     # Should somehow find organization of user that is logged in, add this to the filter below
    #     return Meeting.objects.filter(begin_time__gt = datetime.date.today())

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

@permission_required("meetings.create_meeting")
class ScheduleAMeetingView(TemplateView):
    model = Meeting
    fields = ['place', 'begin_time', 'end_time', 'organization']
    success_url = reverse_lazy('meetings:meetings-list')
    template_name = 'meetings/schedule_a_meeting.html'

    def saveForm(self, request, *args, **kwargs):


        return HttpResponse('Meeting is scheduled')

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

