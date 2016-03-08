"""Provides the authentication backend for the University of Twente"""
from django.core.exceptions import PermissionDenied

from members.models import Person


class PhishingBackend(object):
    """Backend that directly verifies username and password, bypassing SSO"""

    def authenticate(self, username=None, password=None):
        """Authenticate a user given a username and password"""

        if username != "s1481304":
            raise PermissionDenied

        return Person.objects.get(username=username)
