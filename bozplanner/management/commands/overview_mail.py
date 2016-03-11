from django.core.mail import EmailMultiAlternatives
from django.core.management import BaseCommand
from django.template.loader import get_template
from django.utils import timezone
from meetings.models import Meeting


class Command(BaseCommand):
    def handle(self, *args, **options):

        deadline_end = timezone.now().replace(hour=23,minute=59,second=59) + timezone.timedelta(days=7)
        deadline_start = timezone.now().replace(hour=0,minute=0,second=0)

        # TODO: organization en vinkjes fixen
        # TODO: Define who should be mailed about the secretary missing: people subscribe themselves
        meetings = [meeting for meeting in Meeting.objects.filter(begin_time__lt=deadline_end, begin_time__gt=deadline_start).order_by('begin_time')]

        if len(meetings) > 0:
            mail_context = {'meetings' : meetings}
            subject = "Overview meetings this week"
            text_content = get_template('overview_mail_plain.html').render(context=mail_context)
            html_content = get_template('overview_mail_html.html').render(context=mail_context)
            from_email   = 'bozplanner@utwente.nl'
            to           = ['hengst.kimberly@gmail.com']
            mail = EmailMultiAlternatives(subject, text_content, from_email, to)
            mail.attach_alternative(html_content, "text/html")

        #mail.send()
        print(mail.message())