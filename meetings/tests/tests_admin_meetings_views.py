from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from meetings.models import Meeting
from meetings.tests.test_utils import TestUtils
from members.models import Person, Organization


class TestsStudentMeetingsViews(TestCase):
    def setUp(self):
        TestUtils.setupAdminSession(self)
        TestUtils.setupMeeting(self)

    def test_meetings_list(self):
        resp = self.client.get('/meetings/')
        # User is logged in with permission to list meetings thus the page should load (response should be 200)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)

    def test_meetings_list_context(self):
        # Context should contain all meetings added to the database
        resp = self.client.get(reverse('meetings:meetings-list'))
        self.assertEqual([meeting.pk for meeting in resp.context['object_list']], [1, 2, 3])

    def test_meetings_correct_update(self):
        # Sanity check
        meeting_1 = Meeting.objects.get(pk=1)
        self.assertEqual(meeting_1.secretary, None)

        # Change secretary to current user using toggle
        student = Person.objects.get(pk=1)
        resp = self.client.post('/meetings/1/toggle/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Meeting.objects.get(pk=1).secretary, student)

        # Update meeting
        student = Person.objects.get(pk=1)
        begin_time = datetime(2016,12,12,12,12,0)
        end_time = datetime(2016,12,12,13,13,0)
        place = 'HB 2B'
        organization = Organization.objects.get(pk=2)
        resp = self.client.post('/meetings/1/', {'secretary':student, 'begin_time':begin_time, 'end_time':end_time, 'place':place, 'organization':organization})
        self.assertEqual(resp.status_code, 200)
        meeting_1 = Meeting.objects.get(pk=1)
        self.assertTrue(meeting_1.secretary, student)
        self.assertTrue(meeting_1.begin_time, begin_time)
        self.assertTrue(meeting_1.end_time, end_time)
        self.assertTrue(meeting_1.place, place)
        self.assertTrue(meeting_1.organization, organization)

    def test_meetings_incorrect_update(self):
        # Ensure that a non-existent pk throws a 404
        resp = self.client.post('/meetings/9999/toggle/')
        self.assertEqual(resp.status_code, 404)

        # Post unnecessary data
        admin = Person.objects.get(pk=1)
        student = Person.objects.create(username='s1234567', password='secret', first_name='studentTest')
        student.set_password('secret')
        student.save()
        resp = self.client.post('/meetings/1/toggle/', {'secretary': student})
        self.assertEqual(resp.status_code, 200)
        meeting_1 = Meeting.objects.get(pk=1)
        self.assertEqual(meeting_1.secretary, admin)

        # Post NO data
        resp = self.client.post('/meetings/1/')
        self.assertEqual(resp.status_code, 200)
        # TODO Check whether errors have occured

        # Send junk post data
        resp = self.client.post('/meetings/1/', {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)

        # Send non-existent Organization pk
        resp = self.client.post('/meetings/1/', {'organization': 5})
        self.assertEqual(resp.status_code, 200)



