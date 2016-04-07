from django.core.urlresolvers import reverse
from django.test import TestCase

from members.models import Organization
from members.tests.test_user_utils import TestUserMixin


class TestAdminOrganizationsViews(TestCase, TestUserMixin):
    def setUp(self):
        self.setupAdminSession()

    def test_organizations_list(self):
        resp = self.client.get(reverse('members:list_organization'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([orga for orga in resp.context['object_list']], [self.o])

    def test_organizations_correct_update(self):
        p_orga = Organization.objects.create(name='Parent')
        resp = self.client.post(reverse('members:change_organization', kwargs={'pk': self.o.pk}), {'name':'Child', 'parent_organization': p_orga.pk})

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Organization.objects.get(pk=self.o.pk).name, 'Child')
        self.assertEqual(Organization.objects.get(pk=self.o.pk).parent_organization, p_orga)

    def test_organizations_incorrect_update(self):
        # Ensure that a non-existent pk throws a 404
        resp = self.client.post(reverse('members:change_organization', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)

        # Post NO data
        resp = self.client.post(reverse('members:change_organization', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

        # Post junk data
        resp = self.client.post(reverse('members:change_organization', kwargs={'pk': 1}), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)

        # Send non-existent parent-organization pk
        resp = self.client.post(reverse('members:change_organization', kwargs={'pk': 1}), {'parent_organization': 9999})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Organization.objects.get(pk=1).parent_organization, None)

    def test_organizations_correct_delete(self):
        # Add new organization
        orga = Organization.objects.create(name='Parent')
        resp = self.client.get(reverse('members:list_organization'))
        self.assertEqual([orga for orga in resp.context['object_list']], [self.o, orga])
        # Delete newly added organization
        resp = self.client.post(reverse('members:delete_organization', kwargs={'pk': orga.pk}))
        self.assertEqual(resp.status_code, 302)
        # Ensure that organization has been deleted
        resp = self.client.get(reverse('members:list_organization'))
        self.assertEqual([orga for orga in resp.context['object_list']], [self.o])

    def test_organizations_incorrect_delete(self):
        # Delete non-existing organization
        resp = self.client.post(reverse('members:delete_organization', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)
        # Assert that list of organizations did not change
        resp = self.client.get(reverse('members:list_organization'))
        self.assertEqual([orga for orga in resp.context['object_list']], [self.o])
