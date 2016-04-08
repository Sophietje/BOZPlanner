import logging

from django.contrib.auth import decorators

from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators import csrf

from members.models import Person

logger = logging.getLogger('bozplanner')

login_required = method_decorator(decorators.login_required, name='dispatch')

csrf_exempt = method_decorator(csrf.csrf_exempt, name='dispatch')


def permission_required(*args, **kwargs):
    kwargs['raise_exception'] = True
    return method_decorator(decorators.permission_required(*args, **kwargs), name='dispatch')
