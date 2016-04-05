from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from meetings.models import Meeting, Minutes
from meetings.tests.test_meeting_utils import TestMeetingUtils
from members.tests.test_user_utils import TestUserUtils


class TestStudentMinutesViews(TestCase):
    def setUp(self):
        TestUserUtils.setupStudentSession(self)
        TestMeetingUtils.setupMeeting(self)

    def test_minutes_list(self):
        resp = self.client.get(reverse('meetings:minutes'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([meeting.pk for meeting in resp.context['object_list']], [4])

    def test_minutes_correct_delete(self):
        # Add new minutes
        minutes = Minutes.objects.create(file='minutes.txt', meeting=Meeting.objects.get(pk=4), date=datetime.now())
        self.assertEqual(Meeting.objects.get(pk=4).minutes.all().count(), 2)
        resp = self.client.get(reverse('meetings:minutes'))
        self.assertEqual([meeting.pk for meeting in resp.context['object_list']], [4])
        # Delete newly added minutes
        resp = self.client.post(reverse('meetings:minutes-delete', kwargs={'pk': minutes.pk}))
        self.assertEqual(resp.status_code, 302)
        # Ensure that minutes have been deleted
        self.assertEqual(Meeting.objects.get(pk=4).minutes.all().count(), 1)
        resp = self.client.get(reverse('meetings:minutes'))
        self.assertEqual([orga.pk for orga in resp.context['object_list']], [4])

    def test_minutes_incorrect_delete(self):
        # Delete non-existing minutes
        resp = self.client.post(reverse('meetings:minutes-delete', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)
        # Assert that list of minutes did not change
        resp = self.client.get(reverse('meetings:minutes'))
        self.assertEqual(Meeting.objects.get(pk=4).minutes.all().count(), 1)
