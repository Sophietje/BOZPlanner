import mimetypes
import urllib
import datetime
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from meetings.forms import MeetingForm
from meetings.models import Meeting, Minutes
from members.auth import permission_required
from members.models import Person


@permission_required('meetings.list_meetings')
class MeetingsView(TemplateView):
    model = Meeting
    template_name = 'meetings/meetings.html'

    def get_context_data(self, **kwargs):
        now = datetime.datetime.now()

        # First condition: You should be able to see upcoming meetings where you are the secretary
        q1 = Q(end_time__gt=now, secretary=self.request.user)

        # If the user may only see meetings from his/her own (sub-)organization(s), put all upcoming meetings of this organization in context
        if self.request.user.has_perm('meetings.list_meetings_organization'):
            # Second condition: Only meetings from own (sub-)organization(s) should be shown
            q2 = Q(organization__in = self.request.user.all_organizations, end_time__gt=now)
            q1 = q1 | q2

        if self.request.user.has_perm('meetings.list_meetings_all'):
            # Should be able to see all meetings
            q2 = Q(end_time__gt=now)
            q1 = q1 | q2

        object_list = list(filter_meetings(q1))

        for meeting in object_list:
            meeting.form = MeetingForm(instance=meeting, auto_id='%s_'+str(meeting.pk))

        return locals()

@permission_required("meetings.add_meeting")
class ScheduleAMeetingView(CreateView):
    model = Meeting
    fields = ['organization', 'begin_time', 'end_time', 'place']
    success_url = reverse_lazy('meetings:meetings-list')
    template_name = 'meetings/schedule_a_meeting.html'

@permission_required("meetings.change_meeting")
class MeetingUpdate(UpdateView):
    model = Meeting
    form_class = MeetingForm

class MeetingToggleView(View):
    def post(self, request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)

        if meeting.secretary is None:
            meeting.secretary = request.user
            meeting.save()
            send_confirmation_email(meeting,request.user, True)
        elif meeting.secretary == request.user:
            meeting.secretary = None
            meeting.save()
            send_confirmation_email(meeting,request.user, False)
        else:
            return JsonResponse({"error": True, "error_message": _("Someone has already claimed this meeting.")})

        return JsonResponse({"error": False, "secretary": meeting.secretary.get_full_name() if meeting.secretary else None})

@permission_required('meetings.delete_meeting')
class MeetingDelete(DeleteView):
    model = Meeting
    success_url = reverse_lazy('meetings:meetings-list')

@permission_required('meetings.add_secretary')
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
        now = datetime.datetime.now()

        # Should be able to see all meetings (with minutes) for which you were secretary
        q1 = Q(begin_time__lt=now, secretary=self.request.user)

        # Should be able to see all meetings (with minutes) from own organizations
        if self.request.user.has_perm('meetings.list_meetings_organization'):
            q2 = Q(organization__in=self.request.user.all_organizations, begin_time__lt=now)
            q1 = q1 | q2

        # Should be able to see all meetings (with minutes)
        if self.request.user.has_perm('meetings.list_meetings_all'):
            q2 = Q(begin_time__lt=now)
            q1 = q1 | q2

        object_list = filter_meetings(q1).prefetch_related('minutes')

        return locals()

class MinuteUploadView(View):
    model = Minutes
    succes_url = reverse_lazy('meetings')
    template_name = 'meetings/upload_minutes.html'

    def post(self, request, *args, **kwargs):
        form = request.POST
        file = request.FILES['minutes']
        date = datetime.datetime.now()
        original_name = file.name
        meeting = Meeting.objects.get(id=form.get('meeting'))
        minutes = Minutes.objects.create(file=file, meeting=meeting, original_name=original_name, date=date)
        minutes.save()

        return redirect('meetings:minutes')

class MinutesDownloadView(View):
    def get(self, request, pk):
        file = get_object_or_404(Minutes, pk=pk)
        response = HttpResponse(open(file.file.path, 'rb').read(), content_type=mimetypes.guess_type(file.original_name)[0] or 'application/octet-stream')
        response['Content-Disposition']= 'attachment; filename=%s' % urllib.parse.quote(file.original_name)
        return response

@permission_required("meetings.delete_minutes")
class MinutesDeleteView(View):
    def post(self, request, pk):
        minutes = get_object_or_404(Minutes, pk=pk)

        if not (minutes.meeting.secretary == request.user or request.user.has_permission('meetings.delete_minutes')):
            raise PermissionError

        minutes.delete()
        return redirect("meetings:minutes")

class AgendaView(View):
    def get(self, request, pk, token):
        person = get_object_or_404(Person, pk=pk)

        if person.agenda_token != token:
            raise PermissionError

        meeting_filter = ~Q()

        if person.preferences.agenda_secretary:
            meeting_filter |= Q(secretary=person)

        if person.preferences.agenda_organization:
            meeting_filter |= Q(organization__in=person.all_organizations)

        print(Meeting.objects.filter(meeting_filter).query)

        calendar = Meeting.objects.filter(meeting_filter).as_icalendar()
        return HttpResponse(calendar.to_ical(), content_type="text/calendar")

def filter_meetings(perms):
    return Meeting.objects.filter(perms)

def filter_minutes(perms):
    return Minutes.objects.filter(perms)

def send_confirmation_email(meeting, person, added=True):
    mail_context = {'meeting' : meeting, 'added' : added}
    subject = '[BOZPlanner] Confirmation meeting '+meeting.begin_time.strftime('%Y-%m-%d %H:%M')
    text_content = get_template('confirmation_mail_student_plain.html').render(context=mail_context)
    html_content = get_template('confirmation_mail_student_html.html').render(context=mail_context)
    from_email   = 'bozplanner@utwente.nl'
    to           = [person.email]

    mail = EmailMultiAlternatives(subject, text_content, from_email, to)
    mail.attach_alternative(html_content, "text/html")
    mail.send()



