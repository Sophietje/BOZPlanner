from django.contrib.auth.models import User, Permission, Group, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
            ("change_groups", "Can change user groups"),
            ("list_persons", "Can view persons"),
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

class Preferences(models.Model):
    person = models.OneToOneField("Person")
    overview = models.ManyToManyField(Organization, blank=True, related_name='+')
    reminder = models.ManyToManyField(Organization, blank=True, related_name='+')

    class Meta:
        verbose_name_plural = 'Preferences'
        verbose_name = 'Preferences'

    def __str__(self):
        return self._meta.verbose_name + ' for ' + self.person.__str__()


@receiver(post_save, sender=Person)
def create_preferences(sender, instance, created, **kwargs):
     if created:
         Preferences.objects.create(person=instance)