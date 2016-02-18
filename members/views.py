from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView

from members.models import Person


class PersonsView(ListView):
    model = Person
    template_name = "person/list.html"

class PersonCreateView(CreateView):
    model = Person
    template_name = "none"

class PersonUpdateView(UpdateView):
    model = Person
    template_name = "none"

class PersonDeleteView(DeleteView):
    model = Person
    template_name = "none"