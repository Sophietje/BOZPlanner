from django.contrib import admin

from sokolov.models import User, Meeting, Minutes, Organization

admin.site.register(User)
admin.site.register(Meeting)
admin.site.register(Minutes)
admin.site.register(Organization)