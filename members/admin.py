from django.contrib import admin

from members.models import Person, Organization, Preferences

admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Preferences)