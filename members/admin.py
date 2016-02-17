from django.contrib import admin

from members.models import Person, Organization

admin.site.register(Person)
admin.site.register(Organization)