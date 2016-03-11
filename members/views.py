from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, View

from members.auth import permission_required
from members.models import Person


class PermissionDeniedView(TemplateView):
    template_name = "http/templates/403.html"

@permission_required("")
class PersonsView(TemplateView):
    template_name = "person/list.html"

    def get_context_data(self):
        object_list = Person.objects.filter(is_active=True)
        return locals()

class PersonCreateView(CreateView):
    template_name = "person/form.html"
    model = Person
    success_url = reverse_lazy("members:persons")
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
    success_url = reverse_lazy("members:persons")
    fields = [
        "first_name",
        "last_name",
        "email",
        "groups",
        "organization",
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



def logout(request):
    import djangosaml2.views
    result = djangosaml2.views.logout(request)
    auth.logout(request)
    return result
