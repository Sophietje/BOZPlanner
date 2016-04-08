from abc import ABCMeta, abstractmethod

from django.forms import ModelForm
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View

from bozplanner.settings import LOGIN_URL


class EditModalListView(View):
    __metaclass__ = ABCMeta
    form = ModelForm
    template_name = None
    model = None
    success_url = None
    edit_permission = None

    @abstractmethod
    def get_context_data(self):
        pass

    def _context(self):
        """Add forms to the subclass-provided object_list"""
        ctx = self.get_context_data()

        for obj in ctx["object_list"]:
            obj.form = type(self).form(instance=obj, auto_id='%s_' + str(obj.pk))

        return ctx

    def get(self, request):
        return render(request, type(self).template_name, self._context())

    def post(self, request):
        if "edit" not in request.POST:
            return self.get(request)

        if not request.user.has_perm(type(self).edit_permission):
            raise PermissionError

        instance = get_object_or_404(type(self).model, pk=int(request.POST["edit"]))

        form = type(self).form(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect(type(self).success_url or instance.get_absolute_url())
        else:
            ctx = self._context()

            # Insert the user values in the correct form
            for obj in ctx["object_list"]:
                if obj == instance:
                    obj.form = form

            # Tell the template to open this modal immediately
            ctx["edit"] = instance.pk

            return render(request, type(self).template_name, ctx)


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
