from django.core.urlresolvers import reverse
from django.test import TestCase

from members.models import Organization
from members.tests.test_user_utils import TestUserMixin


class TestStudentOrganizationsViews(TestCase, TestUserMixin):
    def setUp(self):
        self.setupStudentSession()

    def test_organizations_list(self):
        resp = self.client.get(reverse('members:list_organization'))
        # Student is not allowed to view organizations so should be redirected (302)
        self.assertEqual(resp.status_code, 403)

    def test_organizations_correct_update(self):
        p_orga = Organization.objects.create(name='Parent')
        resp = self.client.post(reverse('members:list_organization'), {'edit': self.o.pk, 'name':'Child', 'parent_organization': p_orga.pk})

        self.assertEqual(resp.status_code, 403)
        # Ensure nothing has been updated (student is not allowed to update organizations)
        self.assertEqual(Organization.objects.get(pk=1).name, 'Test')
        self.assertEqual(Organization.objects.get(pk=1).parent_organization, None)

    def test_organizations_incorrect_update(self):
        # Ensure that a non-existent pk throws a 404
        resp = self.client.post(reverse('members:list_organization'), {'edit': 9999})
        self.assertEqual(resp.status_code, 403)

        # Post NO data
        resp = self.client.post(reverse('members:list_organization'), {'edit': self.o.pk})
        self.assertEqual(resp.status_code, 403)

        # Post junk data
        resp = self.client.post(reverse('members:list_organization'), {'edit': self.o.pk, 'foo': 'bar'})
        self.assertEqual(resp.status_code, 403)

        # Send non-existent parent-organization pk
        resp = self.client.post(reverse('members:list_organization'), {'edit': self.o.pk, 'parent_organization': 9999})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(Organization.objects.get(pk=self.o.pk).parent_organization, None)

    def test_organizations_correct_delete(self):
        # Add new organization
        orga = Organization.objects.create(name='Parent')
        self.assertEqual('Parent', Organization.objects.get(pk=orga.pk).name)
        # Delete newly added organization
        resp = self.client.post(reverse('members:delete_organization', kwargs={'pk': orga.pk}))
        self.assertEqual(resp.status_code, 403)
        # Ensure that organization has NOT been deleted
        self.assertNotEqual(None, Organization.objects.get(pk=orga.pk))
        # Delete newly added organization
        Organization.objects.get(pk=orga.pk).delete()

    def test_organizations_incorrect_delete(self):
        # Delete non-existing organization
        resp = self.client.post(reverse('members:delete_organization', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 403)
        # Assert that list of organizations did not change
        self.assertEqual([orga for orga in Organization.objects.all()], [self.o])
