import django.contrib.auth.models
from django.core.exceptions import ValidationError
from django.db import models

class Person(django.contrib.auth.models.User):
    """Any user that can log in to BOZPlanner"""
    organization = models.ManyToManyField("Organization", blank=True)

    class Meta:
        verbose_name = "person"
        permissions = (
            ("admin", "Can do anything"),
            ("plan", "Can schedule and change meetings"),
            ("take_minutes", "Can upload minutes"),
            ("approve_minutes", "Can approve minutes")
        )

class Meeting(models.Model):
    """A meeting planned by a planner"""
    place = models.CharField(max_length=255)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    secretary = models.ForeignKey("Person", related_name="secretary")
    organization = models.ForeignKey("Organization")
    planner = models.ForeignKey("Person", related_name="planner")

    def clean(self):
        if self.begin_time > self.end_time:
            raise ValidationError

class Minutes(models.Model):
    """Minutes corresponding to a meeting"""
    file = models.FileField(upload_to="minutes")
    meeting = models.ForeignKey("Meeting")
    approved_by = models.ForeignKey("Person", null=True)

    class Meta:
        verbose_name_plural = "Minutes"

class Organization(models.Model):
    """An organization for which OLC meetings can be planned in BOZPlanner"""
    name = models.CharField(max_length=255)
    parent_organization = models.ForeignKey("Organization", null=True)