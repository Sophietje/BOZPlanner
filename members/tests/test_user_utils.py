from django.contrib.auth.models import Permission
from django.test import Client

from members.models import Organization, Person


class TestUserUtils():
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