from django.core.urlresolvers import reverse
from django.test import TestCase

from members.models import Organization
from members.tests.test_user_utils import TestUserUtils


class TestStudentOrganizationsViews(TestCase):
    def setUp(self):
        TestUserUtils.setupStudentSession(self)

    def test_organizations_list(self):
        resp = self.client.get(reverse('members:organizations'))
        # Student is not allowed to view organizations so should be redirected (302)
        self.assertEqual(resp.status_code, 302)

    def test_organizations_correct_update(self):
        p_orga = Organization.objects.create(name='Parent')
        resp = self.client.post(reverse('members:organization_update', kwargs={'pk': 1}), {'name':'Child', 'parent_organization': p_orga.pk})

        self.assertEqual(resp.status_code, 302)
        # Ensure nothing has been updated (student is not allowed to update organizations)
        self.assertEqual(Organization.objects.get(pk=1).name, 'Test')
        self.assertEqual(Organization.objects.get(pk=1).parent_organization_id, None)

    def test_organizations_incorrect_update(self):
        # Ensure that a non-existent pk throws a 404
        resp = self.client.post(reverse('members:organization_update', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 302)

        # Post NO data
        resp = self.client.post(reverse('members:organization_update', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 302)

        # Post junk data
        resp = self.client.post(reverse('members:organization_update', kwargs={'pk': 1}), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 302)

        # Send non-existent parent-organization pk
        resp = self.client.post(reverse('members:organization_update', kwargs={'pk': 1}), {'parent_organization': 9999})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Organization.objects.get(pk=1).parent_organization, None)

    def test_organizations_correct_delete(self):
        # Add new organization
        orga = Organization.objects.create(name='Parent')
        self.assertEqual('Parent', Organization.objects.get(pk=2).name)
        # Delete newly added organization
        resp = self.client.post(reverse('members:organization_delete', kwargs={'pk': orga.pk}))
        self.assertEqual(resp.status_code, 302)
        # Ensure that organization has NOT been deleted
        self.assertNotEqual(None, Organization.objects.get(pk=2))
        # Delete newly added organization
        Organization.objects.get(pk=2).delete()

    def test_organizations_incorrect_delete(self):
        # Delete non-existing organization
        resp = self.client.post(reverse('members:organization_delete', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 302)
        # Assert that list of organizations did not change
        self.assertEqual([orga.pk for orga in Organization.objects.all()], [1])
