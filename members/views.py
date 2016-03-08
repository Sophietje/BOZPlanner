from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView

from members.auth import permission_required
from members.models import Person


class PermissionDeniedView(TemplateView):
    template_name = "http/403.html"

@permission_required("")
class PersonsView(ListView):
    model = Person
    template_name = "person/list.html"

class PersonCreateView(CreateView):
    template_name = "person/form.html"
    model = Person
    success_url = reverse_lazy("persons")
    fields = [
        "first_name",
        "last_name",
        "email",
        "groups",
        "organization",
    ]

class PersonUpdateView(UpdateView):
    template_name = "person/form.html"
    model = Person
    success_url = reverse_lazy("persons")
    fields = [
        "first_name",
        "last_name",
        "email",
        "groups",
        "organization",
    ]

class PersonDeleteView(DeleteView):
    model = Person
    template_name = "none"
