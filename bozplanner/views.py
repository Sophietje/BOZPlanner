from django.shortcuts import redirect

from bozplanner.settings import LOGIN_URL


def index(request):
    """Redirects the user to the login page when not authenticated.
    When the user logs in for the first time, the redirect is to the preferences page instead of the home page."""
    if request.user.is_authenticated():
        if request.user.first_login:
            return redirect('members:preferences')
        else:
            return redirect('meetings:list_meeting')
    else:
        return redirect(LOGIN_URL)
