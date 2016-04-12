from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import get_template
from meetings.models import Meeting
from members.models import Organization


class Command(BaseCommand):
    def handle(self, *args, **options):

        deadline_end = timezone.now().replace(hour=23,minute=59,second=59) + timezone.timedelta(days=21)
        deadline_start = timezone.now().replace(hour=0,minute=0,second=0)

        for organization in Organization.objects.all():
            meetings = [meeting for meeting in Meeting.objects.filter(secretary = None, organization=organization, begin_time__lt=deadline_end, begin_time__gt=deadline_start).order_by('begin_time')]
            if len(meetings) > 0:
                mail_context = {'meetings' : meetings, 'organization' : organization}
                subject = '[BOZPlanner] ['+organization.name+'] Overview meetings the coming weeks'
                text_content = get_template('overview_mail_student_plain.html').render(context=mail_context)
                html_content = get_template('overview_mail_student_html.html').render(context=mail_context)
                from_email   = 'bozplanner@utwente.nl'
                to           = organization.student_pref_overview.values_list('person__email', flat=True)

                mail = EmailMultiAlternatives(subject, text_content, from_email, to)
                mail.attach_alternative(html_content, "text/html")
                mail.send()
