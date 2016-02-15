from django.db import models

class User(models.Model):
    """Any user that can log in to BOZPlanner"""
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    organization = models.ManyToManyField("Organization")
    is_admin = models.BooleanField()
    is_secretary = models.BooleanField()
    is_planner = models.BooleanField()

class Meeting(models.Model):
    """A meeting planned by a planner"""
    place = models.CharField(max_length=255)
    date = models.DateField()
    begin_time = models.TimeField()
    end_time = models.TimeField()
    secretary = models.ForeignKey("Meeting")
    organization = models.ForeignKey("Organization")
    planner = models.ForeignKey("User")

class Minutes(models.Model):
    """Minutes corresponding to a meeting"""
    meeting = models.ForeignKey("Meeting")
    approved_by = models.ForeignKey("User", null=True)

    class Meta:
        verbose_name_plural = "Minutes"

class Organization(models.Model):
    """An organization for which OLC meetings can be planned in BOZPlanner"""
    name = models.CharField(max_length=255)