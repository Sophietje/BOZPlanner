import logging

from django.contrib.auth import decorators
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

from members.models import Person

logger = logging.getLogger('bozplanner')

login_required = method_decorator(decorators.login_required, name='dispatch')

def permission_required(*args, **kwargs):
    return method_decorator(decorators.permission_required(*args, **kwargs), name='dispatch')

class SAML2Backend:
    def authenticate(self, session_info, attribute_mapping, create_unknown_user):
        # Temporary hack to get the s-nummer out of the name_id (s1234567@utwente.nl)

        username = session_info['name_id'].text.split("@")[0]

        try:
            return Person.objects.get(username=username)
        except Person.DoesNotExist:
            raise PermissionDenied

    def get_user(self, user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            return None
