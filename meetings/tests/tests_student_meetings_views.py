
from django.core.urlresolvers import reverse
from django.test import TestCase

from meetings.models import Meeting
from meetings.tests.test_utils import TestUtils
from members.models import Person


class TestsStudentMeetingsViews(TestCase):
    def setUp(self):
        TestUtils.setupStudentSession(self)
        TestUtils.setupMeeting(self)

    def test_meetings_list(self):
        resp = self.client.get('/meetings/')
        # User is logged in with permission to list meetings thus the page should load (response should be 200)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)

    def test_meetings_list_context(self):
        # Context should contain all meetings added to the database that belong to a (sub)organization of the student
        # 1 represents a meeting belonging to the organization of the student
        # 2 represents a meeting belonging to another organization that the student is not a part of, it should NOT see this meeting
        # 3 represents a meeting belonging to a suborganization of the organization of the student
        resp = self.client.get(reverse('meetings:meetings-list'))
        self.assertEqual([meeting.pk for meeting in resp.context['object_list']], [1, 3])

    def test_meetings_correct_update(self):
        # Test whether posting correct update (toggle) for meeting works correctly
        # Sanity check
        meeting_1 = Meeting.objects.get(pk=1)
        self.assertEqual(meeting_1.secretary, None)

        # Change secretary to student
        student = Person.objects.get(pk=1)
        resp = self.client.post('/meetings/1/toggle/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Meeting.objects.get(pk=1).secretary, student)

    def test_meetings_incorrect_update(self):
        # Test whether posting incorrect data, or try to post things you are not allowed to change as a student

        # Ensure that a non-existent pk throws a 404
        resp = self.client.post('/meetings/2/toggle/')
        self.assertEqual(resp.status_code, 404)

        # Post unnecessary data
        student = Person.objects.get(pk=1)
        resp = self.client.post('/meetings/1/toggle/', {'secretary': student})
        self.assertEqual(resp.status_code, 200)
        meeting_1 = Meeting.objects.get(pk=1)
        self.assertEqual(meeting_1.secretary, student)






