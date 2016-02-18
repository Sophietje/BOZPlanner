import icalendar
from django.db import models

class MeetingManager(models.Manager):
    """Manager for the Meeting model that adds a method to retrieve the queryset as an iCalendar"""

    def as_icalendar(self):
        """Returns the current queryset as an iCalendar"""
        calendar = icalendar.Calendar()

        for meeting in self.get_queryset():
            calendar.add_component(meeting.as_icalendar_event())

        return calendar