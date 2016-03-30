from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import get_template
from meetings.models import Meeting
from members.models import Organization
from tasks import send_mail


class Command(BaseCommand):
    def handle(self, *args, **options):

        deadline_end = timezone.now().replace(hour=23,minute=59,second=59) + timezone.timedelta(days=10)
        deadline_start = timezone.now().replace(hour=0,minute=0,second=0) + timezone.timedelta(days=10)

        for organization in Organization.objects.all():
            meetings = [meeting for meeting in Meeting.objects.filter(secretary = None, organization=organization, begin_time__lt=deadline_end, begin_time__gt=deadline_start).order_by('begin_time')]
            if len(meetings) > 0:
                mail_context = {'meetings' : meetings, 'organization' : organization}
                if len(meetings) == 1:
                    subject      = '[BOZPlanner] ['+organization.name+'] Secretary required: '+meetings[0].begin_time.strftime('%Y-%m-%d %H:%M')
                else:
                    subject      = '[BOZPlanner] ['+organization.name+'] Secretaries required for multiple meetings '
                text_content = get_template('reminder_mail_plain.html').render(context=mail_context)
                html_content = get_template('reminder_mail_html.html').render(context=mail_context)
                from_email   = 'bozplanner@utwente.nl'
                to           = organization.pref_reminder.values_list('person__email', flat=True)

                mail = EmailMultiAlternatives(subject, text_content, from_email, to)
                mail.attach_alternative(html_content, "text/html")
                send_mail.delay(mail)
