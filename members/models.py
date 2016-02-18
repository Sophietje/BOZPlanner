from django.contrib.auth.models import User, Permission
from django.db import models


class Person(User):
    """Any user that can log in to BOZPlanner"""
    organization = models.ManyToManyField("Organization", blank=True)

    class Meta:
        verbose_name = "person"

    def __str__(self):
        return self.get_full_name()



class Organization(models.Model):
    """An organization for which OLC meetings can be planned in BOZPlanner"""
    name = models.CharField(max_length=255)
    parent_organization = models.ForeignKey("Organization", null=True, blank=True)

    def __str__(self):
        return self.name
