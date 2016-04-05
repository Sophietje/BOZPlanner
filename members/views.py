from urllib.parse import urlencode
from django.contrib.auth import login
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View

from bozplanner.local import WEBCAL_BASE
from bozplanner.settings import HAVE_DJANGOSAML2, LOGOUT_REDIRECT_URL
from members.auth import permission_required
from members.forms import OrganizationForm, PersonForm
from members.models import Person, Organization, Preferences


class PermissionDeniedView(TemplateView):
    template_name = "http/templates/403.html"

@permission_required("members.list_persons")
class PersonsView(TemplateView):
    template_name = "person/list.html"

    def get_context_data(self):
        object_list = Person.objects.filter(is_active=True)

        for person in object_list:
            person.form = PersonForm(instance=person, auto_id="%s_" + str(person.pk))

        return locals()

@permission_required("members.add_person")
class PersonCreateView(CreateView):
    template_name = "person/form.html"
    model = Person
    success_url = reverse_lazy("members:persons")
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "groups",
        "organizations",
    ]

@permission_required("members.change_person")
class PersonUpdateView(UpdateView):
    template_name = "person/form.html"
    model = Person
    success_url = reverse_lazy("members:persons")
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "groups",
        "organizations",
    ]

@permission_required("members.delete_person")
class PersonDeleteView(View):
    def get(self, request, pk):
        object = get_object_or_404(Person, pk=pk)
        return render(request, "person/delete.html", locals())

    def post(self, request, pk):
        object = get_object_or_404(Person, pk=pk)
        object.is_active = False
        object.save()
        return redirect("members:persons")

@permission_required("members.list_organizations")
class OrganizationsView(TemplateView):
    template_name = "organization/list.html"

    def get_context_data(self):
        object_list = Organization.objects.all()

        for organization in object_list:
            organization.form = OrganizationForm(instance=organization, auto_id="%s_" + str(organization.pk))

        return locals()

@permission_required("members.add_organization")
class OrganizationCreateView(CreateView):
    template_name = "organization/form.html"
    model = Organization
    success_url = reverse_lazy("members:organizations")
    fields = [
        "name",
        "parent_organization",
    ]

@permission_required("members.change_organization")
class OrganizationUpdateView(UpdateView):
    template_name = "organization/form.html"
    model = Organization
    success_url = reverse_lazy("members:organizations")
    fields = [
        "name",
        "parent_organization",
    ]

@permission_required("members.delete_organization")
class OrganizationDeleteView(DeleteView):
    template_name = "organization/delete.html"
    model = Organization
    success_url = reverse_lazy("members:organizations")

@permission_required("members.list_organizations")
class OrganizationEmailView(View):
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

class SettingsView(UpdateView):
    template_name = "settings.html"
    model = Preferences
    success_url = reverse_lazy("members:preferences")
    fields = [
        'overview',
        'reminder',
        'agenda_secretary',
        'agenda_organization',
        'zoom_in',
        'overview_student',
        'confirmation_student'
    ]

    def get_object(self, queryset=None):
       return self.request.user.preferences

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data()
        context['first_login'] = self.request.user.first_login
        context['webcal_url'] = 'webcal://{}/meetings/agenda/{}/{}'.format(
            WEBCAL_BASE, self.request.user.id, self.request.user.agenda_token)
        google_args = {'cid': 'http://{}/meetings/agenda/{}/{}'.format(
            WEBCAL_BASE, self.request.user.id, self.request.user.agenda_token
        )}
        context['google_url'] = 'http://www.google.com/calendar/render?' + urlencode(google_args)

        if self.request.user.first_login:
            self.request.user.first_login = False
            self.request.user.save()

        return context

class SudoView(View):
    def post(self, request):
        user = Person.objects.get(pk=request.POST['pk'])

        logout(request)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return redirect('meetings:meetings-list')
