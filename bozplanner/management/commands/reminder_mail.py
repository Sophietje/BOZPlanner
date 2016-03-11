from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import get_template
from meetings.models import Meeting


class Command(BaseCommand):
    def handle(self, *args, **options):

        deadline_end = timezone.now().replace(hour=23,minute=59,second=59) + timezone.timedelta(days=7)
        deadline_start = timezone.now().replace(hour=0,minute=0,second=0) + timezone.timedelta(days=7)

        #TODO: meerdere meetings in 1 email
        # TODO: Define who should be mailed about the secratary missing: people subscribe themselves
        for meeting in Meeting.objects.filter(secretary = None, begin_time__lt=deadline_end, begin_time__gt=deadline_start):
            mail_context = {'meeting' : meeting}
            subject      = 'Secretary required: '+meeting.begin_time.strftime('%Y-%m-%d %H:%M')
            text_content = get_template('reminder_mail_plain.html').render(context=mail_context)
            html_content = get_template('reminder_mail_html.html').render(context=mail_context)
            from_email   = 'bozplanner@utwente.nl'
            to           = ['hengst.kimberly@gmail.com']

            mail = EmailMultiAlternatives(subject, text_content, from_email, to)
            mail.attach_alternative(html_content, "text/html")
            mail.send()
            #print(mail.message())