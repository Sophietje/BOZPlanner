import os

import datetime
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView
from django.http import HttpResponse

from bozplanner import settings
from meetings.models import Meeting, Minutes
from members.auth import permission_required
from members.models import Organization


@permission_required('meetings.list_meetings')
class MeetingsView(TemplateView):
    model = Meeting
    template_name = 'meetings/meetings.html'

    def get_context_data(self, **kwargs):
        # First condition: You should be able to see upcoming meetings where you are the secretary
        q1 = Q(end_time__gt = datetime.datetime.now(), secretary = self.request.user)
        context = super(MeetingsView, self).get_context_data()

        # If the user may only see meetings from his/her own (sub-)organization(s), put all upcoming meetings of this organization in context
        if self.request.user.has_perm('meetings.view_organization'):
            # Second condition: Only meetings from own (sub-)organization(s) should be shown
            q2 = Q(organization__in = self.request.user.all_organizations)
            q1 = q1 & q2

        if self.request.user.has_perm('meetings.view_all'):
            # Should be able to see all meetings
            q2 = Q(begin_time__gt = datetime.datetime.now())
            q1 = q1 | q2

        context['object_list'] = filter_meetings(q1)

        return context

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

@permission_required('meetings.list_meetings')
class MinutesView(TemplateView):
    model = Meeting
    template_name = 'meetings/minutes.html'

    def get_context_data(self, **kwargs):
        # Should be able to see all meetings (with minutes) for which you were secretary
        q1 = Q(secretary = self.request.user)
        context = super(MinutesView, self).get_context_data()

        # Should be able to see all meetings (with minutes) from own organizations
        if self.request.user.has_perm('meetings.view_organizations'):
            q2 = Q(organization__in = self.request.user.all_organizations)
            q1 = q1 | q2

        # Should be able to see all meetings (with minutes)
        if self.request.user.has_perm('meetings.view_all'):
            q2 = Q(begin_time__lt = datetime.datetime.now())
            q1 = q1 | q2

        all_meetings = filter_meetings(q1)

        context['object_list'] = all_meetings.prefetch_related('minutes')
        return context

@permission_required("meetings.create_meeting")
class ScheduleAMeetingView(CreateView):
    model = Meeting
    fields = ['organization', 'begin_time', 'end_time', 'place']
    success_url = reverse_lazy('meetings:meetings-list')
    template_name = 'meetings/schedule_a_meeting.html'


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
                print('i='+i.__str__()+': ' + new_path)
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


def filter_meetings(perms):
    return Meeting.objects.filter(perms)

def filter_minutes(perms):
    return Minutes.objects.filter(perms)

