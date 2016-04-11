import mimetypes
import urllib
import datetime
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from bozplanner.views import EditModalListView
from meetings.forms import MeetingForm
from meetings.models import Meeting, Minutes
from members.auth import permission_required, login_required
from members.models import Person


@permission_required('meetings.list_meetings')
class ListMeetingView(EditModalListView):
    model = Meeting
    form = MeetingForm
    edit_permission = "meetings.change_meeting"
    success_url = reverse_lazy("meetings:list_meeting")
    template_name = 'meetings/list.html'

    def get_context_data(self):
        now = datetime.datetime.now()

        # First condition: You should be able to see upcoming meetings where you are the secretary
        q = Q(end_time__gt=now, secretary=self.request.user)

        # If the user may only see meetings from his/her own (sub-)organization(s), put all upcoming
        # meetings of this organization in context
        if self.request.user.has_perm('meetings.list_meetings_organization'):
            # Second condition: Only meetings from own (sub-)organization(s) should be shown
            q |= Q(organization__in=self.request.user.all_organizations, end_time__gt=now)

        if self.request.user.has_perm('meetings.list_meetings_all'):
            # Should be able to see all meetings
            q |= Q(end_time__gt=now)

        object_list = list(filter_meetings(q))

        return locals()


@permission_required("meetings.add_meeting")
class AddMeetingView(CreateView):
    model = Meeting
    fields = ['organization', 'begin_time', 'end_time', 'place']
    success_url = reverse_lazy('meetings:list_meeting')
    template_name = 'meetings/form.html'


class ToggleMeetingView(View):
    def post(self, request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)

        if meeting.secretary is None:
            meeting.secretary = request.user
            meeting.save()
            send_confirmation_email(meeting, request.user, added=True)
        elif meeting.secretary == request.user:
            if meeting.is_soon:
                return JsonResponse(
                    {"error": True, "error_message": _("You cannot unsubscribe from this meeting anymore")})
            else:
                meeting.secretary = None
                meeting.save()
                send_confirmation_email(meeting, request.user, added=False)
        else:
            return JsonResponse({"error": True, "error_message": _("Someone has already claimed this meeting.")})

        return JsonResponse(
            {"error": False, "secretary": meeting.secretary.get_full_name() if meeting.secretary else None})


@permission_required('meetings.delete_meeting')
class DeleteMeetingView(DeleteView):
    model = Meeting
    success_url = reverse_lazy('meetings:list_meeting')


@permission_required('meetings.list_meetings')
class ListMinutesView(TemplateView):
    model = Meeting
    template_name = 'minutes/list.html'

    def get_context_data(self, **kwargs):
        now = datetime.datetime.now()

        # Should be able to see all meetings (with minutes) for which you were secretary
        q = Q(begin_time__lt=now, secretary=self.request.user)

        # Should be able to see all meetings (with minutes) from own organizations
        if self.request.user.has_perm('meetings.list_meetings_organization'):
            q |= Q(organization__in=self.request.user.all_organizations, begin_time__lt=now)

        # Should be able to see all meetings (with minutes)
        if self.request.user.has_perm('meetings.list_meetings_all'):
            q |= Q(begin_time__lt=now)

        object_list = filter_meetings(q).prefetch_related('minutes')

        return locals()


@login_required
class UploadMinutesView(View):
    model = Minutes
    succes_url = reverse_lazy('meetings')
    template_name = 'meetings/upload_minutes.html'

    def post(self, request, *args, **kwargs):
        form = request.POST
        meeting = get_object_or_404(Meeting, pk=form.get('meeting'))

        if not (meeting.secretary == request.user or request.user.has_perm('meetings.add_minutes')):
            raise PermissionError

        file = request.FILES['minutes']
        date = datetime.datetime.now()
        original_name = file.name
        minutes = Minutes.objects.create(file=file, meeting=meeting, original_name=original_name, date=date)
        minutes.save()

        return redirect('meetings:list_minutes')


@permission_required('meetings.list_meetings')
class DownloadMinutesView(View):
    def get(self, request, pk):
        file = get_object_or_404(Minutes, pk=pk)
        response = HttpResponse(open(file.file.path, 'rb').read(),
            content_type=mimetypes.guess_type(file.original_name)[0] or 'application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s' % urllib.parse.quote(file.original_name)
        return response


@permission_required("meetings.delete_minutes")
class DeleteMinutesView(View):
    def post(self, request, pk):
        minutes = get_object_or_404(Minutes, pk=pk)
        minutes.delete()
        return redirect("meetings:list_minutes")


class CalendarMeetingView(View):
    def get(self, request, pk, token):
        person = get_object_or_404(Person, pk=pk)

        if person.calendar != token:
            raise PermissionError

        meeting_filter = ~Q()

        if person.preferences.calendar_secretary:
            meeting_filter |= Q(secretary=person)

        if person.preferences.calendar_organization:
            meeting_filter |= Q(organization__in=person.all_organizations)

        calendar = Meeting.objects.filter(meeting_filter).as_icalendar()
        return HttpResponse(calendar.to_ical(), content_type="text/calendar")


def filter_meetings(perms):
    return Meeting.objects.filter(perms)


def filter_minutes(perms):
    return Minutes.objects.filter(perms)


def send_confirmation_email(meeting, person, added=True):
    mail_context = {'meeting': meeting, 'added': added}
    subject = '[BOZPlanner] Confirmation meeting ' + meeting.begin_time.strftime('%Y-%m-%d %H:%M')
    text_content = get_template('confirmation_mail_student_plain.html').render(context=mail_context)
    html_content = get_template('confirmation_mail_student_html.html').render(context=mail_context)
    from_email = 'bozplanner@utwente.nl'
    to = [person.email]

    mail = EmailMultiAlternatives(subject, text_content, from_email, to)
    mail.attach_alternative(html_content, "text/html")
    mail.send()
