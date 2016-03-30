from django.forms import models

from members.models import Organization


class OrganizationForm(models.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'parent_organization']
