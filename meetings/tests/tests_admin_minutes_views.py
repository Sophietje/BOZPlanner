from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from meetings.models import Meeting, Minutes
from meetings.tests.test_meeting_utils import TestMeetingMixin
from members.tests.test_user_utils import TestUserMixin


class TestAdminMinutesViews(TestCase, TestMeetingMixin, TestUserMixin):
    def setUp(self):
        self.setupAdminSession()
        self.setupMeeting()

    def test_minutes_list(self):
        resp = self.client.get(reverse('meetings:list_minutes'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([meeting for meeting in resp.context['object_list']], [self.meeting_4])

    def test_minutes_correct_delete(self):
        # Add new minutes
        minutes = Minutes.objects.create(file='minutes.txt', meeting=Meeting.objects.get(pk=self.meeting_4.pk), date=datetime.now())
        self.assertEqual(Meeting.objects.get(pk=self.meeting_4.pk).minutes.all().count(), 2)
        resp = self.client.get(reverse('meetings:list_minutes'))
        self.assertEqual([meeting for meeting in resp.context['object_list']], [self.meeting_4])
        # Delete newly added minutes
        resp = self.client.post(reverse('meetings:delete_minutes', kwargs={'pk': minutes.pk}))
        self.assertEqual(resp.status_code, 302)
        # Ensure that minutes have been deleted
        self.assertEqual(Meeting.objects.get(pk=self.meeting_4.pk).minutes.all().count(), 1)
        resp = self.client.get(reverse('meetings:list_minutes'))
        self.assertEqual([meeting for meeting in resp.context['object_list']], [self.meeting_4])

    def test_minutes_incorrect_delete(self):
        # Delete non-existing minutes
        resp = self.client.post(reverse('meetings:delete_minutes', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)
        # Assert that list of minutes did not change
        resp = self.client.get(reverse('meetings:list_minutes'))
        self.assertEqual(Meeting.objects.get(pk=self.meeting_4.pk).minutes.all().count(), 1)
