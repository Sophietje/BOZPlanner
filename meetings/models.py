from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.db import models
from django.core.urlresolvers import reverse
import icalendar

from meetings.managers import MeetingManager


class Meeting(models.Model):
    """A meeting planned by a planner"""
    objects = MeetingManager()

    place = models.CharField(max_length=255)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    secretary = models.ForeignKey("members.Person", related_name="secretary", blank=True, null=True)
    organization = models.ForeignKey("members.Organization")
    planner = models.ForeignKey("members.Person", related_name="planner", blank=True, null=True)

    def as_icalendar_event(self):
        """Returns a copy of this meeting as an iCalendar event
        If a secretary is set, the secretary is added as an attendee."""

        event = icalendar.Event()
        event.add("summary", str(self))
        event.add("dtstart", self.begin_time)
        event.add("dtend", self.end_time)

        if self.secretary:
            secretary = icalendar.vCalAddress("MAILTO:{}".format(self.secretary.email))
            secretary.params["cn"] = self.secretary.get_full_name()
            # Required participant, refer to https://www.ietf.org/rfc/rfc2445.txt
            secretary.params["ROLE"] = "REQ-PARTICIPANT"
            event.add("attendee", secretary, encode=0)

        return event

    def clean(self):
        if self.begin_time > self.end_time:
            raise ValidationError

    def __str__(self):
        return _("OLC-vergadering van {}").format(self.organization)

    def get_absolute_url(self):
        return reverse('meetings:meetings-list')

class Minutes(models.Model):
    """Minutes corresponding to a meeting"""
    file = models.FileField(upload_to="minutes")
    meeting = models.ForeignKey("Meeting")
    approved_by = models.ForeignKey("members.Person", null=True)

    class Meta:
        verbose_name_plural = "Minutes"