from django.core.exceptions import ValidationError
from django.db import models


class Meeting(models.Model):
    """A meeting planned by a planner"""
    place = models.CharField(max_length=255)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    secretary = models.ForeignKey("members.Person", related_name="secretary")
    organization = models.ForeignKey("members.Organization")
    planner = models.ForeignKey("members.Person", related_name="planner")

    def clean(self):
        if self.begin_time > self.end_time:
            raise ValidationError

class Minutes(models.Model):
    """Minutes corresponding to a meeting"""
    file = models.FileField(upload_to="minutes")
    meeting = models.ForeignKey("Meeting")
    approved_by = models.ForeignKey("members.Person", null=True)

    class Meta:
        verbose_name_plural = "Minutes"