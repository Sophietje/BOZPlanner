from datetime import datetime

from meetings.models import Meeting, Minutes
from members.models import Organization


class TestMeetingUtils():
    def setupMeeting(self):
        # Get first organization in database, this should be "Test"
        o = Organization.objects.get(pk=1)
        # Add meeting to be able to check the context
        m = Meeting.objects.create(organization=o, begin_time=datetime(9999, 11, 11, 11, 11, 0), end_time=datetime(9999, 11, 12, 13, 14, 0), place='Zi 0000')
        m.save()

        # Add meeting from new organization
        p = Organization.objects.create(name='Special')
        m = Meeting.objects.create(organization=p, begin_time=datetime(9999, 11, 12, 14, 15, 0), end_time=datetime(9999, 11, 12, 15, 15, 0), place='Educafé')
        m.save()

        # Add meeting from suborganization of 'Test'
        q = Organization.objects.create(name='Subtest', parent_organization=o)
        m = Meeting.objects.create(organization=q, begin_time=datetime(9999, 11, 12, 11, 12, 0), end_time=datetime(9999, 11, 12, 12, 0, 0), place='CR 2D')
        m.save()

        # Add meeting in the past
        p = Organization.objects.get(pk=1)
        m = Meeting.objects.create(organization=p, begin_time=datetime(1990,9,9,10,11,0), end_time=datetime(1990,9,9,11,11,0), place='RA 3224')

        # Add minutes to Meeting "m"
        minutes = Minutes.objects.create(meeting=m, file="minutes.txt", date=datetime(1999,10,10,11,12,0))
        minutes.save()