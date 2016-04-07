from django.core.urlresolvers import reverse
from django.test import TestCase

from members.models import Person, Organization
from members.tests.test_user_utils import TestUserMixin


class TestAdminUsersViews(TestCase, TestUserMixin):
    def setUp(self):
        self.setupAdminSession()

    def test_users_list(self):
        resp = self.client.get(reverse('members:list_person'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([user for user in resp.context['object_list']], [self.user])

    def test_users_correct_update(self):
        # User that will be updated
        user_1 = Person.objects.get()

        # The to-be-updated data
        username = 'm7654321'
        first_name = 'Testing'
        last_name = 'Tester'
        email = 'test@utwente.nl'

        # Assert that this is the correct User
        self.assertEqual(user_1.username, 'm1234567')
        self.assertEqual(user_1.first_name, 'test')
        self.assertEqual(user_1.last_name, '')
        self.assertEqual(user_1.email, '')
        self.assertEqual(user_1.all_organizations, [self.o])

        # Post the data
        resp = self.client.post(reverse('members:change_person', kwargs={'pk': user_1.pk}), {'username': username, 'first_name':first_name, 'last_name':last_name, 'email':email})

        # Assert that it redirects to the overview Users page
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('members:list_person'))

        # Assert that the user now contains the new data posted to person_update
        user_1 = Person.objects.get(pk=user_1.pk)
        self.assertEqual(user_1.username, 'm7654321')
        self.assertEqual(user_1.first_name, first_name)
        self.assertEqual(user_1.last_name, 'Tester')
        self.assertEqual(user_1.email, 'test@utwente.nl')
        self.assertEqual(user_1.all_organizations, [])

    def test_users_incorrect_update(self):
        # Ensure that a non-existent pk throws a 404
        resp = self.client.post(reverse('members:change_person', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)

        # Post NO data
        resp = self.client.post(reverse('members:change_person', kwargs={'pk': self.user.pk}))
        self.assertEqual(resp.status_code, 200)

        # Post junk data
        resp = self.client.post(reverse('members:change_person', kwargs={'pk': self.user.pk}), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)

        # Send non-existent Organization pk
        organizations = Person.objects.get(pk=1).all_organizations
        resp = self.client.post(reverse('members:change_person', kwargs={'pk': 1}), {'organizations':[9999]})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(organizations, Person.objects.get(pk=1).all_organizations)

    def test_users_correct_delete(self):
        # Add user to delete
        user = Person.objects.create(username='foo', first_name='foo')
        self.assertEqual(Person.objects.get(pk=user.pk).username, 'foo')

        # Delete existing user
        resp = self.client.post(reverse('members:delete_person', kwargs={'pk': user.pk}))
        self.assertEqual(resp.status_code, 302)

        # Assert that user no longer exists
        resp = self.client.get(reverse('members:list_person'))
        self.assertEqual([user for user in resp.context['object_list']], [self.user])

    def test_users_incorrect_delete(self):
        # Delete non-existing meeting
        resp = self.client.post(reverse('members:delete_person', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)
