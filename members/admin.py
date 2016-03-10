from django.contrib import admin

from members.models import Person, Organizations

admin.site.register(Person)
admin.site.register(Organizations)