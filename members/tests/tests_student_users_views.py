from django.core.urlresolvers import reverse
from django.test import TestCase

from meetings.models import Meeting
from members.models import Person
from members.tests.test_user_utils import TestUserUtils


class TestStudentUsersViews(TestCase):
    def setUp(self):
        TestUserUtils.setupStudentSession(self)

    def test_users_list(self):
        # Ensure that students may not view this page, should be redirected (302)
        resp = self.client.get(reverse('members:persons'))
        self.assertEqual(resp.status_code, 403)

    # Student should not be allowed to edit users so should be redirected
    def test_users_update(self):
        # Ensure non-existent pk throws a 302
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 403)

        # Post NO data
        user_1 = Person.objects.get(pk=1)
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 403)
        # Ensure meeting has not been changed
        self.assertEqual(user_1, Person.objects.get(pk=1))

        # Post correct data, user should NOT be updated
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 1}), {'first_name': 'Tester'})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(user_1, Person.objects.get(pk=1))

        # Post junk data, user should NOT be updated
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 1}), {'test': 'onzin'})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(user_1, Person.objects.get(pk=1))

    def test_users_delete(self):
        # Will succeed if user 1 exists
        Person.objects.get(pk=1)
        # Ensure that student may not delete a user
        resp = self.client.post(reverse('members:person_delete', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 403)
        # Ensure meeting is not deleted
        Person.objects.get(pk=1)
