from django import forms

from meetings.models import Meeting


class MeetingForm(forms.ModelForm):
    class Meta:
        fields = ['organization', 'secretary', 'begin_time', 'end_time', 'place']
        model = Meeting
