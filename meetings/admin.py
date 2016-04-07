from django.contrib import admin

from meetings.models import Meeting, Minutes

class MeetingAdmin(admin.ModelAdmin):
    list_display = ('organization', 'begin_time', 'end_time', 'place', 'secretary')

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Minutes)

