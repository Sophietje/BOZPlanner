from django.core.urlresolvers import reverse
from django.test import TestCase

from members.models import Person, Organization
from members.tests.test_user_utils import TestUserUtils


class TestAdminUsersViews(TestCase):
    def setUp(self):
        TestUserUtils.setupAdminSession(self)

    def test_users_list(self):
        resp = self.client.get(reverse('members:persons'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([user.pk for user in resp.context['object_list']], [1])

    def test_users_correct_update(self):
        # User that will be updated
        user_1 = Person.objects.get(pk=1)

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
        self.assertEqual(user_1.all_organizations, [Organization.objects.get(pk=1)])

        # Post the data
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 1}), {'username': username, 'first_name':first_name, 'last_name':last_name, 'email':email})

        # Assert that it redirects to the overview Users page
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('members:persons'))

        # Assert that
        user_1 = Person.objects.get(pk=1)
        self.assertEqual(user_1.username, 'm7654321')
        self.assertEqual(user_1.first_name, first_name)
        self.assertEqual(user_1.last_name, 'Tester')
        self.assertEqual(user_1.email, 'test@utwente.nl')
        self.assertEqual(user_1.all_organizations, [])

    def test_users_incorrect_update(self):
        # Ensure that a non-existent pk throws a 404
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)

        # Post NO data
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

        # Post junk data
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 1}), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)

        # Send non-existent Organization pk
        organizations = Person.objects.get(pk=1).all_organizations
        resp = self.client.post(reverse('members:person_update', kwargs={'pk': 1}), {'organizations':[9999]})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(organizations, Person.objects.get(pk=1).all_organizations)

    def test_users_correct_delete(self):
        # Add user to delete
        user = Person.objects.create(username='foo', first_name='foo')
        self.assertEqual(Person.objects.get(pk=2).username, 'foo')

        # Delete existing user
        resp = self.client.post(reverse('members:person_delete', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 302)

        # Assert that user no longer exists
        resp = self.client.get(reverse('members:persons'))
        self.assertEqual([user.pk for user in resp.context['object_list']], [1])

    def test_users_incorrect_delete(self):
        # Delete non-existing meeting
        resp = self.client.post(reverse('members:person_delete', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)