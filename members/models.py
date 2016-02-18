import django.contrib.auth.models
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
            ("approve_minutes", "Can approve minutes"),
        )

    def __str__(self):
        return self.get_full_name()

class Organization(models.Model):
    """An organization for which OLC meetings can be planned in BOZPlanner"""
    name = models.CharField(max_length=255)
    parent_organization = models.ForeignKey("Organization", null=True, blank=True)

    def __str__(self):
        return self.name
