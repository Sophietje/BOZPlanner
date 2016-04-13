from django import forms

from meetings.models import Meeting
from members.models import Person


class MeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields['secretary'].queryset = Person.objects.filter(is_active=True)

    class Meta:
        fields = ['organization', 'secretary', 'begin_time', 'end_time', 'place']
        model = Meeting
