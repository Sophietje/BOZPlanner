from django.contrib import admin

from meetings.models import Meeting, Minutes

admin.site.register(Meeting)
admin.site.register(Minutes)