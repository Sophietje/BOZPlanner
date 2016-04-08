from urllib.parse import urlencode
from django.contrib.auth import login
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View

from bozplanner.local import WEBCAL_BASE
from bozplanner.settings import HAVE_DJANGOSAML2, LOGOUT_REDIRECT_URL
from bozplanner.views import EditModalListView
from members.auth import permission_required
from members.forms import OrganizationForm, PersonForm, PreferencesForm
from members.models import Person, Organization, Preferences


@permission_required("members.list_persons")
class ListPersonView(EditModalListView):
    model = Person
    form = PersonForm
    edit_permission = "members.change_person"
    success_url = reverse_lazy("members:list_person")
    template_name = "person/list.html"

    def get_context_data(self):
        object_list = Person.objects.filter(is_active=True)
        return locals()


@permission_required("members.add_person")
class AddPersonView(CreateView):
    template_name = "person/form.html"
    model = Person
    success_url = reverse_lazy("members:list_person")
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "groups",
        "organizations",
    ]


@permission_required("members.delete_person")
class DeletePersonView(View):
    def post(self, request, pk):
        object = get_object_or_404(Person, pk=pk)
        object.is_active = False
        object.save()
        return redirect("members:list_person")


@permission_required("members.list_organizations")
class ListOrganizationView(EditModalListView):
    model = Organization
    form = OrganizationForm
    edit_permission = "members.change_organization"
    success_url = reverse_lazy("members:list_organization")
    template_name = "organization/list.html"

    def get_context_data(self):
        object_list = Organization.objects.all()
        return locals()


@permission_required("members.add_organization")
class AddOrganizationView(CreateView):
    template_name = "organization/form.html"
    model = Organization
    success_url = reverse_lazy("members:list_organization")
    fields = [
        "name",
        "parent_organization",
    ]


@permission_required("members.delete_organization")
class DeleteOrganizationView(DeleteView):
    template_name = "organization/delete.html"
    model = Organization
    success_url = reverse_lazy("members:list_organization")


@permission_required("members.list_organizations")
class EmailOrganizationView(View):
    def get(self, request, organizations):
        # Verified by URL pattern
        org_ids = map(int, organizations.split(","))
        organizations = set()

        for org_id in org_ids:
            organization = get_object_or_404(Organization, pk=org_id)
            organizations = organizations | set(organization.all_organizations())

        persons = Person.objects.filter(organizations__in=organizations)
        return JsonResponse({"result": list(map(lambda person: person.full_email, persons))})


def logout(request):
    if HAVE_DJANGOSAML2:
        import djangosaml2.views
        result = djangosaml2.views.logout(request)
        auth.logout(request)
        return result
    else:
        auth.logout(request)
        return redirect(LOGOUT_REDIRECT_URL)


class PreferencesView(UpdateView):
    template_name = "settings.html"
    form_class = PreferencesForm
    success_url = reverse_lazy("members:preferences")

    def get_object(self, queryset=None):
       return self.request.user.preferences

    def get_form_kwargs(self):
        args = super(PreferencesView, self).get_form_kwargs()
        args['request'] = self.request
        return args

    def get_context_data(self, **kwargs):
        context = super(PreferencesView, self).get_context_data()
        context['first_login'] = self.request.user.first_login
        context['webcal_url'] = 'webcal://{}/meetings/calendar/{}/{}'.format(
            WEBCAL_BASE, self.request.user.id, self.request.user.calendar_token)
        google_args = {'cid': 'http://{}/meetings/calendar/{}/{}'.format(
            WEBCAL_BASE, self.request.user.id, self.request.user.calendar_token
        )}
        context['google_url'] = 'http://www.google.com/calendar/render?' + urlencode(google_args)

        if self.request.user.first_login:
            self.request.user.first_login = False
            self.request.user.save()

        return context
