from django import forms
from django.forms import models

from members.models import Organization, Person, Preferences


class OrganizationForm(models.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'parent_organization']


class PersonForm(models.ModelForm):
    class Meta:
        model = Person
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'organizations']


class PreferencesForm(models.ModelForm):
    def __init__(self, *args, request, **kwargs):
        self.request = request
        super(PreferencesForm, self).__init__(*args, **kwargs)
        self.fields['overview_secretary'].queryset = Organization.objects.filter(
            pk__in=map(lambda org: org.pk, self.request.user.all_organizations))

    def clean(self):
        cleaned_data = super(PreferencesForm, self).clean()

        organizations = self.request.user.all_organizations

        if any(group not in organizations for group in cleaned_data.get('overview_secretary') or []):
            raise PermissionError

    class Meta:
        model = Preferences
        fields = [
            'overview',
            'reminder',
            'calendar_secretary',
            'calendar_organization',
            'zoom_in',
            'overview_secretary',
            'confirmation_secretary'
        ]
