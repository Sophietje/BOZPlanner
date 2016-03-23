from django import forms

from meetings.models import Meeting


class UploadForm(forms.Form):
    minutes = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class MeetingForm(forms.ModelForm):
    class Meta:
        fields = ['organization', 'secretary', 'begin_time', 'end_time', 'place']
        model = Meeting
