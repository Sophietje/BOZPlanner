from django.shortcuts import render, get_list_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView

from meetings.models import Meeting


class MeetingsView(ListView):
    model = Meeting
    template_name = 'meetings/meetings.html'

class MeetingCreate(CreateView):
    model = Meeting

class MeetingUpdate(UpdateView):
    model = Meeting

class MeetingDelete(DeleteView):
    model = Meeting