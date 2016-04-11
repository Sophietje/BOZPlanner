from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
import icalendar

from meetings.managers import MeetingManager


class Meeting(models.Model):
    """A meeting planned by a planner"""
    objects = MeetingManager()

    place = models.CharField(max_length=255, verbose_name=_("place"))
    begin_time = models.DateTimeField(verbose_name=_("begin date & time"))
    end_time = models.DateTimeField(verbose_name=_("end date & time"))
    secretary = models.ForeignKey("members.Person", related_name="secretary", blank=True, null=True, verbose_name=_("secretary"))
    organization = models.ForeignKey("members.Organization", verbose_name=_("organization"))

    @property
    def is_soon(self):
        td = self.begin_time - datetime.now()
        return td <= timedelta(days=10)

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
        super(Meeting, self).clean()

        if self.begin_time > self.end_time:
            raise ValidationError(_('End of a meeting cannot be before the start of a meeting.'))

    def __str__(self):
        return _("OLC meeting of {}").format(self.organization)

    class Meta:
        permissions = [
            ("list_meetings", "Can list meetings"),
            ("list_meetings_organization", "Can list meetings of her organization"),
            ("list_meetings_all", "Can list all meetings"),
            ("view_organization", "Can view meetings from own organization"),
            ("view_all", "Can view all meetings"),
        ]
        verbose_name = "Meeting"


class Minutes(models.Model):
    """Minutes corresponding to a meeting"""
    meeting = models.ForeignKey("Meeting", related_name='minutes', verbose_name=_("meeting"))
    file = models.FileField(verbose_name=_("file"))
    original_name = models.TextField(verbose_name=_("original name"))
    date = models.DateTimeField(verbose_name=_("date"))

    class Meta:
        verbose_name_plural = "minutes"
        permissions = [
            ("approve", "Can approve minutes"),
        ]
