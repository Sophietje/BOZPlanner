from django.contrib.auth.models import User, Permission, Group, AbstractUser
from django.db import models


class Person(AbstractUser):
    """Any user that can log in to BOZPlanner"""
    organizations = models.ManyToManyField("Organization", blank=True)

    @property
    def is_admin(self):
        return self.groups.filter(name="Administrator").exists()

    @property
    def is_planner(self):
        return self.groups.filter(name="Planner").exists()

    @property
    def is_secretary(self):
        return self.groups.filter(name="Secretary").exists()
    
    @property
    def is_approver(self):
        return self.groups.filter(name="Approver").exists()
    
    @property
    def is_user_manager(self):
        return self.groups.filter(name="User Manager").exists()

    @property
    def all_organizations(self):
        result = []

        for organization in self.organizations.all():
            result += organization.all_organizations()

        return result

    class Meta:
        verbose_name = "person"
        permissions = [
            ("groups", "Can change user groups"),
        ]

    def __str__(self):
        return self.get_full_name()


class Organization(models.Model):
    """An organization for which OLC meetings can be planned in BOZPlanner"""
    name = models.CharField(max_length=255)
    parent_organization = models.ForeignKey("Organization", null=True, blank=True)

    def all_organizations(self):
        result = [self]

        for organization in Organization.objects.filter(parent_organization=self):
            result += organization.all_organizations()

        return result

    def __str__(self):
        return self.name
