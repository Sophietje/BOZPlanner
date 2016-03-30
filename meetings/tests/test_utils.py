from datetime import datetime

from django.contrib.auth.models import Permission
from django.test import Client

from meetings.models import Meeting
from members.models import Organization, Person


class TestUtils():
    def setupStudentSession(self):
        # Add user to the database
        o = Organization.objects.create(name='Test')
        user = Person.objects.create(username='s1234567', password='secret', first_name='test')
        user.set_password('secret')
        user.organizations.add(o)

        # Add permissions belonging to general student accounts
        permission_1 = Permission.objects.get(codename='list_meetings')
        user.user_permissions.add(permission_1)
        permission_2 = Permission.objects.get(codename='add_minutes')
        user.user_permissions.add(permission_2)
        permission_3 = Permission.objects.get(codename='change_minutes')
        user.user_permissions.add(permission_3)
        permission_4 = Permission.objects.get(codename='delete_minutes')
        user.user_permissions.add(permission_4)
        permission_5 = Permission.objects.get(codename='view_organization')
        user.user_permissions.add(permission_5)
        user.save()

        # Create a session, log the user in
        self.client = Client()
        self.client.force_login(user)

    def setupAdminSession(self):
        # Add user to the database
        o = Organization.objects.create(name='Test')
        user = Person.objects.create(username='m1234567', password='secret', first_name='test')
        user.set_password('secret')
        user.organizations.add(o)

        # Add permissions belonging to admin accounts
        user.is_superuser = True
        user.save()

        # Create a session, log the user in
        self.client = Client()
        self.client.force_login(user)

    def setupMeeting(self):
        # Get first organization in database, this should be "Test"
        o = Organization.objects.get(pk=1)
        # Add meeting to be able to check the context
        m = Meeting.objects.create(organization=o, begin_time=datetime(9999, 11, 11, 11, 11, 0), end_time=datetime(9999, 11, 12, 13, 14, 0), place='Zi 0000')
        m.save()

        # Add meeting from new organization
        p = Organization.objects.create(name='Special')
        m = Meeting.objects.create(organization=p, begin_time=datetime(9999, 11, 12, 14, 15, 0), end_time=datetime(9999, 11, 12, 15, 15, 0), place='Educafé')
        m.save()

        # Add meeting from suborganization of 'Test'
        q = Organization.objects.create(name='Subtest', parent_organization=o)
        m = Meeting.objects.create(organization=q, begin_time=datetime(9999, 11, 12, 11, 12, 0), end_time=datetime(9999, 11, 12, 12, 0, 0), place='CR 2D')
        m.save()