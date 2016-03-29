from datetime import datetime

from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from meetings.models import Meeting
from members.models import Person, Organization


class TestsMeetingsViews(TestCase):
    def setUp(self):
        # Voeg gebruiker toe aan de database
        o = Organization.objects.create(name='EWI')
        user = Person.objects.create(username='s1234567', password='secret', first_name='test')
        user.set_password('secret')
        user.organizations.add(o)
        # Voeg juiste permissions toe voor tests
        permission_1 = Permission.objects.get(codename='list_meetings')
        user.user_permissions.add(permission_1)
        permission_2 = Permission.objects.get(codename='view_all')
        user.user_permissions.add(permission_2)
        user.save()
        # Maak een sessie en log de gebruiker in
        self.client = Client()
        self.client.force_login(user)

    def test_meetings_list(self):
        resp = self.client.get(reverse('meetings:meetings-list'))
        # User is ingelogd met juiste permission dus moet doorgestuurd worden naar meetings pagina
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)

    def test_context_meetings_list(self):
        # Add meeting to see whether the request has the expected context
        o = Organization.objects.get(pk=1)
        m = Meeting.objects.create(organization=o, begin_time=datetime(2016, 11, 11, 11, 11, 0), end_time=datetime(2016, 11, 12, 13, 14, 0), place='Zi 0000')
        m.save()
        resp = self.client.get(reverse('meetings:meetings-list'))
        self.assertEqual([meeting.pk for meeting in resp.context['object_list']], [1])

    # Test of niet bestaande meetings een 404 geven
    # def test_detail(self):
        # resp = self.client.get('/meetings/1/')
        # print(resp)
        # self.assertEqual(resp.status_code, 200)

        # Ensure that non-existent meetings throw a 404.
        # resp = self.client.get('/meetings/9999/')
        # self.assertEqual(resp.status_code, 404)

    # Test of the context is wat je verwacht (lijst van meetings)

    #