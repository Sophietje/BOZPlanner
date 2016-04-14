from django.core.urlresolvers import reverse
from django.test import TestCase

from meetings.models import Meeting
from members.models import Person
from members.tests.test_user_utils import TestUserMixin


class TestStudentUsersViews(TestCase, TestUserMixin):
    def setUp(self):
        self.setupStudentSession()

    def test_users_list(self):
        # Ensure that students may not view this page, should be redirected (302)
        resp = self.client.get(reverse('members:list_person'))
        self.assertEqual(resp.status_code, 403)

    # Student should not be allowed to edit users so should be redirected
    def test_users_update(self):
        # Ensure non-existent pk throws a 302
        resp = self.client.post(reverse('members:list_person'), {'edit': 9999})
        self.assertEqual(resp.status_code, 403)

        # Post NO data
        user_1 = Person.objects.get(pk=1)
        resp = self.client.post(reverse('members:list_person'), {'edit': self.user.pk})
        self.assertEqual(resp.status_code, 403)
        # Ensure meeting has not been changed
        self.assertEqual(user_1, Person.objects.get(pk=self.user.pk))

        # Post correct data, user should NOT be updated
        resp = self.client.post(reverse('members:list_person'), {'edit': self.user.pk, 'first_name': 'Tester'})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(user_1, Person.objects.get(pk=self.user.pk))

        # Post junk data, user should NOT be updated
        resp = self.client.post(reverse('members:list_person'), {'edit': self.user.pk, 'test': 'onzin'})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(user_1, Person.objects.get(pk=self.user.pk))

    def test_users_delete(self):
        # Will succeed if user 1 exists
        Person.objects.get(pk=self.user.pk)
        # Ensure that student may not delete a user
        resp = self.client.post(reverse('members:delete_person', kwargs={'pk': self.user.pk}))
        self.assertEqual(resp.status_code, 403)
        # Ensure meeting is not deleted
        Person.objects.get(pk=self.user.pk)
