"""Provides the authentication backend for the University of Twente"""
from django.core.exceptions import PermissionDenied

from sokolov.models import User


class PhishingBackend(object):
    """Backend that directly verifies username and password, bypassing SSO"""

    def authenticate(self, username=None, password=None):
        if username != "s1481304":
            raise PermissionDenied

        return User.objects.get(username=username)