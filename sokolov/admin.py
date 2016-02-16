from django.contrib import admin

from sokolov.models import Person, Meeting, Minutes, Organization

admin.site.register(Person)
admin.site.register(Meeting)
admin.site.register(Minutes)
admin.site.register(Organization)