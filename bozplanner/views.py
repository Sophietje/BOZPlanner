from django.shortcuts import redirect
import os

import datetime
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView
from django.http import HttpResponse

from bozplanner.settings import LOGIN_REDIRECT_URL

def index(request):
    if request.user.is_authenticated():
        if request.user.first_login:
            return redirect('members:preferences')
        else:
            return redirect('meetings:meetings-list')
    else:
        return redirect('/saml2/login/')

class HelpView(TemplateView):
    template_name = "help.html"
