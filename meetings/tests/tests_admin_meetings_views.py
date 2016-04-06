from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from meetings.models import Meeting
from meetings.tests.test_meeting_utils import TestMeetingMixin
from members.models import Person, Organization
from members.tests.test_user_utils import TestUserMixin


class TestsAdminMeetingsViews(TestCase, TestMeetingMixin, TestUserMixin):
    def setUp(self):
        self.setupAdminSession()
        self.setupMeeting()

    def test_meetings_list(self):
        resp = self.client.get(reverse('meetings:meetings-list'))
        # User is logged in with permission to list meetings thus the page should load (response should be 200)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)
        # Context should contain all meetings in the database
        self.assertEqual([meeting for meeting in resp.context['object_list']], [self.meeting_1, self.meeting_2, self.meeting_3])

    def test_meetings_correct_update(self):
        # Sanity check
        meeting_1 = Meeting.objects.get(pk=self.meeting_1.pk)
        self.assertEqual(meeting_1.secretary, None)

        # Change secretary to current user using toggle
        student = Person.objects.get(pk=self.user.pk)
        resp = self.client.post(reverse('meetings:meeting-toggle', kwargs={'pk': self.meeting_1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Meeting.objects.get(pk=self.meeting_1.pk).secretary, student)

        # Update meeting using update page
        student = Person.objects.get(pk=self.user.pk)
        begin_time = datetime(2016,12,12,12,12,0)
        end_time = datetime(2016,12,12,13,13,0)
        place = 'HB 2B'
        organization = self.p
        resp = self.client.post(reverse('meetings:meeting-update', kwargs={'pk': 1}), {'secretary':student,
                'begin_time':begin_time, 'end_time':end_time, 'place':place, 'organization':organization })
        self.assertEqual(resp.status_code, 200)
        meeting_1 = Meeting.objects.get(pk=meeting_1.pk)
        self.assertTrue(meeting_1.secretary, student)
        self.assertTrue(meeting_1.begin_time, begin_time)
        self.assertTrue(meeting_1.end_time, end_time)
        self.assertTrue(meeting_1.place, place)
        self.assertTrue(meeting_1.organization, organization)

    def test_meetings_incorrect_update(self):
        # Ensure that a non-existent pk throws a 404
        resp = self.client.post(reverse('meetings:meeting-toggle', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)

        # Post unnecessary data
        admin = Person.objects.get(pk=self.user.pk)
        student = Person.objects.create(username='s1234567', password='secret', first_name='studentTest')
        student.set_password('secret')
        student.save()
        resp = self.client.post(reverse('meetings:meeting-toggle', kwargs={'pk': self.meeting_1.pk}), {'secretary': student})
        self.assertEqual(resp.status_code, 200)
        meeting_1 = Meeting.objects.get(pk=self.meeting_1.pk)
        self.assertEqual(meeting_1.secretary, admin)

        # Post NO data
        resp = self.client.post(reverse('meetings:meeting-update', kwargs={'pk': self.meeting_1.pk}))
        self.assertEqual(resp.status_code, 200)
        # TODO Check whether errors have occured

        # Send junk post data
        resp = self.client.post(reverse('meetings:meeting-update', kwargs={'pk': self.meeting_1.pk}), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)

        # Send non-existent Organization pk
        resp = self.client.post(reverse('meetings:meeting-update', kwargs={'pk': self.meeting_1.pk}), {'organization': 5})
        self.assertEqual(resp.status_code, 200)

    def test_meetings_incorrect_delete(self):
        # Delete non-existent meeting
        resp = self.client.post(reverse('meetings:meeting-delete', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)

    def test_meetings_correct_delete(self):
        # Delete existing meeting
        resp = self.client.post(reverse('meetings:meeting-delete', kwargs={'pk': self.meeting_1.pk}))
        self.assertEqual(resp.status_code, 302)

        # Ensure that meeting is deleted
        resp = self.client.get(reverse('meetings:meetings-list'))
        self.assertEqual([meeting for meeting in resp.context['object_list']], [self.meeting_2, self.meeting_3])

