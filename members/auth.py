import logging

from django.core.exceptions import PermissionDenied

logger = logging.getLogger('bozplanner')

class SAML2Backend:
    def authenticate(self, session_info, attribute_mapping, create_unknown_user):
        logger.debug(session_info, attribute_mapping, create_unknown_user)
        raise PermissionDenied
