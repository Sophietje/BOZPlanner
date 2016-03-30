from django.forms import models

from members.models import Organization, Person


class OrganizationForm(models.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'parent_organization']


class PersonForm(models.ModelForm):
    class Meta:
        model = Person
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'organizations']
