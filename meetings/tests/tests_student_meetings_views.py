
from django.core.urlresolvers import reverse
from django.test import TestCase

from meetings.models import Meeting
from meetings.tests.test_meeting_utils import TestMeetingMixin
from members.models import Person
from members.tests.test_user_utils import TestUserMixin


class TestsStudentMeetingsViews(TestCase, TestMeetingMixin, TestUserMixin):
    def setUp(self):
        self.setupStudentSession()
        self.setupMeeting()

    def test_meetings_list(self):
        resp = self.client.get(reverse('meetings:meetings-list'))
        # User is logged in with permission to list meetings thus the page should load (response should be 200)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)

    def test_meetings_list_context(self):
        # Context should contain all meetings added to the database that belong to a (sub)organization of the student
        # 1 represents a meeting belonging to the organization of the student
        # 2 represents a meeting belonging to another organization that the student is not a part of, it should NOT see this meeting
        # 3 represents a meeting belonging to a suborganization of the organization of the student
        # 4 represents a meeting in the past
        resp = self.client.get(reverse('meetings:meetings-list'))
        self.assertEqual([meeting for meeting in resp.context['object_list']], [self.meeting_1, self.meeting_3])

    def test_meetings_correct_update(self):
        # Test whether posting correct update (toggle) for meeting works correctly
        # Sanity check
        meeting_1 = Meeting.objects.get(pk=self.meeting_1.pk)
        self.assertEqual(meeting_1.secretary, None)

        # Change secretary to student
        student = Person.objects.get(pk=self.user.pk)
        resp = self.client.post(reverse('meetings:meeting-toggle', kwargs={'pk': self.meeting_1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Meeting.objects.get(pk=self.meeting_1.pk).secretary, student)

    def test_meetings_incorrect_update(self):
        # Test whether posting incorrect data, or try to post things you are not allowed to change as a student

        # Ensure that a non-existent pk throws a 404
        resp = self.client.post(reverse('meetings:meeting-toggle', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)

        # Try to update a meeting, should not be allowed so user should be redirected
        student = Person.objects.get(pk=self.user.pk)
        resp = self.client.post(reverse('meetings:meeting-update', kwargs={'pk': self.meeting_1.pk}), {'secretary': student})
        self.assertEqual(resp.status_code, 403)

        # Post unnecessary data
        student = Person.objects.get(pk=self.user.pk)
        resp = self.client.post(reverse('meetings:meeting-toggle', kwargs={'pk': self.meeting_1.pk}), {'secretary': student})
        self.assertEqual(resp.status_code, 200)
        meeting_1 = Meeting.objects.get(pk=self.meeting_1.pk)
        self.assertEqual(meeting_1.secretary, student)

    def test_meetings_delete(self):
        # Ensure that student may not delete a meeting
        resp = self.client.post(reverse('meetings:meeting-delete', kwargs={'pk': self.meeting_1.pk}))
        self.assertEqual(resp.status_code, 403)
        # Ensure meeting is not deleted
        resp = self.client.get(reverse('meetings:meetings-list'))
        self.assertEqual([meeting for meeting in resp.context['object_list']], [self.meeting_1, self.meeting_3])




