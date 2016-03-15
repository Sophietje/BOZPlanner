from django import forms

from meetings.models import Meeting


class UploadForm(forms.Form):
    minutes = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class MeetingForm(forms.ModelForm):
    class Meta:
        fields = ['place', 'begin_time', 'end_time', 'secretary', 'organization']
        model = Meeting