import icalendar
from django.db import models


class MeetingManager(models.Manager):
    """Manager for the Meeting model that adds a method to retrieve the queryset as an iCalendar"""

    def __init__(self):
        self.queryset_class = MeetingQuerySet
        super(MeetingManager, self).__init__()

    def get_queryset(self):
        return self.queryset_class(self.model)

    def __getattr__(self, item, *args):
        try:
            return getattr(self.__class__, item, *args)
        except AttributeError:
            return getattr(self.get_queryset(), item, *args)


class MeetingQuerySet(models.query.QuerySet):
    def as_icalendar(self):
        """Returns the current queryset as an iCalendar"""
        calendar = icalendar.Calendar()
        calendar['x-wr-calname'] = 'OLC Meetings'
        calendar['x-wr-caldesc'] = 'OLC Meetings'

        for meeting in self:
            calendar.add_component(meeting.as_icalendar_event())

        return calendar
