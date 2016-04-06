from django.shortcuts import redirect
from django.views.generic import TemplateView


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
