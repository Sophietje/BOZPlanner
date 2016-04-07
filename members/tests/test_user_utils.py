from django.contrib.auth.models import Permission
from django.test import Client

from members.models import Organization, Person


class TestUserMixin:
    def setupStudentSession(self):
        # Add user to the database
        self.o = Organization.objects.create(name='Test')
        self.user = Person.objects.create(username='s1234567', password='secret', first_name='test')
        self.user.set_password('secret')
        self.user.organizations.add(self.o)

        # Add permissions belonging to general student accounts
        permission_1 = Permission.objects.get(codename='list_meetings')
        self.user.user_permissions.add(permission_1)
        permission_2 = Permission.objects.get(codename='add_minutes')
        self.user.user_permissions.add(permission_2)
        permission_3 = Permission.objects.get(codename='change_minutes')
        self.user.user_permissions.add(permission_3)
        permission_4 = Permission.objects.get(codename='delete_minutes')
        self.user.user_permissions.add(permission_4)
        permission_5 = Permission.objects.get(codename='list_meetings_organization')
        self.user.user_permissions.add(permission_5)
        self.user.save()

        # Create a session, log the user in
        self.client = Client()
        self.client.force_login(self.user)

    def setupAdminSession(self):
        # Add user to the database
        self.o = Organization.objects.create(name='Test')
        self.user = Person.objects.create(username='m1234567', password='secret', first_name='test')
        self.user.set_password('secret')
        self.user.organizations.add(self.o)

        # Add permissions belonging to admin accounts
        self.user.is_superuser = True
        self.user.save()

        # Create a session, log the user in
        self.client = Client()
        self.client.force_login(self.user)
