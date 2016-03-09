from django.shortcuts import redirect

from bozplanner.settings import LOGIN_REDIRECT_URL


def index(request):
    if request.user.is_authenticated():
        return redirect('meetings:meetings-list')
    else:
        return redirect(LOGIN_REDIRECT_URL)
